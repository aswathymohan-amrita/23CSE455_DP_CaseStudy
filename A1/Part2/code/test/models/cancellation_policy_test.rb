# frozen_string_literal: true

require "test_helper"

class CancellationPolicyTest < ActiveSupport::TestCase
  DEADLINE = Time.zone.parse("2026-05-08 12:00")

  test "flexible policy is free up to and including the deadline, then fully penalised" do
    before  = CancellationPolicy.evaluate(policy: "flexible", free_until: DEADLINE, at: Time.zone.parse("2026-05-08 11:59"))
    exactly = CancellationPolicy.evaluate(policy: "flexible", free_until: DEADLINE, at: DEADLINE)
    after   = CancellationPolicy.evaluate(policy: "flexible", free_until: DEADLINE, at: Time.zone.parse("2026-05-08 12:01"))

    assert before.free?
    assert exactly.free?
    assert_not after.free?
    assert_equal 100, after.penalty_percent
    assert_equal 0, after.refund_percent
  end

  test "moderate policy keeps a partial refund after the deadline" do
    after = CancellationPolicy.evaluate(policy: "moderate", free_until: DEADLINE, at: Time.zone.parse("2026-05-09 09:00"))

    assert_not after.free?
    assert_equal 50, after.penalty_percent
    assert_equal 50, after.refund_percent
  end

  test "non-refundable policy is never free, even before any deadline" do
    result = CancellationPolicy.evaluate(policy: "non_refundable", free_until: DEADLINE, at: Time.zone.parse("2026-01-01"))

    assert_not result.free?
    assert_equal 100, result.penalty_percent
  end

  test "a flexible policy without a deadline is not free" do
    result = CancellationPolicy.evaluate(policy: "flexible", free_until: nil, at: Time.zone.now)

    assert_not result.free?
    assert_equal 100, result.penalty_percent
  end

  test "raises for an unsupported policy" do
    assert_raises(ArgumentError) do
      CancellationPolicy.evaluate(policy: "banana", free_until: nil, at: Time.zone.now)
    end
  end

  test "normalizes common spellings and labels known policies" do
    assert_equal "non_refundable", CancellationPolicy.normalize("Non-refundable")
    assert_equal "flexible", CancellationPolicy.normalize("  Flexible ")
    assert_nil CancellationPolicy.normalize("  ")
    assert_equal "Moderate", CancellationPolicy.label_for("moderate")
  end
end
