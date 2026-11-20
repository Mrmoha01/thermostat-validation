import pytest


@pytest.mark.req("REQ-05")
@pytest.mark.parametrize("start_temp, temp, expected", [
    (20.0, 18.9, "ON"),   # just below the lower threshold
    (20.0, 19.0, "OFF"),  # on the lower threshold, stays off
    (18.0, 21.0, "ON"),   # on the upper threshold, stays on
    (18.0, 21.1, "OFF"),  # just above the upper threshold
])
def test_hysteresis_band(dut, start_temp, temp, expected):
    # start_temp puts the heater in a known state first
    dut.inject_temp(start_temp)
    dut.heater()
    dut.inject_temp(temp)
    assert dut.heater() == expected


@pytest.mark.req("REQ-05")
def test_temperature_settles_around_setpoint(dut):
    dut.set(25)
    dut.wait(600)
    assert 23.8 <= dut.temp() <= 26.2
    assert dut.state() == "NORMAL"


@pytest.mark.req("REQ-06")
def test_mode_off_keeps_heater_off(dut):
    dut.inject_temp(10.0)
    assert dut.heater() == "ON"
    assert dut.mode("OFF") == "OK"
    assert dut.heater() == "OFF"
    dut.wait(60)
    assert dut.heater() == "OFF"


@pytest.mark.req("REQ-06")
def test_mode_auto_resumes_heating(dut):
    dut.mode("OFF")
    dut.inject_temp(10.0)
    assert dut.mode("AUTO") == "OK"
    assert dut.heater() == "ON"


@pytest.mark.req("REQ-06")
def test_invalid_mode_is_rejected(dut):
    assert dut.mode("HEAT") == "ERR ARG"
