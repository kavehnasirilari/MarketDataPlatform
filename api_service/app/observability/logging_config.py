import json
import logging
from datetime import datetime


class JsonExtraFormatter(logging.Formatter):
    """
    Prints message + selected record fields + any extra fields.
    """

    # استانداردهایی که نمی‌خوایم به عنوان extra چاپ کنیم
    _reserved = {
        "name", "msg", "args", "levelname", "levelno", "pathname", "filename",
        "module", "exc_info", "exc_text", "stack_info", "lineno", "funcName",
        "created", "msecs", "relativeCreated", "thread", "threadName",
        "processName", "process", "message", "asctime"
    }

    def format(self, record: logging.LogRecord) -> str:
        base = {
            "ts": datetime.utcfromtimestamp(record.created).isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }

        # همه‌ی extra ها (هر چیزی غیر از reserved)
        extras = {
            k: v for k, v in record.__dict__.items()
            if k not in self._reserved and not k.startswith("_")
        }

        if extras:
            base.update(extras)

        return json.dumps(base, ensure_ascii=False)


def configure_logging(level: int = logging.INFO) -> None:
    root = logging.getLogger()
    root.setLevel(level)

    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(JsonExtraFormatter())

    # جلوگیری از handler های تکراری در --reload
    root.handlers.clear()
    root.addHandler(handler)
