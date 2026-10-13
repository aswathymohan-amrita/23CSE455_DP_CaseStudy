class AddProviderToTripItems < ActiveRecord::Migration[8.1]
  def change
    add_column :trip_items, :provider, :string
  end
end
