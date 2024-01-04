from asyncio import create_task
from functools import lru_cache
from logging import Handler
from typing import TYPE_CHECKING
from warnings import warn

from anyio.to_thread import run_sync

from nlogging.filters import Filter
from nlogging.shared import RAISE_EXCEPTIONS, get_stderr_lock

if TYPE_CHECKING:
    from logging import LogRecord

    from nlogging._types import FormatterProtocol, LevelType


@lru_cache(maxsize=1)
def _handler_id_generator():
    i = 1
    while True:
        yield i
        i += 1


class BaseAsyncHandler:
    terminator = b"\n"

    def __init__(self, level: "LevelType", formatter: "FormatterProtocol"):
        self._id = next(_handler_id_generator())
        self._filter = Filter(level=level)
        self.formatter = formatter

    @property
    def id(self):
        return self._id

    @property
    def filter(self):
        return self._filter

    def set_level(self, level: "LevelType"):
        self.filter.level = level

    async def emit(self, record: "LogRecord"):
        try:
            msg = self.format(record) + self.terminator
            await self.write_and_flush(msg)
        except:  # noqa
            await self.handle_error(record)

    async def write_and_flush(self, msg: bytes) -> None:
        raise NotImplementedError(
            "'write_and_flush' must be implemented by Handler subclasses"
        )

    async def close(self) -> None:
        raise NotImplementedError("'close' must be implemented by Handler subclasses")

    def format(self, record: "LogRecord"):
        return self.formatter.format(record)

    async def handle(self, record: "LogRecord"):
        if self.filter.filter(record):
            await self.emit(record)

    async def handle_error(self, record: "LogRecord"):
        if RAISE_EXCEPTIONS:
            async with get_stderr_lock():
                await run_sync(Handler.handleError, None, record)

    def __del__(self):
        try:
            create_task(self.close())
        except RuntimeError:
            warn("Event loop is closed. Handler resources may not be closed properly")
