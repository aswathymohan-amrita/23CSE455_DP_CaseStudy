# frozen_string_literal: true

# Shared authorization for controllers that scope a trip to the current user
# as an owner or planner (i.e. a member allowed to edit the trip).
#
# Extracted from TripsController#set_editable_trip so the new itinerary
# generation controller enforces the exact same access rules.
module EditableTripScoped
  extend ActiveSupport::Concern

  private

  def set_editable_trip
    @trip = Trip.joins(trip_members: :traveler)
                .where(travelers: { user_id: current_user.id })
                .where(trip_members: { role: [ "owner", "planner" ] })
                .find(params[:trip_id] || params[:id])
  rescue ActiveRecord::RecordNotFound
    redirect_to trips_path, alert: "You don't have permission to do that."
  end
end
