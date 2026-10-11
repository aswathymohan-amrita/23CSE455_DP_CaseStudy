class Card {
  pay(amount, reference) {
    return { provider: "card", amount, ref: reference };
  }
}

class Wallet {
  pay(amount, reference) {
    return { provider: "wallet", amount, ref: reference };
  }
}

class Billing {
  constructor(strategy) {
    this.strategy = strategy;
  }

  checkout(amount, reference) {
    if (amount <= 0 || !reference) {
      throw Error("invalid");
    }
    return this.strategy.pay(amount, reference);
  }
}

if (
  new Billing(new Card()).checkout(100, "B1").provider !== "card" ||
  new Billing(new Wallet()).checkout(100, "B1").provider !== "wallet"
) {
  throw Error("strategy");
}
console.log("PASS");
