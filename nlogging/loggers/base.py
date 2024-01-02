from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from logging import LogRecord

    from nlogging._types import CallerInfo, LevelType, MessageType
    from nlogging.handlers import BaseAsyncHandler, BaseSyncHandler


class BaseAsyncLogger:
    __metaclass__ = ABCMeta

    _handlers: dict[int, "BaseAsyncHandler"]

    @abstractmethod
    def __init__(self, name: str, level: "LevelType") -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def level(self) -> int:
        raise NotImplementedError

    @level.setter
    @abstractmethod
    def level(self, value: "LevelType") -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def handlers(self) -> dict[str, "BaseAsyncHandler"]:
        raise NotImplementedError

    @property
    def mem_addr(self) -> str:
        raise NotImplementedError

    @abstractmethod
    async def debug(self, msg: "MessageType") -> None:
        raise NotImplementedError

    @abstractmethod
    async def info(self, msg: "MessageType") -> None:
        raise NotImplementedError

    @abstractmethod
    async def warning(self, msg: "MessageType") -> None:
        raise NotImplementedError

    @abstractmethod
    async def error(
        self, msg: "MessageType", exc: Optional[BaseException] = None
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def critical(self, msg: "MessageType") -> None:
        raise NotImplementedError

    @abstractmethod
    def find_caller(self) -> "CallerInfo":
        raise NotImplementedError

    @abstractmethod
    def make_record(
        self,
        name: str,
        level: int,
        msg: "MessageType",
        filename: str,
        function_name: str,
        line_number: int,
        exc_info: Optional[BaseException] = None,
    ) -> "LogRecord":
        raise NotImplementedError

    @abstractmethod
    async def _log(
        self, level: int, msg: "MessageType", exc_info: Optional[BaseException] = None
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def handle(self, record: "LogRecord") -> None:
        raise NotImplementedError

    @abstractmethod
    def add_handler(self, handler: "BaseAsyncHandler") -> None:
        raise NotImplementedError

    @abstractmethod
    def remove_handler(self, handler: "BaseAsyncHandler") -> None:
        raise NotImplementedError

    @abstractmethod
    def has_handlers(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def call_handlers(self, record: "LogRecord") -> None:
        raise NotImplementedError

    @abstractmethod
    def is_enabled_for(self, level: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def update_handlers_level(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def disable(self) -> None:
        raise NotImplementedError


class BaseSyncLogger(BaseAsyncLogger):
    _handlers: dict[int, "BaseSyncHandler"]

    @abstractmethod
    def debug(self, msg: "MessageType") -> None:
        raise NotImplementedError

    @abstractmethod
    def info(self, msg: "MessageType") -> None:
        raise NotImplementedError

    @abstractmethod
    def warning(self, msg: "MessageType") -> None:
        raise NotImplementedError

    @abstractmethod
    def error(self, msg: "MessageType", exc: Optional[BaseException] = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def critical(self, msg: "MessageType") -> None:
        raise NotImplementedError

    @abstractmethod
    def _log(
        self, level: int, msg: "MessageType", exc_info: Optional[BaseException] = None
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def handle(self, record: "LogRecord") -> None:
        raise NotImplementedError

    @abstractmethod
    def call_handlers(self, record: "LogRecord") -> None:
        raise NotImplementedError

    @abstractmethod
    def disable(self) -> None:
        raise NotImplementedError
