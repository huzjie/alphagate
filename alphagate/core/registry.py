"""通用注册表：装饰器驱动的可插拔组件注册与实例化。"""
from __future__ import annotations

from typing import Any, Callable, Dict, Generic, List, Optional, Type, TypeVar

T = TypeVar("T")


class Registry(Generic[T]):
    """一个按名字注册类的注册表，支持别名与实例化。"""

    def __init__(self, name: str) -> None:
        self.name = name
        self._items: Dict[str, Type[T]] = {}
        self._aliases: Dict[str, str] = {}

    def register(self, name: str, *aliases: str) -> Callable[[Type[T]], Type[T]]:
        def deco(cls: Type[T]) -> Type[T]:
            self._items[name] = cls
            for a in aliases:
                self._aliases[a] = name
            return cls
        return deco

    def resolve(self, name: str) -> Type[T]:
        key = self._aliases.get(name, name)
        if key not in self._items:
            raise KeyError(f"[{self.name}] unknown: {name!r} (available: {sorted(self._items)})")
        return self._items[key]

    def get(self, name: str, *args: Any, **kwargs: Any) -> T:
        return self.resolve(name)(*args, **kwargs)

    def names(self) -> List[str]:
        return sorted(self._items)

    def __contains__(self, name: str) -> bool:
        return name in self._items or name in self._aliases

    def __len__(self) -> int:
        return len(self._items)


StrategyRegistry = Registry("strategy")
EmbedderRegistry = Registry("embedder")
ModelRegistry = Registry("model")
DataSourceRegistry = Registry("datasource")
