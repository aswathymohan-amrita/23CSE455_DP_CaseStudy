# frozen_string_literal: true

require "test_helper"

class ItineraryGeneratorTest < ActiveSupport::TestCase
  setup do
    @user     = create_user
    @account, @traveler = create_account(owner: @user)
    @trip     = create_trip(account: @account, created_by: @user,
                            start_date: Date.new(2026, 5, 1),
                            end_date: Date.new(2026, 5, 10))
    add_member(trip: @trip, traveler: @traveler, role: "owner")
    @trip.trip_items.create!(name: "Old Town", kind: "do", status: "idea", added_by: @user)
  end

  test "generates and normalizes suggestions" do
    fake = FakeAnthropic.client(suggestions: [
      { "name" => "Colosseum", "kind" => "do", "starts_at" => "2026-05-02", "notes" => "Ancient amphitheatre" }
    ])

    result = ItineraryGenerator.new(trip: @trip, user: @user, client: fake).call

    assert result.items.any?
    item = result.items.first
    assert_equal "Colosseum", item["name"]
    assert_equal "do", item["kind"]
    assert_equal "Ancient amphitheatre", item["notes"]
    assert_equal Date.new(2026, 5, 2), Time.zone.parse(item["starts_at"]).to_date
  end

  test "rejects unknown kinds, out-of-range dates, duplicates and blanks" do
    fake = FakeAnthropic.client(suggestions: [
      { "name" => "Bad Kind", "kind" => "banana" },
      { "name" => "Too Late", "kind" => "do", "starts_at" => "2026-06-01" },
      { "name" => "Old Town", "kind" => "do" },
      { "name" => "", "kind" => "do" },
      { "name" => "Valid Spot", "kind" => "eat" }
    ])

    result = ItineraryGenerator.new(trip: @trip, user: @user, client: fake).call

    assert_equal [ "Valid Spot" ], result.items.map { |i| i["name"] }
    assert_equal 4, result.rejected.size
    assert result.unusable_reason.blank?, "usable results must not carry a reason"
  end

  test "rejects an end date outside the trip range" do
    fake = FakeAnthropic.client(suggestions: [
      { "name" => "Too Long", "kind" => "do", "starts_at" => "2026-05-02", "ends_at" => "2026-06-01" }
    ])

    result = ItineraryGenerator.new(trip: @trip, user: @user, client: fake).call

    assert_empty result.items
    assert_equal 1, result.rejected.size
    assert_equal "Too Long", result.rejected.first["name"]
    assert_equal "date outside trip", result.rejected.first["reason"]
  end

  test "rejects an end date earlier than the start date" do
    fake = FakeAnthropic.client(suggestions: [
      { "name" => "Backwards", "kind" => "do", "starts_at" => "2026-05-05", "ends_at" => "2026-05-03" }
    ])

    result = ItineraryGenerator.new(trip: @trip, user: @user, client: fake).call

    assert_empty result.items
    assert_equal [ "Backwards" ], result.rejected.map { |r| r["name"] }
    assert_equal "ends before start", result.rejected.first["reason"]
  end

  test "accepts a suggestion whose start and end timestamps are equal" do
    fake = FakeAnthropic.client(suggestions: [
      { "name" => "Punctual", "kind" => "do",
        "starts_at" => "2026-05-05T10:00:00", "ends_at" => "2026-05-05T10:00:00" }
    ])

    result = ItineraryGenerator.new(trip: @trip, user: @user, client: fake).call

    assert_equal [ "Punctual" ], result.items.map { |i| i["name"] }
    assert_equal result.items.first["starts_at"], result.items.first["ends_at"]
    assert_empty result.rejected
  end

  test "accepts suggestions with missing optional dates" do
    fake = FakeAnthropic.client(suggestions: [
      { "name" => "No Dates", "kind" => "do" },
      { "name" => "Only Start", "kind" => "eat", "starts_at" => "2026-05-04" }
    ])

    result = ItineraryGenerator.new(trip: @trip, user: @user, client: fake).call

    assert_equal [ "No Dates", "Only Start" ], result.items.map { |i| i["name"] }
    assert_nil result.items[0]["starts_at"]
    assert_nil result.items[0]["ends_at"]
    assert_nil result.items[1]["ends_at"]
    assert_empty result.rejected
  end

  test "keeps a valid http(s) URL on an accepted suggestion" do
    fake = FakeAnthropic.client(suggestions: [
      { "name" => "Museum", "kind" => "do", "url" => "https://example.com/museum" }
    ])

    result = ItineraryGenerator.new(trip: @trip, user: @user, client: fake).call

    assert_equal [ "Museum" ], result.items.map { |i| i["name"] }
    assert_equal "https://example.com/museum", result.items.first["url"]
  end

  test "normalizes an invalid URL to nil without discarding the suggestion" do
    fake = FakeAnthropic.client(suggestions: [
      { "name" => "Mystery Spot", "kind" => "do", "address" => "Rome, Italy", "url" => "not-a-url" }
    ])

    result = ItineraryGenerator.new(trip: @trip, user: @user, client: fake).call

    assert_equal [ "Mystery Spot" ], result.items.map { |i| i["name"] }
    item = result.items.first
    assert_nil item["url"]
    assert_equal "Rome, Italy", item["address"]
    assert_empty result.rejected
  end

  test "accepts missing or blank URLs" do
    fake = FakeAnthropic.client(suggestions: [
      { "name" => "No URL", "kind" => "do" },
      { "name" => "Blank URL", "kind" => "eat", "url" => "   " }
    ])

    result = ItineraryGenerator.new(trip: @trip, user: @user, client: fake).call

    assert_equal [ "No URL", "Blank URL" ], result.items.map { |i| i["name"] }
    assert result.items.all? { |i| i["url"].nil? }
    assert_empty result.rejected
  end

  test "an invalid AI URL does not discard the suggestion when it is persisted" do
    fake = FakeAnthropic.client(suggestions: [
      { "name" => "Hidden Gem", "kind" => "do", "url" => "www.example.com" }
    ])

    result = ItineraryGenerator.new(trip: @trip, user: @user, client: fake).call
    import = TripItemsBulkImport.new(trip: @trip, added_by: @user).call(result.items)

    assert_equal 1, import[:created]
    item = @trip.trip_items.find_by(name: "Hidden Gem")
    assert_not_nil item
    assert_nil item.url
  end

  test "never returns more than MAX_RESULTS items" do
    suggestions = (1..15).map { |n| { "name" => "Place #{n}", "kind" => "do" } }
    fake = FakeAnthropic.client(suggestions: suggestions)

    result = ItineraryGenerator.new(trip: @trip, user: @user, client: fake).call

    assert_equal ItineraryGenerator::MAX_RESULTS, result.items.size
    assert_equal 3, result.rejected.size
  end

  test "returns an unusable reason when the assistant returns nothing" do
    fake = FakeAnthropic.client(suggestions: [])

    result = ItineraryGenerator.new(trip: @trip, user: @user, client: fake).call

    assert_empty result.items
    assert result.unusable_reason.present?
  end

  test "cache_key is stable per trip and user" do
    assert_equal [ "itinerary_generation", @trip.id, @user.id ],
                 ItineraryGenerator.cache_key(trip: @trip, user: @user)
  end
end
