class Source:
    def __init__(self):
        self.calls = 0

    def fetch(self, p):
        self.calls += 1
        return {"id": p}


class Proxy:
    def __init__(self, s):
        self.source = s
        self.cache = {}

    def fetch(self, p):
        if p not in self.cache:
            self.cache[p] = self.source.fetch(p)
        return self.cache[p]

    def invalidate(self, p):
        self.cache.pop(p, None)


s = Source()
p = Proxy(s)
p.fetch("P1")
p.fetch("P1")
assert s.calls == 1
p.invalidate("P1")
p.fetch("P1")
assert s.calls == 2
print("PASS")
