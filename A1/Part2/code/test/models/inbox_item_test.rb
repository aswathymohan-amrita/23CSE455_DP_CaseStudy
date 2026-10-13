# frozen_string_literal: true

require "test_helper"

# Covers the booking branch of InboxItem#fill_missing_links!: provider is kept
# as a normalised field and bookings made through the same provider no longer
# collapse onto a single trip item.
class InboxItemTest < ActiveSupport::TestCase
  setup do
    @user     = create_user
    @account, @traveler = create_account(owner: @user)
    @trip     = create_trip(account: @account, created_by: @user)
    add_member(trip: @trip, traveler: @traveler, role: "owner")
  end

  def inbox_with(bookings)
    @trip.inbox_items.create!(
      from_email:  "bookings@example.com",
      received_at: Time.current,
      parsed_data: { "bookings" => bookings }
    )
  end

  test "stores a canonical provider and a distinguishing name on booking items" do
    inbox = inbox_with([
      { "provider" => "booking.com", "booking_type" => "tour", "location" => "Colosseum" }
    ])

    inbox.fill_missing_links!(@user)

    item = @trip.trip_items.find_by(kind: "do")
    assert_equal "Booking.com", item.provider
    assert_equal "Booking.com Tour - Colosseum", item.name
  end

  test "multiple bookings from the same provider do not collapse" do
    inbox = inbox_with([
      { "provider" => "viator", "booking_type" => "tour", "location" => "Colosseum" },
      { "provider" => "Viator", "booking_type" => "tour", "location" => "Vatican Museums" }
    ])

    assert_difference -> { @trip.trip_items.count }, 2 do
      inbox.fill_missing_links!(@user)
    end

    assert_equal [ "Viator", "Viator" ], @trip.trip_items.where(kind: "do").pluck(:provider).sort
  end

  test "is idempotent when the same booking is processed twice" do
    inbox = inbox_with([
      { "provider" => "Viator", "booking_type" => "tour", "location" => "Colosseum" }
    ])

    inbox.fill_missing_links!(@user)

    assert_no_difference -> { @trip.trip_items.count } do
      inbox.fill_missing_links!(@user)
    end
  end

  test "keeps a booking that has a blank provider" do
    inbox = inbox_with([
      { "provider" => "", "booking_type" => "car rental", "location" => "Fiumicino" }
    ])

    inbox.fill_missing_links!(@user)

    item = @trip.trip_items.find_by(kind: "car")
    assert_nil item.provider
    assert_equal "Car rental - Fiumicino", item.name
  end
end
