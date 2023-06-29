from dataclasses import dataclass, field
from typing import Any, Iterator, TypeVar

T = TypeVar("T")


@dataclass
class Context:
    targets: list[Any] = field(default_factory=list)

    def __lshift__(self, target: Any) -> None:
        self.targets.append(target)

    def select(self, type_: type[T]) -> Iterator[T]:
        for target in self.targets:
            if isinstance(target, type_):
                yield target
