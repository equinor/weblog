import json
import web_log
import mock


def test_server():
    with mock.serve():
        web_log.log("TestApp", "TestEvent", async_=False)
        web_log.log("TestApp2", "TestEvent2", extra_info="a b c", async_=True)

    assert len(mock.OUTPUT) == 2
    msg0 = mock.OUTPUT[0].decode("UTF-8")
    data0 = json.loads(msg0)
    assert "application" in data0
    assert data0["application"] == "TestApp"
    assert "event" in data0
    assert data0["event"] == "TestEvent"
    assert "extra_info" not in data0

    msg1 = mock.OUTPUT[1].decode("UTF-8")
    data1 = json.loads(msg1)
    assert "application" in data1
    assert data1["application"] == "TestApp2"
    assert "event" in data1
    assert data1["event"] == "TestEvent2"
    assert "extra_info" in data1
    assert data1["extra_info"] == "a b c"
