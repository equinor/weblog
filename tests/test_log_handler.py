import json
import logging
import mock

from web_log import StatoilLogHandler


def test_log_handler():
    with mock.serve():
        logger = logging.getLogger("test")
        logger.addHandler(StatoilLogHandler("TestHandler"))
        logger.info("Is ignored")
        logger.warning("A warning")

    print(mock.OUTPUT)
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
    with mock.serve():
        logger = logging.getLogger("test")
        logger.addHandler(StatoilLogHandler("TestHandler2"))
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
