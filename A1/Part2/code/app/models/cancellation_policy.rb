# Cancellation terms for a booking, kept as a small curated set rather than a
# database table. A policy decides whether cancelling at a given moment is free,
# and how much of the booking price is kept as a penalty once the free window
# has passed.
#
# This only evaluates eligibility/penalty. It never cancels a booking and never
# moves money; no refund is performed anywhere in the application.
module CancellationPolicy
  # key => rule. late_penalty_percent is applied once the deadline has passed.
  POLICIES = {
    "flexible"       => { label: "Flexible",       free_until_deadline: true,  late_penalty_percent: 100 },
    "moderate"       => { label: "Moderate",       free_until_deadline: true,  late_penalty_percent: 50 },
    "non_refundable" => { label: "Non-refundable", free_until_deadline: false, late_penalty_percent: 100 }
  }.freeze

  Result = Struct.new(:policy, :free, :refund_percent, :penalty_percent, keyword_init: true) do
    def free?
      free
    end
  end

  # Canonical policy keys available for selection.
  def self.known
    POLICIES.keys
  end

  def self.label_for(policy)
    POLICIES.dig(policy.to_s.strip.downcase, :label) || policy.to_s.humanize
  end

  # Accepts common spellings ("Non-refundable", "non refundable") and returns the
  # canonical key. Unknown values are returned cleaned so model validation can
  # reject them rather than silently discarding them.
  def self.normalize(raw)
    value = raw.to_s.strip.downcase.gsub(/[\s-]+/, "_")
    value.presence
  end

  # Evaluates a policy at `at`. Raises ArgumentError for an unsupported policy so
  # callers cannot silently apply the wrong rule.
  def self.evaluate(policy:, free_until:, at:)
    key  = normalize(policy)
    rule = POLICIES[key]
    raise ArgumentError, "unknown cancellation policy: #{policy.inspect}" unless rule

    free    = rule[:free_until_deadline] && free_until.present? && at <= free_until
    penalty = free ? 0 : rule[:late_penalty_percent]

    Result.new(policy: key, free: free, refund_percent: 100 - penalty, penalty_percent: penalty)
  end
end
