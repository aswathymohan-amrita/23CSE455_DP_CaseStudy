class Store:
    def __init__(self):
        self.rows = []

    def save(self, p, d):
        self.rows.append((p, d))
        return len(self.rows)


class Notice:
    def __init__(self):
        self.sent = []

    def send(self, p, msg):
        self.sent.append((p, msg))


class Facade:
    def __init__(self, s, n):
        self.s, self.n = s, n

    def book(self, p, d):
        if not p or not d:
            raise ValueError("missing fields")
        i = self.s.save(p, d)
        self.n.send(p, str(i))
        return i


s, n = Store(), Notice()
assert Facade(s, n).book("P1", "D1") == 1 and len(n.sent) == 1
print("PASS")
