"""Decorator: Persisted Profile Store (devtools(persist(creator)))."""


class BasicStore:
    """ConcreteComponent."""

    def __init__(self) -> None:
        self._fields = {"profile": "null", "pinForm": "false"}

    def set(self, field: str, value: str) -> None:
        if field not in self._fields:
            raise ValueError(f"unknown field {field}")
        self._fields[field] = value

    def state(self) -> str:
        return f"profile={self._fields['profile']}&pinForm={self._fields['pinForm']}"

    def clear_storage(self) -> None:
        raise ValueError("clearStorage not available")


class StoreDecorator:
    """Base Decorator: forwards everything to the wrapped store."""

    def __init__(self, inner) -> None:
        self._inner = inner

    def set(self, field: str, value: str) -> None:
        self._inner.set(field, value)

    def state(self) -> str:
        return self._inner.state()

    def clear_storage(self) -> None:
        self._inner.clear_storage()


class PersistDecorator(StoreDecorator):
    KEY = "test-store"

    def __init__(self, inner, storage: dict) -> None:
        super().__init__(inner)
        self._storage = storage

    def set(self, field: str, value: str) -> None:
        super().set(field, value)
        self._storage[self.KEY] = self.state()

    def clear_storage(self) -> None:
        self._storage.pop(self.KEY, None)


class DevtoolsDecorator(StoreDecorator):
    def __init__(self, inner, log: list) -> None:
        super().__init__(inner)
        self._log = log

    def set(self, field: str, value: str) -> None:
        super().set(field, value)
        self._log.append(f"set {field}={value}")
