class Observer:
    def __init__(self):
        self.events = []

    def update(self, e):
        self.events.append(e)


class Publisher:
    def __init__(self):
        self.subs = []

    def subscribe(self, o):
        self.subs.append(o)

    def unsubscribe(self, o):
        self.subs.remove(o)

    def publish(self, e):
        for o in self.subs:
            o.update(e)


p = Publisher()
o = Observer()
p.subscribe(o)
p.publish("lab.ready")
p.unsubscribe(o)
p.publish("other")
assert o.events == ["lab.ready"]
print("PASS")
