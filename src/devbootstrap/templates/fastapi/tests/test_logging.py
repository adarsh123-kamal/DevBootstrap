"""Tests for structured JSON logging."""

import json
import logging

from app.core.logging_config import JsonFormatter


def test_json_formatter_includes_standard_fields() -> None:
    record = logging.LogRecord(
        name="service.test",
        level=logging.WARNING,
        pathname=__file__,
        lineno=1,
        msg="example message",
        args=(),
        exc_info=None,
    )

    payload = json.loads(JsonFormatter().format(record))

    assert payload["level"] == "WARNING"
    assert payload["logger"] == "service.test"
    assert payload["message"] == "example message"
    assert "timestamp" in payload
