# frozen_string_literal: true

# Generates AI itinerary suggestions for a trip, shows a preview, and only
# persists them into the itinerary on explicit confirmation.
class ItineraryGenerationsController < ApplicationController
  include EditableTripScoped

  before_action :authenticate_user!
  before_action :set_editable_trip

  def create
    GenerateItineraryJob.enqueue_unless_running(trip: @trip, user: current_user)
    @generation = pending_generation
    render :show
  end

  def show
    @generation = pending_generation
  end

  def confirm
    generation = pending_generation
    unless generation && generation["status"] == "ready" && generation["items"].present?
      redirect_to trip_path(@trip, tab: "itinerary"),
                  alert: "Those suggestions have expired. Please generate them again."
      return
    end

    result = TripItemsBulkImport.new(trip: @trip, added_by: current_user).call(generation["items"])
    msg    = "#{result[:created]} idea(s) added from suggestions."
    msg   += " #{result[:duplicates]} skipped (already in itinerary)." if result[:duplicates] > 0
    msg   += " #{result[:skipped]} skipped." if result[:skipped] > 0

    Rails.cache.delete(ItineraryGenerator.cache_key(trip: @trip, user: current_user))
    redirect_to trip_path(@trip, tab: "itinerary"), notice: msg
  end

  private

  def pending_generation
    Rails.cache.read(ItineraryGenerator.cache_key(trip: @trip, user: current_user))
  end
end
