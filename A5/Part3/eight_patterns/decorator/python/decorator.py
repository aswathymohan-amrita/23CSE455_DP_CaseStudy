class Reader:
    def read(self, p):
        return {"patient_id": p, "summary": "synthetic"}


class AuditedReader:
    def __init__(self, inner):
        self.inner = inner
        self.audit = []

    def read(self, p):
        r = self.inner.read(p)
        self.audit.append(("read", p))
        return r


a = AuditedReader(Reader())
assert a.read("P1")["patient_id"] == "P1" and a.audit == [("read", "P1")]
print("PASS")
