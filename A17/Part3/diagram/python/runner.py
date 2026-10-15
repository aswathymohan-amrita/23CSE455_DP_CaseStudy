import sys
from diagram import DiagramParser, Compact, Bracketed, NamesAdapter, Exporter

try:
    model = DiagramParser().parse(sys.stdin.read().splitlines())
    renderer = {"compact": Compact, "bracketed": Bracketed, "json": NamesAdapter}[sys.argv[1]]()
    print(Exporter(renderer).export(model))
except ValueError as error:
    print("ERROR:" + str(error))
