class Vendor:
    def submit(self, p):
        return {"accepted": True, "id": "LAB-1", "payload": p}


class Adapter:
    def __init__(self, v):
        self.vendor = v

    def order(self, p, t):
        if not p or not t:
            raise ValueError("missing")
        r = self.vendor.submit({"patient": {"id": p}, "test": {"code": t}})
        if not r["accepted"]:
            raise RuntimeError("rejected")
        return r["id"]


assert Adapter(Vendor()).order("P1", "CBC") == "LAB-1"
print("PASS")
