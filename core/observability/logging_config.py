import json
import logging
import traceback
from datetime import datetime, UTC
from typing import Any


class JsonExtraFormatter(logging.Formatter):
    """
    JSON formatter for application logs.

    Common fields:
    - ts
    - level
    - logger
    - msg

    Extra fields are added from logger.extra.
    Exception fields are added when exc_info exists.
    """

    # استانداردهایی که نمی‌خوایم به عنوان extra چاپ کنیم
    _reserved = {
        "name", "msg", "args", "levelname", "levelno", "pathname", "filename",
        "module", "exc_info", "exc_text", "stack_info", "lineno", "funcName",
        "created", "msecs", "relativeCreated", "thread", "threadName",
        "processName", "process", "message", "asctime", "taskName"
    }

    def format(self, record: logging.LogRecord) -> str:
        log = {
            "ts": datetime.fromtimestamp(record.created, UTC).isoformat().replace("+00:00", "Z"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }

        # همه‌ی extra ها (هر چیزی غیر از reserved)
        extras = {
            k: self._serialize(v) 
            for k, v in record.__dict__.items()
            if k not in self._reserved and not k.startswith("_")
        }
        
        if extras:
            log.update(extras)

        if record.exc_info:
            exc_type, exc_value, exc_tb = record.exc_info

            log["exception"] = {
                "type": exc_type.__name__ if exc_type else None,
                "message": str(exc_value),
                "traceback": "".join(
                    traceback.format_exception(exc_type, exc_value, exc_tb)
                )
            }

        return json.dumps(log, ensure_ascii=False, default=str)

    @staticmethod
    def _serialize(value: Any) -> Any:
        try:
            json.dumps(value)
            return value
        except TypeError:
            return str(value)


def configure_logging(level: int = logging.INFO) -> None:
    root = logging.getLogger()
    root.setLevel(level)

    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(JsonExtraFormatter())

    # جلوگیری از handler های تکراری در --reload
    root.handlers.clear()
    root.addHandler(handler)
