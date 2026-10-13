class AddCancellationPolicyToTripItems < ActiveRecord::Migration[8.1]
  def change
    add_column :trip_items, :cancellation_policy, :string
    add_column :trip_items, :free_cancellation_until, :datetime
  end
end
