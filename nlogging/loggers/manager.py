from typing import TYPE_CHECKING, Optional, Self

if TYPE_CHECKING:
    from nlogging._types import LevelType, LoggerProtocol


class AsyncLoggerManagerSingleton[LC: "LoggerProtocol"]:
    _instance: Optional[Self] = None
    _active_loggers: dict[str, LC]
    _logger_class: LC

    def __new__(cls, logger_class: LC):
        self, created = cls.get_instance()
        if created:
            self._active_loggers = {}
            self._logger_class = logger_class
        return self

    @property
    def lc(self):
        return self._logger_class

    @classmethod
    def get_instance(cls):
        created = False
        if not cls._instance:
            cls._instance = super().__new__(cls)
            created = True
        return cls._instance, created

    def get_logger(self, name: str, level: "LevelType"):
        created = False
        if name not in self._active_loggers:
            self._active_loggers[name], created = self.lc(name, level), True
        (logger := self._active_loggers[name]).level = level
        return logger, created

    @classmethod
    async def disable_loggers(cls):
        self = cls.get_instance()[0]
        for name in self._active_loggers:
            await self._active_loggers[name]._disable()
        self._active_loggers = {}

    @classmethod
    async def disable_logger(cls, name: str):
        self = cls.get_instance()[0]
        if logger := self._active_loggers.pop(name, None):
            await logger._disable()
