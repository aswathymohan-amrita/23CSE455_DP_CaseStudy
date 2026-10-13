class TripItem < ApplicationRecord
  include Geocodable

  belongs_to :trip
  belongs_to :added_by, class_name: "User"
  belongs_to :inbox_item, optional: true
  has_one :expense, dependent: :nullify

  enum :kind, {
    stay:    "stay",
    eat:     "eat",
    "do":    "do",
    shop:    "shop",
    flight:  "flight",
    car:     "car",
    train:   "train",
    ferry:   "ferry",
    other:   "other"
  }

  enum :status, {
    idea:      "idea",
    confirmed: "confirmed"
  }

  validates :name, presence: true
  validates :kind, presence: true
  validates :url, format: { with: /\Ahttps?:\/\/.+\z/i, message: "must start with http:// or https://" }, allow_blank: true
  validates :provider, length: { maximum: 120 }, allow_blank: true
  validates :cancellation_policy, inclusion: { in: CancellationPolicy.known }, allow_blank: true

  before_validation :normalize_provider
  before_validation :normalize_cancellation_policy

  TRANSPORT_KINDS = %w[flight car train ferry].freeze

  # Don't geocode transport items (car/flight/train/ferry) unless a real address is present.
  # Company names like "Sicily By Car" geocode to wrong locations (company HQ, not trip area).
  def geocode_from_address
    return if TRANSPORT_KINDS.include?(kind.to_s) && address.blank?
    super
  end

  def expense_category
    kind
  end

  # Eligibility/penalty for cancelling at `at`, based on this item's policy.
  # Returns nil when no policy is recorded. Does not cancel or refund anything.
  def cancellation_status(at: Time.current)
    return nil if cancellation_policy.blank?

    CancellationPolicy.evaluate(
      policy: cancellation_policy, free_until: free_cancellation_until, at: at
    )
  end

  def when_label
    return nil unless starts_at
    has_time = starts_at.hour != 0 || starts_at.min != 0
    if ends_at.present?
      if ends_at.to_date != starts_at.to_date
        "#{starts_at.strftime("%-d %b")} – #{ends_at.strftime("%-d %b %Y")}"
      else
        has_time ? "#{starts_at.strftime("%-d %b · %H:%M")} – #{ends_at.strftime("%H:%M")}" : starts_at.strftime("%-d %b %Y")
      end
    else
      has_time ? starts_at.strftime("%-d %b %Y · %H:%M") : starts_at.strftime("%-d %b %Y")
    end
  end

  private

  # Provider is only meaningful for bookings, but normalizing it here keeps a
  # single canonical value whether it arrives from an email, the manual form
  # or a console/import path. Non-bookings simply normalize to nil.
  def normalize_provider
    self.provider = BookingProvider.normalize(provider)
  end

  def normalize_cancellation_policy
    self.cancellation_policy = CancellationPolicy.normalize(cancellation_policy)
  end
end
