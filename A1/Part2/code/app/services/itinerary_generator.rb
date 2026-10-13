# frozen_string_literal: true

# Turns a trip's title/dates/description into a short list of suggested
# itinerary items by asking Claude, then validates and normalises everything
# before it is ever shown to - or persisted for - the user.
#
# The service never persists anything. It returns an ItineraryGenerator::Result
# and GenerateItineraryJob caches it; TripItemsBulkImport is the only thing that
# writes accepted items, so AI output goes through exactly the same path as a
# manual import.
class ItineraryGenerator
  MODEL      = "claude-haiku-4-5-20251001"
  MAX_TOKENS = 2048
  MAX_RESULTS = 12

  # Mirrors TripItem's url format validation (app/models/trip_item.rb:28) so the
  # AI boundary never hands the importer a URL the model would reject.
  HTTP_URL_PATTERN = /\Ahttps?:\/\/.+\z/i

  Result = Struct.new(:items, :rejected, :unusable_reason, keyword_init: true)

  SYSTEM_PROMPT = <<~PROMPT
    You are a travel planning assistant. Given a trip's title, dates and notes,
    suggest a small number of specific places and activities to include in the
    itinerary.

    Rules:
    - Only suggest real, specific places or activities that fit the trip's dates and location.
    - Prefer a balanced mix: meals, sights, activities and at most one or two stays/transport legs.
    - Use the "kind" field exactly: stay, eat, do, shop, flight, car, train, ferry, other.
    - Provide dates in ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS) and keep them within the trip's start and end dates.
    - Include a URL only when you are confident it is correct; otherwise omit it.
    - Return at most #{MAX_RESULTS} suggestions.
  PROMPT

  ANTHROPIC_TOOLS = [
    {
      name: "record_itinerary_suggestions",
      description: "Record suggested itinerary items for the trip",
      input_schema: {
        type: "object",
        properties: {
          suggestions: {
            type: "array",
            items: {
              type: "object",
              properties: {
                name:      { type: "string", description: "Name of the place or activity" },
                kind:      { type: "string", enum: TripItem.kinds.keys },
                address:   { type: "string" },
                starts_at: { type: "string", description: "ISO 8601 date or datetime" },
                ends_at:   { type: "string", description: "ISO 8601 date or datetime" },
                url:       { type: "string" },
                notes:     { type: "string", description: "One short sentence explaining the suggestion" }
              },
              required: %w[name kind]
            }
          }
        }
      }
    }
  ].freeze

  # Stable cache identity for a user's generation on a trip, used by the job
  # to store and later read the pending preview.
  def self.cache_key(trip:, user:)
    [ "itinerary_generation", trip.id, user.id ]
  end

  def initialize(trip:, user:, client: nil)
    @trip   = trip
    @user   = user
    @client = client
  end

  def call
    raw        = fetch_suggestions
    normalized = normalize(raw)

    result = Result.new(items: normalized[:items], rejected: normalized[:rejected], unusable_reason: nil)
    result.unusable_reason = "The assistant did not return any usable suggestions." if result.items.empty?
    result
  end

  private

  def client
    @client ||= Anthropic::Client.new
  end

  def fetch_suggestions
    response = client.messages.create(
      model:      MODEL,
      max_tokens: MAX_TOKENS,
      system:     SYSTEM_PROMPT,
      tools:      ANTHROPIC_TOOLS,
      messages:   [ { role: "user", content: build_prompt } ]
    )
    tool_use = response.content.find { |block| block.type == :tool_use }
    tool_use ? Array(tool_use.input.deep_stringify_keys["suggestions"]) : []
  end

  def build_prompt
    parts = []
    parts << "Trip: #{@trip.title}"
    parts << "Dates: #{@trip.start_date} to #{@trip.end_date}"
    parts << "Notes: #{@trip.description}" if @trip.description.present?

    existing = @trip.trip_items.pluck(:name)
    parts << "Already in the itinerary (do not repeat these): #{existing.join(', ')}" if existing.any?

    parts.join("\n")
  end

  # Applies the same rules the manual import enforces, so that an accepted
  # suggestion is always something TripItemsBulkImport can persist.
  def normalize(raw)
    items          = []
    rejected       = []
    seen_names     = @trip.trip_items.pluck(:name).map(&:downcase).to_set

    Array(raw).each do |suggestion|
      suggestion = suggestion.to_h
      name = suggestion["name"].to_s.strip
      if name.blank?
        rejected << { "name" => suggestion["name"].to_s, "reason" => "missing name" }
        next
      end
      if seen_names.include?(name.downcase)
        rejected << { "name" => name, "reason" => "duplicate (already in itinerary)" }
        next
      end

      kind = suggestion["kind"].to_s
      unless TripItem.kinds.key?(kind)
        rejected << { "name" => name, "reason" => "unknown kind" }
        next
      end

      starts_at = parse_within_trip(suggestion["starts_at"])
      ends_at   = parse_within_trip(suggestion["ends_at"])
      if suggestion["starts_at"].present? && starts_at.nil?
        rejected << { "name" => name, "reason" => "date outside trip" }
        next
      end
      if suggestion["ends_at"].present? && ends_at.nil?
        rejected << { "name" => name, "reason" => "date outside trip" }
        next
      end
      if starts_at && ends_at && ends_at < starts_at
        rejected << { "name" => name, "reason" => "ends before start" }
        next
      end

      if items.size >= MAX_RESULTS
        rejected << { "name" => name, "reason" => "over the #{MAX_RESULTS} suggestion limit" }
        next
      end

      seen_names << name.downcase
      items << {
        "name"      => name,
        "kind"      => kind,
        "address"   => suggestion["address"].presence,
        "starts_at" => starts_at&.iso8601,
        "ends_at"   => ends_at&.iso8601,
        "url"       => normalized_url(suggestion["url"]),
        "notes"     => suggestion["notes"].presence
      }
    end

    { items: items, rejected: rejected }
  end

  def parse_within_trip(value)
    return nil if value.blank?

    time = Time.zone.parse(value.to_s)
    return nil unless time

    (time.to_date >= @trip.start_date) && (time.to_date <= @trip.end_date) ? time : nil
  rescue ArgumentError, TypeError
    nil
  end

  # Drops an optional URL the TripItem model would reject, so an invalid URL
  # never causes TripItemsBulkImport to skip an otherwise-valid suggestion.
  def normalized_url(value)
    url = value.to_s.strip
    url.match?(HTTP_URL_PATTERN) ? url : nil
  end
end
