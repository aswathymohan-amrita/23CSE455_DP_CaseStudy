# frozen_string_literal: true

require "test_helper"

class ItineraryGenerationsControllerTest < ActionController::TestCase
  include ModernBrowserHelper

  setup do
    @user     = create_user
    @account, @traveler = create_account(owner: @user)
    @trip     = create_trip(account: @account, created_by: @user)
    add_member(trip: @trip, traveler: @traveler, role: "owner")
    session[:user_id] = @user.id
    @request.host = "whats.test"
  end

  def cache_ready_generation(items = [ { "name" => "Colosseum", "kind" => "do" } ])
    Rails.cache.write(
      ItineraryGenerator.cache_key(trip: @trip, user: @user),
      { "status" => "ready", "items" => items, "rejected" => [], "reason" => nil, "error" => nil }
    )
  end

  def cache_generation(payload)
    Rails.cache.write(ItineraryGenerator.cache_key(trip: @trip, user: @user), payload)
  end

  test "create enqueues the job and renders the preview page" do
    assert_enqueued_with(job: GenerateItineraryJob, args: [ @trip.id, @user.id ]) do
      post :create, params: { trip_id: @trip.id }
    end

    assert_response :success
    assert_select "div#itinerary-generation-result"
  end

  test "repeated submissions while a generation is running do not enqueue again" do
    assert_enqueued_jobs 1, only: GenerateItineraryJob do
      post :create, params: { trip_id: @trip.id }
      post :create, params: { trip_id: @trip.id }
    end

    assert_response :success
  end

  test "regeneration is allowed once a generation has finished" do
    GenerateItineraryJob.enqueue_unless_running(trip: @trip, user: @user)
    clear_enqueued_jobs

    fake = FakeAnthropic.client(suggestions: [ { "name" => "Colosseum", "kind" => "do" } ])
    Anthropic::Client.stub(:new, fake) do
      GenerateItineraryJob.perform_now(@trip.id, @user.id)
    end

    assert_enqueued_with(job: GenerateItineraryJob, args: [ @trip.id, @user.id ]) do
      post :create, params: { trip_id: @trip.id }
    end

    assert_response :success
  end

  test "show renders the cached results" do
    cache_ready_generation

    get :show, params: { trip_id: @trip.id }

    assert_response :success
    assert_match "Colosseum", response.body
  end

  test "show renders the error state" do
    cache_generation("status" => "error", "items" => [], "rejected" => [],
                     "reason" => nil, "error" => "We couldn't generate suggestions right now.")

    get :show, params: { trip_id: @trip.id }

    assert_response :success
    assert_match "Something went wrong", response.body
  end

  test "show renders the unusable state with rejection reasons" do
    cache_generation("status" => "unusable", "items" => [],
                     "rejected" => [ { "name" => "Bad Place", "reason" => "unknown kind" } ],
                     "reason" => "No usable suggestions.", "error" => nil)

    get :show, params: { trip_id: @trip.id }

    assert_response :success
    assert_match "unknown kind", response.body
  end

  test "confirm persists cached suggestions through the bulk importer" do
    cache_ready_generation

    assert_difference -> { @trip.trip_items.count }, 1 do
      post :confirm, params: { trip_id: @trip.id }
    end

    assert_redirected_to trip_path(@trip, tab: "itinerary")
    assert_equal "Colosseum", @trip.trip_items.last.name
    assert_nil Rails.cache.read(ItineraryGenerator.cache_key(trip: @trip, user: @user))
  end

  test "confirm redirects with an alert when there are no cached suggestions" do
    post :confirm, params: { trip_id: @trip.id }

    assert_redirected_to trip_path(@trip, tab: "itinerary")
    assert_equal "Those suggestions have expired. Please generate them again.", flash[:alert]
    assert_equal 0, @trip.trip_items.count
  end

  test "non-members are not authorized" do
    stranger     = create_user(name: "Stranger")
    @account, @traveler = create_account(owner: stranger)
    session[:user_id] = stranger.id

    post :create, params: { trip_id: @trip.id }

    assert_redirected_to trips_path
    assert_equal "You don't have permission to do that.", flash[:alert]
  end

  test "viewers are not authorized" do
    viewer     = create_user(name: "Viewer")
    _v_account, v_traveler = create_account(owner: viewer)
    add_member(trip: @trip, traveler: v_traveler, role: "viewer")
    session[:user_id] = viewer.id

    get :show, params: { trip_id: @trip.id }

    assert_redirected_to trips_path
    assert_equal "You don't have permission to do that.", flash[:alert]
  end
end
