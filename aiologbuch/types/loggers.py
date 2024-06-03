from typing import TYPE_CHECKING, Protocol, Self

if TYPE_CHECKING:
    from .general import LoggerKind


class BaseLoggerProtocol(Protocol):
    kind: "LoggerKind"

    def __call__(self, name: str) -> Self:
        ...


class AsyncLoggerProtocol(BaseLoggerProtocol):
    async def _disable(self) -> None:
        ...


class SyncLoggerProtocol(BaseLoggerProtocol):
    def _disable(self) -> None:
        ...
