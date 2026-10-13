# frozen_string_literal: true

# Runs the AI itinerary generation off the request cycle and broadcasts the
# result back into the trip page over Turbo Streams.
#
# The generated preview is cached (so the confirm request can read it without
# trusting client-supplied data) and is only ever persisted through
# TripItemsBulkImport on explicit confirmation.
class GenerateItineraryJob < ApplicationJob
  queue_as :default

  CACHE_TTL       = 30.minutes
  IN_PROGRESS_TTL = 5.minutes
  RESULT_TARGET   = "itinerary-generation-result"

  # Queues a generation unless one is already queued or running for this
  # trip/user. This stops repeated accidental submissions (for example a
  # double-clicked button) from enqueuing redundant work. The job clears the
  # marker as soon as it finishes, so regeneration after a result still works.
  def self.enqueue_unless_running(trip:, user:)
    key = in_progress_key(trip: trip, user: user)
    return false if Rails.cache.read(key).present?

    Rails.cache.write(key, true, expires_in: IN_PROGRESS_TTL)
    perform_later(trip.id, user.id)
    true
  end

  def self.in_progress_key(trip:, user:)
    [ "itinerary_generation", "in_progress", trip.id, user.id ]
  end

  def perform(trip_id, user_id)
    trip = Trip.find_by(id: trip_id)
    user = User.find_by(id: user_id)
    return unless trip && user

    payload = build_payload(trip, user)
    payload["generated_at"] = Time.current.iso8601

    Rails.cache.write(
      ItineraryGenerator.cache_key(trip: trip, user: user),
      payload,
      expires_in: CACHE_TTL
    )

    broadcast(trip, user, payload)
  ensure
    # Always release the in-progress marker, including on failure, so a later
    # regeneration is never blocked. The marker TTL is only a safety net.
    Rails.cache.delete(self.class.in_progress_key(trip: trip, user: user)) if trip && user
  end

  private

  def build_payload(trip, user)
    result = ItineraryGenerator.new(trip: trip, user: user).call

    if result.items.any?
      base_payload("ready", items: result.items, rejected: result.rejected)
    elsif result.rejected.any?
      base_payload("unusable", reason: result.unusable_reason, rejected: result.rejected)
    else
      base_payload("empty", reason: result.unusable_reason)
    end
  rescue => e
    Rails.logger.error "[GenerateItineraryJob] Failed for trip #{trip.id}, user #{user.id}: #{e.class}: #{e.message}"
    Rails.logger.error e.backtrace.first(5).join("\n")
    base_payload("error", error: "We couldn't generate suggestions right now. Please try again.")
  end

  def base_payload(status, items: [], rejected: [], reason: nil, error: nil)
    { "status" => status, "items" => items, "rejected" => rejected, "reason" => reason, "error" => error }
  end

  def broadcast(trip, user, payload)
    Turbo::StreamsChannel.broadcast_replace_to(
      [ trip, "itinerary_generation", user.id ],
      target: RESULT_TARGET,
      partial: "itinerary_generations/result",
      locals: { generation: payload, trip: trip }
    )
  rescue => e
    # A failed broadcast must not fail the job: the result is already cached
    # and the user can reload the page to see it.
    Rails.logger.warn "[GenerateItineraryJob] broadcast failed: #{e.class}: #{e.message}"
  end
end
