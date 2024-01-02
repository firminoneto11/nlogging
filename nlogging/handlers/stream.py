from asyncio import StreamWriter, get_running_loop
from dataclasses import dataclass
from sys import stderr
from typing import TYPE_CHECKING

from nlogging.protocols import AIOProtocol

from .base import BaseAsyncHandler, get_stderr_lock

if TYPE_CHECKING:
    from nlogging._types import LevelType
    from nlogging.formatters import BaseFormatter


@dataclass
class _ResourceManager:
    _stderr_writer = None
    _closed = False

    @property
    def closed(self):
        return self._closed

    @property
    def lock(self):
        return get_stderr_lock()

    async def send_message(self, msg: bytes):
        async with self.lock:
            if self.closed:
                raise RuntimeError("Writer was closed")

            if not self._stderr_writer:
                loop = get_running_loop()
                transport, protocol = await loop.connect_write_pipe(AIOProtocol, stderr)
                self._stderr_writer = StreamWriter(
                    transport=transport, protocol=protocol, reader=None, loop=loop
                )

            self._stderr_writer.write(msg)
            await self._stderr_writer.drain()

    async def close(self):
        # TODO: Should we hook this method with process signals?
        async with self.lock:
            if (self.closed) or (not self._stderr_writer):
                return

            self._stderr_writer.write(b"Closing stderr...")
            await self._stderr_writer.drain()

            self._stderr_writer.close()
            await self._stderr_writer.wait_closed()
            self._stderr_writer, self._closed = None, True


class AsyncStreamHandler(BaseAsyncHandler):
    _manager = _ResourceManager()

    def __init__(self, level: "LevelType", formatter: "BaseFormatter"):
        super().__init__(level=level, formatter=formatter)

    @property
    def manager(self):
        return self._manager

    async def write_and_flush(self, msg: bytes):
        await self.manager.send_message(msg)

    async def close(self):
        # NOTE: If we close the StreamWriter bound to sys.stderr, nothing else would be
        # able to use sys.stderr it again. So we just pass for now.
        pass
