# Normalizes free-text booking provider names (from parsed confirmation emails
# or manual entry) to a canonical label. This lets the app recognise that two
# bookings came from the same provider even when the provider was spelled
# differently ("booking.com", "Booking", "BOOKING.COM").
#
# Unknown providers are preserved verbatim rather than discarded, so bookings
# from providers outside the curated list still keep a usable provider name.
module BookingProvider
  # Canonical display name => accepted spellings (matched case-insensitively).
  KNOWN = {
    "Booking.com"       => %w[booking booking.com bookingcom],
    "Airbnb"            => %w[airbnb],
    "Expedia"           => %w[expedia expedia.com],
    "Hotels.com"        => %w[hotels hotels.com hotelscom],
    "Agoda"             => %w[agoda],
    "Trip.com"          => %w[trip.com tripcom],
    "Vrbo"              => %w[vrbo homeaway],
    "Viator"            => %w[viator],
    "GetYourGuide"      => %w[getyourguide getyourguide.com],
    "Klook"             => %w[klook],
    "OpenTable"         => [ "opentable", "open table" ],
    "Rentalcars"        => %w[rentalcars rentalcars.com],
    "Hertz"             => %w[hertz],
    "Avis"              => %w[avis],
    "Sixt"              => %w[sixt],
    "Uber"              => %w[uber],
    "Trainline"         => %w[trainline thetrainline.com],
    "FlixBus"           => %w[flixbus flix],
    "Ryanair"           => %w[ryanair],
    "Delta"             => [ "delta", "delta air lines" ],
    "American Airlines" => [ "american airlines", "americanairlines", "aa" ]
  }.freeze

  LOOKUP = KNOWN.each_with_object({}) do |(canonical, spellings), index|
    spellings.each { |spelling| index[spelling] = canonical }
  end.freeze

  # Canonical provider names available for suggestions in the UI.
  def self.known
    KNOWN.keys
  end

  # Returns the canonical provider name, or nil when the input is blank.
  # Unknown providers are returned trimmed and untouched.
  def self.normalize(raw)
    value = raw.to_s.strip
    return nil if value.empty?

    LOOKUP[value.downcase.gsub(/\s+/, " ")] || value
  end
end
