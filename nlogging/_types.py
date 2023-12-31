from typing import Literal, Optional, Protocol, Self, TypedDict


class CallerInfo(TypedDict):
    caller_filename: str
    caller_function_name: str
    caller_line_number: int


class MapType(TypedDict):
    resource: "_ResourceProtocol"
    reference_count: int


class LoggerProtocol(Protocol):
    def __call__(self, name: str, filter: "FilterProtocol") -> Self:
        ...

    async def _disable(self) -> None:
        ...


class FormatterProtocol(Protocol):
    def format(self, record: "LogRecordProtocol") -> bytes:
        ...


class _ResourceProtocol(Protocol):
    async def init_stream(self) -> None:
        ...

    async def send(self, msg: bytes) -> None:
        ...

    async def close(self) -> None:
        ...


class AsyncHandlerProtocol(Protocol):
    @property
    def id(self) -> int:
        ...

    async def close(self) -> None:
        ...

    async def handle(self, record: "LogRecordProtocol") -> None:
        ...


class FilterProtocol(Protocol):
    def __call__(self, level: int) -> Self:
        ...

    def filter(self, record: "LogRecordProtocol | int") -> bool:
        ...

    @property
    def level(self) -> int:
        ...


class LogRecordProtocol(Protocol):
    levelno: int
    created: float
    msecs: float
    levelname: str
    process: Optional[int]
    processName: Optional[str]
    thread: Optional[int]
    threadName: Optional[str]
    pathname: str
    funcName: str
    lineno: int
    exc_text: Optional[str]

    def getMessage(self) -> str:
        ...


class BackendProtocol(Protocol):
    def __call__(self, filename: str) -> Self:
        ...

    async def init(self) -> None:
        ...

    async def send(self, msg: bytes) -> None:
        ...

    async def close(self) -> None:
        ...


class BinaryFileWrapperProtocol(Protocol):
    async def write(self, msg: bytes) -> None:
        ...

    async def close(self) -> None:
        ...


type MessageType = str | dict
type LevelType = int | Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
