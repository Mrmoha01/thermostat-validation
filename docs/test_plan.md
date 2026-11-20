# Test Plan

## Scope

Functional validation of the thermostat firmware against REQ-01 to REQ-10
(see `requirements.md`). Versions under test: 1.0.0 and 1.1.0-rc1.

Out of scope: real hardware, timing of the serial line, power and EMC tests.

## Test levels

- Protocol tests: each command and its responses, including malformed input.
- Functional tests: setpoint range, heater control with hysteresis, modes.
- Safety tests: overheat alarm, alarm reset, sensor fault.

Boundary values are tested on both sides of every limit (for example 4.9 / 5.0
and 30.0 / 30.1 for the setpoint). Faults are injected by writing the sensor
temperature directly in the simulator.

## Environment

- Python 3.12, pytest, pytest-html
- Device simulator `thermostat/sim.py` with simulated time, so long scenarios run instantly
- GitHub Actions on every push (`.github/workflows/tests.yml`)

## How to run

```
pip install -r requirements.txt
pytest                                  # firmware 1.0.0
pytest --fw 1.1.0-rc1                   # release candidate
pytest --html=reports/report.html --self-contained-html
```

## Traceability

Every test has a `@pytest.mark.req("REQ-xx")` marker. Collection fails if a test has no
marker. The HTML report shows the requirement ID for each test.

## Pass criteria

- 100 % of tests pass on the version proposed for release.
- Every requirement is covered by at least one test.
- Any failure is logged as a bug report in `docs/bugs/`, and a release with an open
  high-severity bug is not recommended.
