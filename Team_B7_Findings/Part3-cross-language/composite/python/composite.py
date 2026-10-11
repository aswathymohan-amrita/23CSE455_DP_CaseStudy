from abc import ABC, abstractmethod


class Component(ABC):
    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def add_child(self, child: "Component") -> None:
        raise NotImplementedError

    @abstractmethod
    def remove_child(self, child: "Component") -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_children(self) -> tuple["Component", ...]:
        raise NotImplementedError

    @abstractmethod
    def traverse(self) -> list[str]:
        raise NotImplementedError


class Leaf(Component):
    def __init__(self, name: str) -> None:
        self._name = name

    def get_name(self) -> str:
        return self._name

    def add_child(self, child: Component) -> None:
        raise TypeError("A location leaf cannot contain children")

    def remove_child(self, child: Component) -> bool:
        return False

    def get_children(self) -> tuple[Component, ...]:
        return ()

    def traverse(self) -> list[str]:
        return [self._name]


class Container(Component):
    def __init__(self, name: str) -> None:
        self._name = name
        self._children: list[Component] = []

    def get_name(self) -> str:
        return self._name

    def add_child(self, child: Component) -> None:
        self._children.append(child)

    def remove_child(self, child: Component) -> bool:
        try:
            self._children.remove(child)
            return True
        except ValueError:
            return False

    def get_children(self) -> tuple[Component, ...]:
        return tuple(self._children)

    def traverse(self) -> list[str]:
        names = [self._name]
        for child in self._children:
            names.extend(child.traverse())
        return names
