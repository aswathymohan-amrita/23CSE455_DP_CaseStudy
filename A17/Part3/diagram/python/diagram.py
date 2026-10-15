from abc import ABC, abstractmethod
import json


class Block(ABC):
    @abstractmethod
    def names(self):
        pass


class Node(Block):
    def __init__(self, name):
        self.name = name

    def names(self):
        return [self.name]


class Group(Block):
    def __init__(self):
        self.children = []

    def names(self):
        return [name for child in self.children for name in child.names()]


class Model(ABC):
    @abstractmethod
    def add(self, name):
        pass


class Diagram(Model):
    def __init__(self):
        self.root = Group()
        self.stack = [self.root]
        self.links = []

    def add(self, name):
        if name in self.root.names():
            raise ValueError("duplicate")
        self.stack[-1].children.append(Node(name))

    def link(self, left, right):
        names = self.root.names()
        if left not in names or right not in names:
            raise ValueError("missing endpoint")
        self.links.append(left + "->" + right)


class Command(ABC):
    @abstractmethod
    def execute(self, model, args):
        pass


class Create(Command):
    def execute(self, model, args):
        model.add(args[0])


class Link(Command):
    def execute(self, model, args):
        model.link(*args)


class OpenGroup(Command):
    def execute(self, model, args):
        group = Group()
        model.stack[-1].children.append(group)
        model.stack.append(group)


class CloseGroup(Command):
    def execute(self, model, args):
        if len(model.stack) == 1:
            raise ValueError("unmatched end")
        model.stack.pop()


class Parser(ABC):
    commands = {"class": (1, Create()), "link": (2, Link()),
                "group": (0, OpenGroup()), "end": (0, CloseGroup())}

    @abstractmethod
    def create_model(self):
        pass

    def parse(self, lines):
        model = self.create_model()
        for line in lines:
            words = line.split()
            if not words:
                continue
            if words[0] not in self.commands:
                raise ValueError("syntax")
            arity, command = self.commands[words[0]]
            if len(words) != arity + 1:
                raise ValueError("syntax")
            command.execute(model, words[1:])
        if len(model.stack) != 1:
            raise ValueError("unclosed group")
        return model


class DiagramParser(Parser):
    def create_model(self):
        return Diagram()


class Renderer(ABC):
    @abstractmethod
    def render(self, model):
        pass


class Compact(Renderer):
    def render(self, model):
        return ",".join(model.root.names()) + "|" + ",".join(model.links)


class Bracketed(Renderer):
    def render(self, model):
        return ",".join("[" + name + "]" for name in model.root.names()) + "|" + ",".join(model.links)


class LegacyNames:
    def encode(self, names):
        return json.dumps(names, separators=(",", ":"))


class NamesAdapter(Renderer):
    def __init__(self):
        self.legacy = LegacyNames()

    def render(self, model):
        return self.legacy.encode(model.root.names())


class Exporter:
    def __init__(self, renderer):
        self.renderer = renderer

    def export(self, model):
        return self.renderer.render(model)
