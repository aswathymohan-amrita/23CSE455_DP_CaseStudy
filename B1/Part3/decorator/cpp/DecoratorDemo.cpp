#include <iostream>
#include <string>
#include <memory>

class MenuItem {
public:
    virtual ~MenuItem() = default;
    virtual std::string getDescription() const = 0;
    virtual double getCost() const = 0;
    virtual std::string getPrepNotes() const = 0;
};

class BaseBurger : public MenuItem {
public:
    std::string getDescription() const override { return "Classic Angus Burger"; }
    double getCost() const override { return 12.00; }
    std::string getPrepNotes() const override { return "Grill beef patty medium"; }
};

class MenuItemDecorator : public MenuItem {
protected:
    std::shared_ptr<MenuItem> item;
public:
    MenuItemDecorator(std::shared_ptr<MenuItem> item) : item(item) {}
    std::string getDescription() const override { return item->getDescription(); }
    double getCost() const override { return item->getCost(); }
    std::string getPrepNotes() const override { return item->getPrepNotes(); }
};

class ExtraCheeseDecorator : public MenuItemDecorator {
public:
    ExtraCheeseDecorator(std::shared_ptr<MenuItem> item) : MenuItemDecorator(item) {}
    std::string getDescription() const override { return item->getDescription() + " + Extra Cheddar"; }
    double getCost() const override { return item->getCost() + 2.00; }
    std::string getPrepNotes() const override { return item->getPrepNotes() + " | Melt double aged cheddar"; }
};

class CrispyBaconDecorator : public MenuItemDecorator {
public:
    CrispyBaconDecorator(std::shared_ptr<MenuItem> item) : MenuItemDecorator(item) {}
    std::string getDescription() const override { return item->getDescription() + " + Smoked Bacon"; }
    double getCost() const override { return item->getCost() + 3.00; }
    std::string getPrepNotes() const override { return item->getPrepNotes() + " | Add two strips crispy bacon"; }
};

class GlutenFreeDecorator : public MenuItemDecorator {
public:
    GlutenFreeDecorator(std::shared_ptr<MenuItem> item) : MenuItemDecorator(item) {}
    std::string getDescription() const override { return item->getDescription() + " (Gluten-Free Bun)"; }
    double getCost() const override { return item->getCost() + 1.50; }
    std::string getPrepNotes() const override { return item->getPrepNotes() + " | Use dedicated allergen-safe toaster"; }
};

int main() {
    auto simpleBurger = std::make_shared<BaseBurger>();
    std::cout << "Test 1 - Base Burger: $" << simpleBurger->getCost() << " -> " << simpleBurger->getDescription() << std::endl;

    auto loadedBurger = std::make_shared<CrispyBaconDecorator>(std::make_shared<ExtraCheeseDecorator>(std::make_shared<BaseBurger>()));
    std::cout << "Test 2 - Loaded Burger: $" << loadedBurger->getCost() << " -> " << loadedBurger->getDescription() << std::endl;
    std::cout << "  Kitchen prep notes: " << loadedBurger->getPrepNotes() << std::endl;

    auto allergyBurger = std::make_shared<GlutenFreeDecorator>(std::make_shared<ExtraCheeseDecorator>(std::make_shared<BaseBurger>()));
    std::cout << "Test 3 - GF Burger: $" << allergyBurger->getCost() << " -> " << allergyBurger->getDescription() << std::endl;
    std::cout << "  Kitchen prep notes: " << allergyBurger->getPrepNotes() << std::endl;

    return 0;
}
