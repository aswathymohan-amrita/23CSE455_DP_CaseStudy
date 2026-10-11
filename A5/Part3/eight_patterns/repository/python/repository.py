class Repository:
    def __init__(self):
        self.rows = {}

    def save(self, p):
        self.rows[p["id"]] = p

    def find(self, i):
        return self.rows.get(i)


class Registry:
    def __init__(self, r):
        self.repo = r

    def register(self, p):
        self.repo.save(p)

    def lookup(self, i):
        return self.repo.find(i)


r = Registry(Repository())
r.register({"id": "P1", "name": "Demo"})
assert r.lookup("P1")["name"] == "Demo" and r.lookup("none") is None
print("PASS")
