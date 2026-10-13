// Component Interface
interface MenuItem {
    String getDescription();
    double getCost();
    String getPrepNotes();
}

// Concrete Component
class BaseBurger implements MenuItem {
    public String getDescription() { return "Classic Angus Burger"; }
    public double getCost() { return 12.00; }
    public String getPrepNotes() { return "Grill beef patty medium"; }
}

// Base Decorator
abstract class MenuItemDecorator implements MenuItem {
    protected MenuItem item;
    public MenuItemDecorator(MenuItem item) { this.item = item; }
    public String getDescription() { return item.getDescription(); }
    public double getCost() { return item.getCost(); }
    public String getPrepNotes() { return item.getPrepNotes(); }
}

// Concrete Decorator 1: Cheese
class ExtraCheeseDecorator extends MenuItemDecorator {
    public ExtraCheeseDecorator(MenuItem item) { super(item); }
    public String getDescription() { return item.getDescription() + " + Extra Cheddar"; }
    public double getCost() { return item.getCost() + 2.00; }
    public String getPrepNotes() { return item.getPrepNotes() + " | Melt double aged cheddar"; }
}

// Concrete Decorator 2: Bacon
class CrispyBaconDecorator extends MenuItemDecorator {
    public CrispyBaconDecorator(MenuItem item) { super(item); }
    public String getDescription() { return item.getDescription() + " + Smoked Bacon"; }
    public double getCost() { return item.getCost() + 3.00; }
    public String getPrepNotes() { return item.getPrepNotes() + " | Add two strips crispy bacon"; }
}

// Concrete Decorator 3: Gluten Free
class GlutenFreeDecorator extends MenuItemDecorator {
    public GlutenFreeDecorator(MenuItem item) { super(item); }
    public String getDescription() { return item.getDescription() + " (Gluten-Free Bun)"; }
    public double getCost() { return item.getCost() + 1.50; }
    public String getPrepNotes() { return item.getPrepNotes() + " | Use dedicated allergen-safe toaster"; }
}

public class DecoratorDemo {
    public static void main(String[] args) {
        MenuItem simpleBurger = new BaseBurger();
        System.out.println("Test 1 - Base Burger: $" + String.format("%.2f", simpleBurger.getCost()) + " -> " + simpleBurger.getDescription());

        MenuItem loadedBurger = new CrispyBaconDecorator(new ExtraCheeseDecorator(new BaseBurger()));
        System.out.println("Test 2 - Loaded Burger: $" + String.format("%.2f", loadedBurger.getCost()) + " -> " + loadedBurger.getDescription());
        System.out.println("  Kitchen prep notes: " + loadedBurger.getPrepNotes());

        MenuItem allergyBurger = new GlutenFreeDecorator(new ExtraCheeseDecorator(new BaseBurger()));
        System.out.println("Test 3 - GF Burger: $" + String.format("%.2f", allergyBurger.getCost()) + " -> " + allergyBurger.getDescription());
        System.out.println("  Kitchen prep notes: " + allergyBurger.getPrepNotes());
    }
}
