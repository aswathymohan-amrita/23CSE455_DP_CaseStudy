# frozen_string_literal: true

require "test_helper"

# Regression coverage for the import flow after it was extracted into
# TripItemsBulkImport.
class TripItemsControllerTest < ActionController::TestCase
  include ModernBrowserHelper

  setup do
    @user     = create_user
    @account, @traveler = create_account(owner: @user)
    @trip     = create_trip(account: @account, created_by: @user)
    add_member(trip: @trip, traveler: @traveler, role: "owner")
    session[:user_id] = @user.id
    @request.host = "whats.test"
  end

  test "confirming an import persists items" do
    json = JSON.dump([ { "name" => "Colosseum", "kind" => "do" } ])

    assert_difference -> { @trip.trip_items.count }, 1 do
      post :import, params: { trip_id: @trip.id, confirm: "1", items_json: json }
    end

    assert_redirected_to trip_path(@trip, tab: "itinerary")
    assert_equal "Colosseum", @trip.trip_items.last.name
  end

  test "import preview parses pasted JSON" do
    json = JSON.dump([ { "name" => "Beach", "kind" => "do" } ])

    post :import, params: { trip_id: @trip.id, items_json: json }

    assert_response :success
    assert_match "Beach", response.body
  end

  test "creates an item with a booking provider, normalized" do
    post :create, params: {
      trip_id: @trip.id,
      trip_item: { name: "Sailing", kind: "do", provider: "getyourguide" }
    }

    assert_redirected_to trip_path(@trip, tab: "itinerary")
    assert_equal "GetYourGuide", @trip.trip_items.find_by(name: "Sailing").provider
  end

  test "rejects an over-long booking provider" do
    post :create, params: {
      trip_id: @trip.id,
      trip_item: { name: "Sailing", kind: "do", provider: "a" * 121 }
    }

    assert_response :unprocessable_entity
  end

  test "shows the booking provider on the item page" do
    item = @trip.trip_items.create!(name: "Tour", kind: "do", added_by: @user, provider: "Viator")

    get :show, params: { trip_id: @trip.id, id: item.id }

    assert_response :success
    assert_match "Booked via", response.body
    assert_match "Viator", response.body
  end

  test "creates an item with a cancellation policy and deadline" do
    post :create, params: {
      trip_id: @trip.id,
      trip_item: {
        name: "Hotel", kind: "stay",
        cancellation_policy: "flexible",
        free_cancellation_until: "2026-05-08T12:00"
      }
    }

    assert_redirected_to trip_path(@trip, tab: "itinerary")
    item = @trip.trip_items.find_by(name: "Hotel")
    assert_equal "flexible", item.cancellation_policy
    assert_equal Time.zone.parse("2026-05-08 12:00"), item.free_cancellation_until
  end

  test "rejects an unsupported cancellation policy" do
    post :create, params: {
      trip_id: @trip.id,
      trip_item: { name: "Hotel", kind: "stay", cancellation_policy: "banana" }
    }

    assert_response :unprocessable_entity
  end

  test "shows the cancellation policy on the item page" do
    item = @trip.trip_items.create!(name: "Hotel", kind: "stay", added_by: @user, cancellation_policy: "non_refundable")

    get :show, params: { trip_id: @trip.id, id: item.id }

    assert_response :success
    assert_match "Cancellation", response.body
    assert_match "Non-refundable", response.body
  end

  test "a non-member cannot import into someone else's trip" do
    other_user = create_user(name: "Other")
    o_account, o_traveler = create_account(owner: other_user)
    other_trip = create_trip(account: o_account, created_by: other_user)
    add_member(trip: other_trip, traveler: o_traveler, role: "owner")

    assert_raises(ActiveRecord::RecordNotFound) do
      post :import, params: { trip_id: other_trip.id, confirm: "1", items_json: "[]" }
    end
  end
end
