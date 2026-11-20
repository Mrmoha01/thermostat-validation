class Dut:
    def __init__(self, sim):
        self.sim = sim

    def send(self, line):
        return self.sim.handle(line)

    def ping(self):
        return self.send("PING")

    def version(self):
        return self.send("VER").removeprefix("VER ")

    def set(self, value):
        return self.send(f"SET {value}")

    def mode(self, value):
        return self.send(f"MODE {value}")

    def reset(self):
        return self.send("RESET")

    def temp(self):
        return float(self.send("TEMP?").removeprefix("TEMP "))

    def heater(self):
        return self.send("HEATER?").removeprefix("HEATER ")

    def state(self):
        return self.send("STATE?").removeprefix("STATE ")

    def inject_temp(self, temp_c):
        self.sim.temp_c = temp_c

    def wait(self, seconds):
        self.sim.advance(seconds)
