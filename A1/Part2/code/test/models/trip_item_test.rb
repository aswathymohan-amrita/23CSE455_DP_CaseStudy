# frozen_string_literal: true

require "test_helper"

class TripItemTest < ActiveSupport::TestCase
  setup do
    @user = create_user
    @account, @traveler = create_account(owner: @user)
    @trip = create_trip(account: @account, created_by: @user)
    add_member(trip: @trip, traveler: @traveler, role: "owner")
  end

  test "normalizes a cancellation policy on save" do
    item = @trip.trip_items.create!(
      name: "Hotel", kind: "stay", added_by: @user, cancellation_policy: "Non-refundable"
    )

    assert_equal "non_refundable", item.cancellation_policy
  end

  test "rejects an unsupported cancellation policy" do
    item = @trip.trip_items.new(name: "Hotel", kind: "stay", added_by: @user, cancellation_policy: "banana")

    assert_not item.valid?
    assert item.errors[:cancellation_policy].any?
  end

  test "returns nil cancellation status when no policy is recorded" do
    item = @trip.trip_items.create!(name: "Idea", kind: "do", added_by: @user)

    assert_nil item.cancellation_status
  end

  test "evaluates the recorded policy at a given time and coexists with provider" do
    item = @trip.trip_items.create!(
      name: "Tour", kind: "do", added_by: @user,
      provider: "viator", cancellation_policy: "moderate",
      free_cancellation_until: Time.zone.parse("2026-05-08 12:00")
    )

    assert_equal "Viator", item.provider

    assert item.cancellation_status(at: Time.zone.parse("2026-05-01")).free?

    after = item.cancellation_status(at: Time.zone.parse("2026-05-10"))
    assert_not after.free?
    assert_equal 50, after.penalty_percent
  end
end
