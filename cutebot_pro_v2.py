from microbit import i2c, sleep, pin8, pin12, pin15, display
from machine import time_pulse_us
import time
import neopixel
import random
import math

I2C_ADDR = 0x10
START_BYTE_1 = 0xFF
START_BYTE_2 = 0xF9
REG_DATA = 0x00
LINE_LOST = 4000

CMD_MOTOR = 0x10
CMD_LIGHT = 0x20
CMD_TRACKBIT = 0x60
CMD_READ = 0xA0


class MotorSelector:
    LEFT = 0
    RIGHT = 1
    ALL = 2


class LightSelector:
    LEFT = 0
    RIGHT = 1
    ALL = 2


class SpeedUnit:
    CM_PER_SEC = 0
    IN_PER_SEC = 1


class DistanceUnit:
    CENTIMETERS = 0
    INCHES = 1


class CutebotPro:
    def __init__(self):
        self._echo_pin = pin12
        self._trigger_pin = pin8
        self._np = neopixel.NeoPixel(pin15, 2)
        self.version = -1
        self._controller_version = None
        self.four_way_state_value = 0
        self._left_distance_offset = 0
        self._right_distance_offset = 0
        self._detect_hardware_version()

    def _get_register(self, register):
        i2c.write(I2C_ADDR, bytearray([register]))
        return i2c.read(I2C_ADDR, 1)[0]

    def _get_block(self, register, length):
        i2c.write(I2C_ADDR, bytearray([register]))
        return i2c.read(I2C_ADDR, length)

    def _write(self, buffer):
        try:
            i2c.write(I2C_ADDR, bytearray(buffer))
            sleep(1)
        except Exception as error:
            print("i2c:", error)

    def _send(self, command, parameters):
        self._write([START_BYTE_1, START_BYTE_2, command, len(parameters)] + parameters)

    def _detect_hardware_version(self):
        warning = "v2?"
        try:
            self._send(CMD_READ, [0])
            sleep(1)
            version = self._get_block(REG_DATA, 3)
            if len(version) == 3 and version != b'\x00\x00\x00':
                self.version = 2
                self._controller_version = "V{}.{}.{}".format(version[0], version[1], version[2])
            else:
                self.version = -1
        except Exception:
            self.version = -1
        if self.version != 2:
            print(warning)
            display.scroll(warning)
            raise RuntimeError(warning)

    def set_motors_speed(self, left_speed, right_speed):
        direction = 0
        left = abs(int(left_speed))
        right = abs(int(right_speed))
        if left_speed < 0:
            direction |= 1
        if right_speed < 0:
            direction |= 2
        self._send(CMD_MOTOR, [2, left, right, direction])

    def set_motor_stop(self, motor):
        if motor not in (MotorSelector.LEFT, MotorSelector.RIGHT, MotorSelector.ALL):
            raise ValueError("motor")
        self._send(CMD_MOTOR, [motor, 0, 0, 0])

    def get_speed(self, motor, speed_unit):
        self._send(CMD_READ, [motor, 0, 0, 0])
        speed = self._get_register(REG_DATA)
        return speed if speed_unit == SpeedUnit.CM_PER_SEC else speed / 2.54

    def _get_rotation_raw(self, motor):
        if motor == MotorSelector.LEFT:
            selector = 3
        elif motor == MotorSelector.RIGHT:
            selector = 4
        else:
            raise ValueError("motor")
        self._send(CMD_READ, [selector])
        sleep(1)
        data = self._get_block(REG_DATA, 4)
        value = data[0] | (data[1] << 8) | (data[2] << 16) | (data[3] << 24)
        if value & 0x80000000:
            value -= 0x100000000
        return value

    def get_rotation(self, motor):
        if motor == MotorSelector.LEFT:
            value = self._get_rotation_raw(MotorSelector.LEFT) - self._left_distance_offset
        elif motor == MotorSelector.RIGHT:
            value = self._get_rotation_raw(MotorSelector.RIGHT) - self._right_distance_offset
        else:
            raise ValueError("motor")
        if value < 0 and value > -2:
            return 0
        return value

    def reset_rotation_degrees(self, motor):
        if motor == MotorSelector.LEFT:
            self._left_distance_offset = self._get_rotation_raw(MotorSelector.LEFT)
        elif motor == MotorSelector.RIGHT:
            self._right_distance_offset = self._get_rotation_raw(MotorSelector.RIGHT)
        elif motor == MotorSelector.ALL:
            self._left_distance_offset = self._get_rotation_raw(MotorSelector.LEFT)
            self._right_distance_offset = self._get_rotation_raw(MotorSelector.RIGHT)
        else:
            raise ValueError("motor")

    def get_distance(self, distance_unit):
        self._echo_pin.read_digital()
        self._trigger_pin.write_digital(1)
        time.sleep_us(10)
        self._trigger_pin.write_digital(0)
        distance = round(time_pulse_us(self._echo_pin, 1, 25000) * 34 / 2 / 1000)
        if distance_unit == DistanceUnit.CENTIMETERS:
            return distance
        if distance_unit == DistanceUnit.INCHES:
            return round(distance / 2.54, 2)

    def set_headlights(self, light, red, green, blue):
        if light not in (LightSelector.LEFT, LightSelector.RIGHT, LightSelector.ALL):
            raise ValueError("light")
        self._send(CMD_LIGHT, [light, abs(red), abs(green), abs(blue)])

    def set_neopixels(self, pixel_index, red, green, blue):
        if pixel_index not in (0, 1):
            raise ValueError("pixel")
        if red < 0 or red > 255 or green < 0 or green > 255 or blue < 0 or blue > 255:
            raise ValueError("rgb")
        self._np[pixel_index] = (red, green, blue)
        self._np.show()

    def set_neopixels_random(self, delay_ms=200):
        if not isinstance(delay_ms, int) or delay_ms < 0:
            raise ValueError("delay")
        now = time.ticks_ms()
        if not hasattr(self, "_random_np_last_update_ms"):
            self._random_np_last_update_ms = now
        if not hasattr(self, "_random_np_next_index"):
            self._random_np_next_index = 0
        if time.ticks_diff(now, self._random_np_last_update_ms) >= delay_ms:
            self._np[self._random_np_next_index] = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
            self._np.show()
            self._random_np_next_index = (self._random_np_next_index + 1) % 2
            self._random_np_last_update_ms = now

    def get_trackbit_state(self):
        self._send(CMD_TRACKBIT, [0])
        sleep(1)
        self.four_way_state_value = self._get_register(REG_DATA)
        return self.four_way_state_value

    def get_offset(self):
        state = self.get_trackbit_state()
        a1 = 1 if ((state >> 0) & 1) == 0 else 0
        a2 = 1 if ((state >> 1) & 1) == 0 else 0
        a3 = 1 if ((state >> 2) & 1) == 0 else 0
        a4 = 1 if ((state >> 3) & 1) == 0 else 0
        total = a1 + a2 + a3 + a4
        if total == 0:
            if hasattr(self, "_last_line_error"):
                return self._last_line_error
            return 0
        if total == 4:
            self._last_line_error = LINE_LOST
            return LINE_LOST
        error = int((a1 * -3000 + a2 * -1000 + a3 * 1000 + a4 * 3000) / total)
        self._last_line_error = error
        return error

    def get_controller_version(self):
        return self._controller_version

    def turn_in_place(self, speed_percent, direction, angle_degrees):
        if not isinstance(speed_percent, (int, float)):
            raise TypeError("speed")
        if not isinstance(direction, str):
            raise TypeError("dir")
        if not isinstance(angle_degrees, (int, float)):
            raise TypeError("angle")
        if speed_percent <= 0 or speed_percent > 100:
            raise ValueError("speed")
        if angle_degrees <= 0:
            raise ValueError("angle")
        direction = direction.lower()
        if direction not in ("left", "right"):
            raise ValueError("dir")
        wheel_diameter_mm = 57.9
        track_width_mm = 91.0
        wheel_circumference_mm = math.pi * wheel_diameter_mm
        turn_fraction = angle_degrees / 360.0
        wheel_travel_mm = math.pi * track_width_mm * turn_fraction
        target_wheel_degrees = int(round((wheel_travel_mm / wheel_circumference_mm) * 360.0))
        drive_speed = int(round(speed_percent))
        self.reset_rotation_degrees(MotorSelector.ALL)
        sleep(20)
        if direction == "left":
            left_speed = -drive_speed
            right_speed = drive_speed
            left_target = -target_wheel_degrees
            right_target = target_wheel_degrees
        else:
            left_speed = drive_speed
            right_speed = -drive_speed
            left_target = target_wheel_degrees
            right_target = -target_wheel_degrees
        while True:
            left_rotation = self.get_rotation(MotorSelector.LEFT)
            right_rotation = self.get_rotation(MotorSelector.RIGHT)
            if direction == "left":
                if left_rotation <= left_target or right_rotation >= right_target:
                    break
            else:
                if left_rotation >= left_target or right_rotation <= right_target:
                    break
            self.set_motors_speed(left_speed, right_speed)
            sleep(10)
        self.set_motor_stop(MotorSelector.ALL)
        sleep(100)


