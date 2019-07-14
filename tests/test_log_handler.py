import json
import logging
import contextlib

import mock

from web_log import LogHandler
from web_log import StatoilLogHandler


@contextlib.contextmanager
def handler(logger_, handler_):
    logger = logging.getLogger(logger_)
    logger.addHandler(handler_)
    yield logger
    logger.removeHandler(handler_)


def test_statoil_log_handler():
    statlog = StatoilLogHandler("StatoilHandler")
    with handler("test", statlog) as logger:
        with mock.serve():
            logger.warning("Statoil")

    assert len(mock.OUTPUT) >= 1  # might be other warnings
    found_warning = False  # find "A warning"
    for log in mock.OUTPUT:
        msg = log.decode("UTF-8")
        data = json.loads(msg)
        if data.get("event") == "Statoil":
            assert data.get("application") == "StatoilHandler"
            assert "extra_info" not in data
            assert data["loglevel"] == "WARNING"
            found_warning = True
    assert found_warning


def test_log_handler():
    loghandler = LogHandler("TestHandler")
    with handler("test", loghandler) as logger:
        with mock.serve():
            logger.info("Is ignored")
            logger.warning("A warning")

    assert len(mock.OUTPUT) >= 1  # might be other warnings
    found_warning = False  # find "A warning"
    for log in mock.OUTPUT:
        msg = log.decode("UTF-8")
        data = json.loads(msg)
        if data.get("event") == "A warning":
            assert data.get("application") == "TestHandler"
            assert "extra_info" not in data
            assert data["loglevel"] == "WARNING"
            found_warning = True
    assert found_warning


def test_log_handler_info():
    loghandler = LogHandler("TestHandler2")
    with handler("test", loghandler) as logger:
        with mock.serve():
            logger.setLevel(logging.INFO)
            logger.info("Is not ignored")
            logger.warning("A warning")

    loglevels = {"Is not ignored": "INFO", "A warning": "WARNING"}

    assert len(mock.OUTPUT) >= 2  # might be more logging
    for log in mock.OUTPUT:
        msg = log.decode("UTF-8")
        data = json.loads(msg)
        if data.get("application", "") == "TestHandler2":
            assert "event" in data
            assert data["event"] in loglevels
            key = data["event"]
            assert data["loglevel"] == loglevels.pop(key)

    assert len(loglevels) == 0
