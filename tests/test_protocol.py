import pytest


@pytest.mark.req("REQ-01")
def test_ping(dut):
    assert dut.ping() == "PONG"


@pytest.mark.req("REQ-02")
def test_version_matches_firmware_under_test(dut, fw):
    assert dut.send("VER") == f"VER {fw}"


@pytest.mark.req("REQ-04")
@pytest.mark.parametrize("temp, expected", [
    (21.0, "TEMP 21.0"),
    (22.46, "TEMP 22.5"),
])
def test_temp_has_one_decimal(dut, temp, expected):
    dut.inject_temp(temp)
    assert dut.send("TEMP?") == expected


@pytest.mark.req("REQ-09")
@pytest.mark.parametrize("line", ["", "ping", "PING 1"])
def test_unknown_or_malformed_command(dut, line):
    assert dut.send(line) == "ERR CMD"


@pytest.mark.req("REQ-10")
def test_defaults_after_start(dut):
    assert dut.state() == "NORMAL"
    assert dut.temp() == 20.0
    assert dut.heater() == "OFF"
