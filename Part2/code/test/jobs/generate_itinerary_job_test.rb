# frozen_string_literal: true

require "test_helper"

class GenerateItineraryJobTest < ActiveSupport::TestCase
  setup do
    @user     = create_user
    @account, @traveler = create_account(owner: @user)
    @trip     = create_trip(account: @account, created_by: @user)
    add_member(trip: @trip, traveler: @traveler, role: "owner")
  end

  def payload
    Rails.cache.read(ItineraryGenerator.cache_key(trip: @trip, user: @user))
  end

  test "enqueue_unless_running enqueues at most one job while one is in progress" do
    assert_enqueued_jobs 1, only: GenerateItineraryJob do
      assert GenerateItineraryJob.enqueue_unless_running(trip: @trip, user: @user)
      assert_not GenerateItineraryJob.enqueue_unless_running(trip: @trip, user: @user)
    end
  end

  test "clears the in-progress marker when it finishes" do
    key = GenerateItineraryJob.in_progress_key(trip: @trip, user: @user)
    Rails.cache.write(key, true)

    fake = FakeAnthropic.client(suggestions: [ { "name" => "Colosseum", "kind" => "do" } ])
    Anthropic::Client.stub(:new, fake) do
      GenerateItineraryJob.perform_now(@trip.id, @user.id)
    end

    assert_nil Rails.cache.read(key)
  end

  test "caches a ready payload when suggestions are usable" do
    fake = FakeAnthropic.client(suggestions: [ { "name" => "Colosseum", "kind" => "do" } ])

    Anthropic::Client.stub(:new, fake) do
      GenerateItineraryJob.perform_now(@trip.id, @user.id)
    end

    assert_equal "ready", payload["status"]
    assert_equal [ "Colosseum" ], payload["items"].map { |i| i["name"] }
    assert_equal 1, fake.messages.create_calls.size
  end

  test "broadcasts the result into the trip's per-user stream" do
    fake = FakeAnthropic.client(suggestions: [ { "name" => "Colosseum", "kind" => "do" } ])
    calls = []

    Turbo::StreamsChannel.stub(:broadcast_replace_to, ->(*args, **kwargs) { calls << [ args, kwargs ] }) do
      Anthropic::Client.stub(:new, fake) do
        GenerateItineraryJob.perform_now(@trip.id, @user.id)
      end
    end

    assert_equal 1, calls.size
    args, kwargs = calls.first
    assert_equal [ @trip, "itinerary_generation", @user.id ], args.first
    assert_equal "itinerary-generation-result", kwargs[:target]
    assert_equal "itinerary_generations/result", kwargs[:partial]
  end

  test "caches an unusable payload when everything was rejected" do
    fake = FakeAnthropic.client(suggestions: [ { "name" => "Nope", "kind" => "banana" } ])

    Anthropic::Client.stub(:new, fake) do
      GenerateItineraryJob.perform_now(@trip.id, @user.id)
    end

    assert_equal "unusable", payload["status"]
    assert payload["reason"].present?
  end

  test "caches an empty payload when the assistant returns nothing at all" do
    fake = FakeAnthropic.client(suggestions: [])

    Anthropic::Client.stub(:new, fake) do
      GenerateItineraryJob.perform_now(@trip.id, @user.id)
    end

    assert_equal "empty", payload["status"]
  end

  test "caches an error payload instead of raising when the API fails" do
    Anthropic::Client.stub(:new, FakeAnthropic::FailingClient.new) do
      GenerateItineraryJob.perform_now(@trip.id, @user.id)
    end

    assert_equal "error", payload["status"]
    assert payload["error"].present?
  end

  test "returns quietly and writes nothing when the trip or user is missing" do
    GenerateItineraryJob.perform_now("missing-trip", @user.id)

    assert_nil payload
  end
end
