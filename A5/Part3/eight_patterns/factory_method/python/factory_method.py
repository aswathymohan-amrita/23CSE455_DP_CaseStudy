import csv
import io
import json


class JsonExporter:
    def export(self, r):
        return json.dumps(r)


class CsvExporter:
    def export(self, r):
        b = io.StringIO()
        csv.writer(b).writerow(r.values())
        return b.getvalue()


class Factory:
    def __init__(self, kind):
        self.kind = kind

    def create_exporter(self):
        return JsonExporter() if self.kind == "json" else CsvExporter()

    def export(self, r):
        return self.create_exporter().export(r)


assert "P1" in Factory("json").export({"id": "P1"})
assert "P1" in Factory("csv").export({"id": "P1"})
print("PASS")
