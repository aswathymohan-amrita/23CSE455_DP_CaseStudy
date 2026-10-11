# frozen_string_literal: true

# Persists externally supplied itinerary item hashes (from the manual JSON
# import or from AI generation) into a trip.
#
# Extracted from TripItemsController#bulk_create_items so the manual import and
# the AI-generated suggestions share exactly one persistence path. Behaviour is
# intentionally identical to the original controller method:
#
#   - blank names are skipped
#   - duplicates (case-insensitive name match) are not re-created
#   - unknown kinds fall back to "other"
#   - new items are always created in the "idea" status
#   - geocoding is deferred to GeocodeTripItemsJob
class TripItemsBulkImport
  VALID_KINDS = TripItem.kinds.keys.to_set

  def initialize(trip:, added_by:)
    @trip = trip
    @added_by = added_by
  end

  def call(items)
    created           = 0
    skipped           = 0
    duplicates        = 0
    needs_geocode_ids = []
    existing_names    = @trip.trip_items.pluck(:name).map(&:downcase).to_set
    TripItem.skip_callback(:save, :after, :geocode_from_address)
    items.each do |data|
      next skipped    += 1 if data["name"].blank?
      if existing_names.include?(data["name"].downcase)
        existing = @trip.trip_items.find_by("lower(name) = ?", data["name"].downcase)
        if existing
          updates = {}
          updates[:latitude]  = data["lat"] if data["lat"].present? && !existing.geocoded?
          updates[:longitude] = data["lng"] if data["lng"].present? && !existing.geocoded?
          updates[:url]       = data["url"] if data["url"].present? && existing.url.blank?
          existing.update_columns(updates) if updates.any?
        end
        next duplicates += 1
      end
      item = @trip.trip_items.create!(
        name:      data["name"],
        kind:      VALID_KINDS.include?(data["kind"].to_s) ? data["kind"].to_s : "other",
        status:    "idea",
        address:   data["address"].presence,
        latitude:  data["lat"].presence,
        longitude: data["lng"].presence,
        notes:     data["notes"].presence,
        url:       data["url"].presence,
        starts_at: parse_time(data["starts_at"]),
        ends_at:   parse_time(data["ends_at"]),
        amount:    data["amount"].presence,
        currency:  data["currency"].presence,
        added_by:  @added_by
      )
      created += 1
      existing_names << item.name.downcase
      needs_geocode_ids << item.id unless item.geocoded?
    rescue => e
      Rails.logger.error "[TripItemsBulkImport] skipped item: #{e.message}"
      skipped += 1
    end
    GeocodeTripItemsJob.perform_later(needs_geocode_ids, @trip.id) if needs_geocode_ids.any?
    { created: created, skipped: skipped, duplicates: duplicates, geocoding_queued: needs_geocode_ids.size }
  ensure
    TripItem.set_callback(:save, :after, :geocode_from_address)
  end

  private

  def parse_time(val)
    Time.zone.parse(val.to_s) if val.present?
  rescue ArgumentError, TypeError
    nil
  end
end
