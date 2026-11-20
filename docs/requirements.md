# Requirements

Device: simulated smart thermostat, text protocol over a serial line (one command per line).

Default after start: setpoint 20.0 C, temperature 20.0 C, mode AUTO, heater OFF, state NORMAL.

| ID | Requirement |
|----|-------------|
| REQ-01 | `PING` returns `PONG`. |
| REQ-02 | `VER` returns `VER <version>`. |
| REQ-03 | `SET <t>` sets the setpoint. 5.0 to 30.0 C (inclusive) returns `OK`; outside the range returns `ERR RANGE`; a value that is not a number returns `ERR ARG`. |
| REQ-04 | `TEMP?` returns `TEMP <t>` with one decimal, e.g. `TEMP 21.0`. |
| REQ-05 | In AUTO mode the heater turns ON when temp < setpoint - 1.0 and OFF when temp > setpoint + 1.0. In between it keeps its state (hysteresis). `HEATER?` returns `HEATER ON` or `HEATER OFF`. |
| REQ-06 | `MODE AUTO` and `MODE OFF` return `OK`. In OFF mode the heater is always off. |
| REQ-07 | Overheat: temp >= 35.0 C sets state ALARM and turns the heater off. `RESET` clears the alarm only when temp < 30.0 C, otherwise it returns `ERR HOT`. |
| REQ-08 | Sensor fault: temp outside -20.0 to 80.0 C sets state SENSOR_FAULT and turns the heater off. It clears automatically when the reading is valid again. |
| REQ-09 | An unknown or malformed command returns `ERR CMD`. |
| REQ-10 | `STATE?` returns `STATE NORMAL`, `STATE ALARM` or `STATE SENSOR_FAULT`. |
