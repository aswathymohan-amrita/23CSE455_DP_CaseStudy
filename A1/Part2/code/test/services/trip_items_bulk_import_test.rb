# frozen_string_literal: true

require "test_helper"

class TripItemsBulkImportTest < ActiveSupport::TestCase
  setup do
    @user     = create_user
    @account, @traveler = create_account(owner: @user)
    @trip     = create_trip(account: @account, created_by: @user)
    add_member(trip: @trip, traveler: @traveler, role: "owner")
  end

  def import(items)
    TripItemsBulkImport.new(trip: @trip, added_by: @user).call(items)
  end

  test "creates valid items as ideas" do
    result = import([
      { "name" => "Colosseum", "kind" => "do", "address" => "Rome, Italy" },
      { "name" => "Pasta Dinner", "kind" => "eat" }
    ])

    assert_equal 2, result[:created]
    assert_equal 0, result[:skipped]
    assert_equal 0, result[:duplicates]

    item = @trip.trip_items.find_by(name: "Colosseum")
    assert_equal "idea", item.status
    assert_equal "do", item.kind
    assert_equal "Rome, Italy", item.address
  end

  test "skips blank names and coerces unknown kinds to other" do
    result = import([
      { "name" => "", "kind" => "eat" },
      { "name" => "Weird Place", "kind" => "banana" }
    ])

    assert_equal 1, result[:created]
    assert_equal 1, result[:skipped]
    assert_equal "other", @trip.trip_items.find_by(name: "Weird Place").kind
  end

  test "skips duplicates case-insensitively and backfills missing geo/url" do
    @trip.trip_items.create!(name: "Old Town", kind: "do", status: "idea", added_by: @user)

    result = import([
      { "name" => "OLD TOWN", "kind" => "do", "lat" => 41.8902, "lng" => 12.4922 }
    ])

    assert_equal 0, result[:created]
    assert_equal 1, result[:duplicates]
    item = @trip.trip_items.find_by("lower(name) = ?", "old town")
    assert_equal 41.8902, item.latitude
    assert_equal 12.4922, item.longitude
  end

  test "queues geocoding for items without coordinates" do
    assert_enqueued_with(job: GeocodeTripItemsJob) do
      import([ { "name" => "Beach", "kind" => "do", "address" => "Nice, France" } ])
    end
  end

  test "does not queue geocoding when every item already has coordinates" do
    assert_no_enqueued_jobs only: GeocodeTripItemsJob do
      import([ { "name" => "Beach", "kind" => "do", "lat" => 43.7102, "lng" => 7.2620 } ])
    end
  end

  test "keeps gecoding callback enabled after import" do
    assert TripItem._save_callbacks.any? { |cb| cb.filter == :geocode_from_address }

    import([ { "name" => "Museum", "kind" => "do", "address" => "Florence, Italy" } ])

    assert TripItem._save_callbacks.any? { |cb| cb.filter == :geocode_from_address }
  end
end
