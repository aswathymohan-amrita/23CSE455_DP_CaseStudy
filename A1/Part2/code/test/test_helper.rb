# frozen_string_literal: true

ENV["RAILS_ENV"] ||= "test"
require_relative "../config/environment"
require "rails/test_help"

Dir[Rails.root.join("test/support/**/*.rb")].sort.each { |file| require file }

# Never hit a real geocoding service from tests: the :test lookup returns
# configured stubs (none by default), so items simply stay ungeocoded.
Geocoder.configure(lookup: :test)

module TestDataHelper
  MODERN_UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

  def create_user(name: "Test User", email: "test-#{SecureRandom.hex(4)}@example.com")
    user = User.create!(name: name, email: email)
    user
  end

  def create_account(owner:)
    account = Account.create!(name: "#{owner.name} account", owner: owner)
    traveler = account.travelers.create!(name: owner.name, user: owner)
    [ account, traveler ]
  end

  def create_trip(account:, created_by:, title: "Test Trip",
                  start_date: Date.current, end_date: Date.current + 3)
    account.trips.create!(
      title: title,
      start_date: start_date,
      end_date: end_date,
      created_by: created_by
    )
  end

  def add_member(trip:, traveler:, role: "owner")
    trip.trip_members.create!(traveler: traveler, role: role)
  end
end

module ModernBrowserHelper
  def setup
    super
    @request.user_agent = TestDataHelper::MODERN_UA if defined?(@request) && @request
  end
end

class ActiveSupport::TestCase
  include TestDataHelper
  include ActiveJob::TestHelper

  # Tests run against a single SQLite database in one process.
  self.use_transactional_tests = true

  setup { Rails.cache.clear }
end
