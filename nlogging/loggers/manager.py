from typing import TYPE_CHECKING, Optional, Self

from nlogging.utils import is_direct_subclass

from .base import BaseAsyncLogger

if TYPE_CHECKING:
    from nlogging._types import LevelType


class AsyncLoggerManagerSingleton[LC: BaseAsyncLogger]:
    _instance: Optional[Self] = None
    _active_loggers: dict[str, LC]
    _logger_class: LC

    def __new__(cls, logger_class: LC):
        self, created = cls.get_instance()
        if created:
            self._set_inner_logger(logger_class=logger_class)
        return self

    @property
    def lc(self):
        return self._logger_class

    def _set_inner_logger(self, logger_class: LC):
        self._active_loggers = {}
        if not is_direct_subclass(value=logger_class, base_cls=BaseAsyncLogger):
            raise TypeError(
                f"'logger_class' must be a {BaseAsyncLogger.__name__} subclass"
            )
        self._logger_class = logger_class

    @classmethod
    def get_instance(cls):
        created = False
        if not cls._instance:
            cls._instance = super().__new__(cls)
            created = True
        return cls._instance, created

    def get_logger(self, name: str, level: "LevelType"):
        if name not in self._active_loggers:
            self._active_loggers[name] = self.lc(name, level)
        (logger := self._active_loggers[name]).level = level
        return logger

    @classmethod
    async def disable_loggers(cls):
        self = cls.get_instance()[0]
        for name in self._active_loggers:
            await self._active_loggers[name].disable()
        self._active_loggers = {}

    @classmethod
    async def disable_logger(cls, name: str):
        self = cls.get_instance()[0]
        if logger := self._active_loggers.pop(name, None):
            await logger.disable()