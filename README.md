# Thermostat Validation

![tests](https://github.com/<user>/<repo>/actions/workflows/tests.yml/badge.svg)

A simulated smart thermostat and a pytest suite that validates its firmware against
written requirements. The simulator has two firmware versions: 1.0.0 (correct) and
1.1.0-rc1 (a release candidate with three bugs). The suite is used to decide whether
the release candidate can be released.

## How to run

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

pytest                      # tests firmware 1.0.0
pytest --fw 1.1.0-rc1       # tests the release candidate
pytest --html=reports/report.html --self-contained-html
```

## Results

| Version | Tests | Passed | Failed |
|---------|-------|--------|--------|
| 1.0.0 | 35 | 35 | 0 |
| 1.1.0-rc1 | 35 | 31 | 4 |

The four failures on 1.1.0-rc1 are three bugs, see `docs/bugs/` and
`docs/release_report.md`. Release is not recommended.

CI runs both versions on every push and uploads the HTML reports as artifacts. The
release candidate job is allowed to fail.

## Project structure

```
thermostat/sim.py          device simulator and serial protocol
tests/conftest.py          --fw option, sim and dut fixtures, report column
tests/dut.py               driver class used by the tests
tests/test_protocol.py     PING, VER, TEMP?, STATE?, unknown commands
tests/test_setpoint.py     SET range and argument checks
tests/test_heating.py      hysteresis control and modes
tests/test_safety.py       overheat alarm, reset, sensor fault
docs/requirements.md       REQ-01 to REQ-10
docs/test_plan.md          scope, environment, pass criteria
docs/bugs/                 bug reports for 1.1.0-rc1
docs/release_report.md     release recommendation
.github/workflows/tests.yml  CI
```
