import pytest


@pytest.mark.req("REQ-07")
@pytest.mark.parametrize("temp, expected", [(34.9, "NORMAL"), (35.0, "ALARM")])
def test_overheat_threshold(dut, temp, expected):
    dut.inject_temp(temp)
    assert dut.state() == expected


@pytest.mark.req("REQ-07")
def test_alarm_turns_heater_off(dut):
    dut.set(28)
    dut.inject_temp(25.0)
    assert dut.heater() == "ON"
    dut.inject_temp(36.0)
    assert dut.state() == "ALARM"
    assert dut.heater() == "OFF"


@pytest.mark.req("REQ-07")
def test_alarm_stays_latched_without_reset(dut):
    dut.inject_temp(36.0)
    dut.state()
    dut.inject_temp(20.0)
    dut.wait(10)
    assert dut.state() == "ALARM"


@pytest.mark.req("REQ-07")
@pytest.mark.parametrize("temp, response, state", [
    (29.9, "OK", "NORMAL"),
    (30.0, "ERR HOT", "ALARM"),
    (31.0, "ERR HOT", "ALARM"),
])
def test_reset_after_alarm(dut, temp, response, state):
    dut.inject_temp(36.0)
    assert dut.state() == "ALARM"
    dut.inject_temp(temp)
    assert dut.reset() == response
    assert dut.state() == state


@pytest.mark.req("REQ-08")
@pytest.mark.parametrize("temp, expected", [
    (-20.1, "SENSOR_FAULT"),
    (-20.0, "NORMAL"),
    (80.0, "ALARM"),  # valid reading, but above the overheat limit
    (80.1, "SENSOR_FAULT"),
])
def test_sensor_range(dut, temp, expected):
    dut.inject_temp(temp)
    assert dut.state() == expected


@pytest.mark.req("REQ-08")
def test_sensor_fault_turns_heater_off_and_clears(dut):
    dut.inject_temp(-25.0)
    assert dut.state() == "SENSOR_FAULT"
    assert dut.heater() == "OFF"
    dut.inject_temp(15.0)
    assert dut.state() == "NORMAL"
    assert dut.heater() == "ON"
