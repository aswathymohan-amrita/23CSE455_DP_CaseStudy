class BaseBurger {
  getDescription() { return "Classic Angus Burger"; }
  getCost() { return 12.00; }
  getPrepNotes() { return "Grill beef patty medium"; }
}

class MenuItemDecorator {
  constructor(item) { this.item = item; }
  getDescription() { return this.item.getDescription(); }
  getCost() { return this.item.getCost(); }
  getPrepNotes() { return this.item.getPrepNotes(); }
}

class ExtraCheeseDecorator extends MenuItemDecorator {
  getDescription() { return this.item.getDescription() + " + Extra Cheddar"; }
  getCost() { return this.item.getCost() + 2.00; }
  getPrepNotes() { return this.item.getPrepNotes() + " | Melt double aged cheddar"; }
}

class CrispyBaconDecorator extends MenuItemDecorator {
  getDescription() { return this.item.getDescription() + " + Smoked Bacon"; }
  getCost() { return this.item.getCost() + 3.00; }
  getPrepNotes() { return this.item.getPrepNotes() + " | Add two strips crispy bacon"; }
}

class GlutenFreeDecorator extends MenuItemDecorator {
  getDescription() { return this.item.getDescription() + " (Gluten-Free Bun)"; }
  getCost() { return this.item.getCost() + 1.50; }
  getPrepNotes() { return this.item.getPrepNotes() + " | Use dedicated allergen-safe toaster"; }
}

const simpleBurger = new BaseBurger();
console.log(`Test 1 - Base Burger: $${simpleBurger.getCost().toFixed(2)} -> ${simpleBurger.getDescription()}`);

const loadedBurger = new CrispyBaconDecorator(new ExtraCheeseDecorator(new BaseBurger()));
console.log(`Test 2 - Loaded Burger: $${loadedBurger.getCost().toFixed(2)} -> ${loadedBurger.getDescription()}`);
console.log("  Kitchen prep notes:", loadedBurger.getPrepNotes());

const allergyBurger = new GlutenFreeDecorator(new ExtraCheeseDecorator(new BaseBurger()));
console.log(`Test 3 - GF Burger: $${allergyBurger.getCost().toFixed(2)} -> ${allergyBurger.getDescription()}`);
console.log("  Kitchen prep notes:", allergyBurger.getPrepNotes());
