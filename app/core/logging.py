import json
import logging

from app.core.tracing import trace_id_var


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname.lower(),
            "message": record.getMessage(),
            "trace_id": trace_id_var.get(),
        }
        for key in ("path", "method", "status_code", "duration_ms"):
            value = getattr(record, key, None)
            if value is not None:
                log[key] = value
        if record.exc_info:
            log["error"] = self.formatException(record.exc_info)
        return json.dumps(log)


def configure_logging() -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logging.basicConfig(level=logging.INFO, handlers=[handler], force=True)
