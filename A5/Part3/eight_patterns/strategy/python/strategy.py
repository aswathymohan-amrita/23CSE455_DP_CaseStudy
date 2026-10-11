class Card:
    def pay(self, amount, ref):
        return {"provider": "card", "amount": amount, "reference": ref}


class Wallet:
    def pay(self, amount, ref):
        return {"provider": "wallet", "amount": amount, "reference": ref}


class Billing:
    def __init__(self, strategy):
        self.strategy = strategy

    def checkout(self, amount, ref):
        if amount <= 0 or not ref:
            raise ValueError("invalid")
        return self.strategy.pay(amount, ref)


assert Billing(Card()).checkout(100, "B1")["provider"] == "card"
assert Billing(Wallet()).checkout(100, "B1")["provider"] == "wallet"
print("PASS")
