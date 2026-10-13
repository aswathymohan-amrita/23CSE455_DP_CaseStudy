# frozen_string_literal: true

require "test_helper"

class BookingProviderTest < ActiveSupport::TestCase
  test "normalizes known provider spellings to a canonical name" do
    assert_equal "Booking.com", BookingProvider.normalize("booking.com")
    assert_equal "Booking.com", BookingProvider.normalize("Booking")
    assert_equal "Booking.com", BookingProvider.normalize("  BOOKING.COM ")
    assert_equal "OpenTable",   BookingProvider.normalize("open table")
  end

  test "preserves unknown providers verbatim" do
    assert_equal "Local Tour Co", BookingProvider.normalize("  Local Tour Co ")
  end

  test "returns nil for blank input" do
    assert_nil BookingProvider.normalize(nil)
    assert_nil BookingProvider.normalize("   ")
  end

  test "exposes unique canonical provider names" do
    assert_includes BookingProvider.known, "Viator"
    assert_equal BookingProvider.known.uniq, BookingProvider.known
  end
end
