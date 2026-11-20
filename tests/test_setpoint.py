import pytest


@pytest.mark.req("REQ-03")
@pytest.mark.parametrize("value", ["5.0", "30.0"])
def test_setpoint_at_limit_is_accepted(dut, value):
    assert dut.set(value) == "OK"


@pytest.mark.req("REQ-03")
@pytest.mark.parametrize("value", ["4.9", "30.1"])
def test_setpoint_outside_limit_is_rejected(dut, value):
    assert dut.set(value) == "ERR RANGE"


@pytest.mark.req("REQ-03")
@pytest.mark.parametrize("value", ["abc", "nan"])
def test_setpoint_not_a_number(dut, value):
    assert dut.set(value) == "ERR ARG"


@pytest.mark.req("REQ-03")
def test_rejected_setpoint_keeps_old_value(dut):
    assert dut.set(25) == "OK"
    assert dut.set(31) == "ERR RANGE"
    # 23.5 is below 25 - 1.0, so the heater only turns on if 25 is still active
    dut.inject_temp(23.5)
    assert dut.heater() == "ON"
