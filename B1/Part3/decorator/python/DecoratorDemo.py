from abc import ABC, abstractmethod

class MenuItem(ABC):
    @abstractmethod
    def get_description(self) -> str: pass
    @abstractmethod
    def get_cost(self) -> float: pass
    @abstractmethod
    def get_prep_notes(self) -> str: pass

class BaseBurger(MenuItem):
    def get_description(self) -> str: return "Classic Angus Burger"
    def get_cost(self) -> float: return 12.00
    def get_prep_notes(self) -> str: return "Grill beef patty medium"

class MenuItemDecorator(MenuItem):
    def __init__(self, item: MenuItem):
        self._item = item
    def get_description(self) -> str: return self._item.get_description()
    def get_cost(self) -> float: return self._item.get_cost()
    def get_prep_notes(self) -> str: return self._item.get_prep_notes()

class ExtraCheeseDecorator(MenuItemDecorator):
    def get_description(self) -> str: return self._item.get_description() + " + Extra Cheddar"
    def get_cost(self) -> float: return self._item.get_cost() + 2.00
    def get_prep_notes(self) -> str: return self._item.get_prep_notes() + " | Melt double aged cheddar"

class CrispyBaconDecorator(MenuItemDecorator):
    def get_description(self) -> str: return self._item.get_description() + " + Smoked Bacon"
    def get_cost(self) -> float: return self._item.get_cost() + 3.00
    def get_prep_notes(self) -> str: return self._item.get_prep_notes() + " | Add two strips crispy bacon"

class GlutenFreeDecorator(MenuItemDecorator):
    def get_description(self) -> str: return self._item.get_description() + " (Gluten-Free Bun)"
    def get_cost(self) -> float: return self._item.get_cost() + 1.50
    def get_prep_notes(self) -> str: return self._item.get_prep_notes() + " | Use dedicated allergen-safe toaster"

if __name__ == "__main__":
    simple_burger = BaseBurger()
    print(f"Test 1 - Base Burger: ${simple_burger.get_cost():.2f} -> {simple_burger.get_description()}")

    loaded_burger = CrispyBaconDecorator(ExtraCheeseDecorator(BaseBurger()))
    print(f"Test 2 - Loaded Burger: ${loaded_burger.get_cost():.2f} -> {loaded_burger.get_description()}")
    print("  Kitchen prep notes:", loaded_burger.get_prep_notes())

    allergy_burger = GlutenFreeDecorator(ExtraCheeseDecorator(BaseBurger()))
    print(f"Test 3 - GF Burger: ${allergy_burger.get_cost():.2f} -> {allergy_burger.get_description()}")
    print("  Kitchen prep notes:", allergy_burger.get_prep_notes())
