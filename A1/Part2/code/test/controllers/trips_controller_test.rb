# frozen_string_literal: true

require "test_helper"

class TripsControllerTest < ActionController::TestCase
  include ModernBrowserHelper

  setup do
    @user     = create_user
    @account, @traveler = create_account(owner: @user)
    @trip     = create_trip(account: @account, created_by: @user)
    add_member(trip: @trip, traveler: @traveler, role: "owner")
    session[:user_id] = @user.id
    @request.host = "whats.test"
  end

  test "the owner's trip page renders the generate entry point" do
    get :show, params: { id: @trip.id }

    assert_response :success
    assert_match "Generate", response.body
    assert_match trip_itinerary_generation_path(@trip), response.body
  end
end