class CutebotProLineController:
    L = -1
    S = 0
    R = 1
    A = 2

    D = 0
    T = 1
    F = 2

    MX = 40
    MN = -55
    SS = 28
    TS = 34
    IL = 8000
    LLT = 700
    ICM = 70
    CNM = 120
    TTM = 1100
    TSM = 80

    def __init__(self, robot):
        if robot is None:
            raise ValueError("robot")
        self.r = robot
        self.le = 0
        self.ie = 0
        self.lve = 0
        self.ab = None
        self.ll = None

    def _d(self, l, r):
        l = max(self.MN, min(self.MX, l))
        r = max(self.MN, min(self.MX, r))
        self.r.set_motors_speed(int(l), int(r))

    def _f(self, ms, sp):
        t = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), t) < ms:
            self._d(sp, sp)
            sleep(10)
        self.r.set_motor_stop(MotorSelector.ALL)

    def _c(self):
        self._f(self.CNM, 24)
        s = self.r.get_trackbit_state() & 15
        a1 = 1 if (s & 1) == 0 else 0
        a2 = 1 if (s & 2) == 0 else 0
        a3 = 1 if (s & 4) == 0 else 0
        a4 = 1 if (s & 8) == 0 else 0
        n = a1 + a2 + a3 + a4
        if n == 0:
            return self.D
        if (a1 or a2) and (a3 or a4):
            return self.F
        return self.T

    def _t(self, d):
        t = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), t) < self.TTM:
            if d == self.L:
                self._d(-self.TS, self.TS)
            elif d == self.R or d == self.A:
                self._d(self.TS, -self.TS)
            else:
                raise ValueError("dir")
            s = self.r.get_trackbit_state() & 15
            if s != 15 and s != 0:
                e = self.r.get_offset()
                self.le = e
                self.lve = e
                sleep(self.TSM)
                return True
            sleep(10)
        self.r.set_motor_stop(MotorSelector.ALL)
        return False

    def _h(self, sp):
        k = self._c()
        if k == self.D:
            self._f(80, -22)
            if not self._t(self.A):
                self.r.set_motor_stop(MotorSelector.ALL)
                sleep(200)
            return
        if k == self.T:
            d = random.choice((self.L, self.R))
        else:
            d = random.choice((self.L, self.R, self.S))
        if d == self.S:
            self._f(180, sp)
        else:
            self._t(d)

    def _s(self):
        if self.ll is None:
            self.ll = time.ticks_ms()
        if time.ticks_diff(time.ticks_ms(), self.ll) > self.LLT:
            self._f(80, -22)
            if not self._t(self.A):
                self.r.set_motor_stop(MotorSelector.ALL)
                sleep(200)
            self.ll = None
            return
        if self.lve < 0:
            self._d(-self.SS, self.SS)
        elif self.lve > 0:
            self._d(self.SS, -self.SS)
        else:
            self._d(self.SS, self.SS)
        sleep(10)

    def pid_follow_step(self, base_speed=30, kp=0.020, ki=0.00002, kd=0.055):
        if not isinstance(base_speed, (int, float)):
            raise TypeError("speed")
        if not isinstance(kp, (int, float)):
            raise TypeError("kp")
        if not isinstance(ki, (int, float)):
            raise TypeError("ki")
        if not isinstance(kd, (int, float)):
            raise TypeError("kd")
        if base_speed < 0:
            raise ValueError("speed")
        s = self.r.get_trackbit_state() & 15
        if s == 15:
            self.ab = None
            self._s()
            return
        self.ll = None
        if s == 0:
            if self.ab is None:
                self.ab = time.ticks_ms()
            elif time.ticks_diff(time.ticks_ms(), self.ab) >= self.ICM:
                self._h(base_speed)
                self.ab = None
            else:
                self._d(base_speed, base_speed)
            return
        self.ab = None
        e = self.r.get_offset()
        self.lve = e
        self.ie += e
        if self.ie < -self.IL:
            self.ie = -self.IL
        elif self.ie > self.IL:
            self.ie = self.IL
        c = kp * e + ki * self.ie + kd * (e - self.le)
        self._d(base_speed + c, base_speed - c)
        self.le = e
        sleep(10)

    def run(self):
        self.r.set_neopixels(0, 0, 255, 0)
        self.r.set_neopixels(1, 0, 255, 0)
        while True:
            try:
                self.pid_follow_step()
            except Exception as error:
                self.r.set_motor_stop(MotorSelector.ALL)
                self.r.set_neopixels(0, 255, 0, 0)
                self.r.set_neopixels(1, 255, 0, 0)
                print("run:", error)
                sleep(500)
