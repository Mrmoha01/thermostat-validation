import math

VERSIONS = ("1.0.0", "1.1.0-rc1")

SETPOINT_MIN = 5.0
SETPOINT_MAX = 30.0
HYSTERESIS = 1.0
OVERHEAT_C = 35.0
RESET_BELOW_C = 30.0
SENSOR_MIN = -20.0
SENSOR_MAX = 80.0

AMBIENT_C = 18.0
HEAT_RATE = 0.1   # degrees per second with heater on
COOL_RATE = 0.05  # degrees per second towards ambient with heater off


class Thermostat:
    def __init__(self, version="1.0.0"):
        if version not in VERSIONS:
            raise ValueError(f"unknown firmware version: {version}")
        self.version = version
        self.temp_c = 20.0
        self.setpoint = 20.0
        self.mode = "AUTO"
        self.heater_on = False
        self.alarm = False
        self.sensor_fault = False

    @property
    def is_rc1(self):
        return self.version == "1.1.0-rc1"

    def state(self):
        if self.sensor_fault:
            return "SENSOR_FAULT"
        if self.alarm:
            return "ALARM"
        return "NORMAL"

    def advance(self, seconds):
        for _ in range(int(seconds)):
            self._apply_physics()
            self._update()

    def handle(self, line):
        # the firmware reads the sensor before answering, so injected
        # temperatures take effect on the next command
        self._update()

        parts = line.strip().split()
        if not parts:
            return "ERR CMD"
        cmd, args = parts[0], parts[1:]

        if cmd == "PING" and not args:
            return "PONG"
        if cmd == "VER" and not args:
            return f"VER {self.version}"
        if cmd == "TEMP?" and not args:
            return f"TEMP {self.temp_c:.1f}"
        if cmd == "HEATER?" and not args:
            return "HEATER ON" if self.heater_on else "HEATER OFF"
        if cmd == "STATE?" and not args:
            return f"STATE {self.state()}"
        if cmd == "RESET" and not args:
            return self._reset()
        if cmd == "SET":
            return self._set(args)
        if cmd == "MODE":
            return self._mode(args)
        return "ERR CMD"

    def _set(self, args):
        if len(args) != 1:
            return "ERR ARG"
        try:
            value = float(args[0])
        except ValueError:
            return "ERR ARG"
        if not math.isfinite(value):
            return "ERR ARG"

        if self.is_rc1:
            in_range = SETPOINT_MIN <= value < SETPOINT_MAX
        else:
            in_range = SETPOINT_MIN <= value <= SETPOINT_MAX
        if not in_range:
            return "ERR RANGE"

        self.setpoint = value
        self._update()
        return "OK"

    def _mode(self, args):
        if len(args) != 1 or args[0] not in ("AUTO", "OFF"):
            return "ERR ARG"
        self.mode = args[0]
        self._update()
        return "OK"

    def _reset(self):
        limit = 32.0 if self.is_rc1 else RESET_BELOW_C
        if self.alarm and self.temp_c >= limit:
            return "ERR HOT"
        self.alarm = False
        self._update()
        return "OK"

    def _is_overheat(self, temp):
        if self.is_rc1:
            return temp > OVERHEAT_C
        return temp >= OVERHEAT_C

    def _update(self):
        temp = self.temp_c
        self.sensor_fault = not (SENSOR_MIN <= temp <= SENSOR_MAX)
        if not self.sensor_fault and self._is_overheat(temp):
            self.alarm = True

        if self.state() != "NORMAL" or self.mode == "OFF":
            self.heater_on = False
        elif temp < self.setpoint - HYSTERESIS:
            self.heater_on = True
        elif temp > self.setpoint + HYSTERESIS:
            self.heater_on = False

    def _apply_physics(self):
        if self.heater_on:
            self.temp_c += HEAT_RATE
        elif self.temp_c > AMBIENT_C:
            self.temp_c = max(AMBIENT_C, self.temp_c - COOL_RATE)
        else:
            self.temp_c = min(AMBIENT_C, self.temp_c + COOL_RATE)
