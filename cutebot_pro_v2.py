from microbit import i2c, sleep, pin8, pin12, pin15, display
from machine import time_pulse_us
import time
import neopixel
import random

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
            print("I2C write error: {}".format(error))

    def _send(self, command, parameters):
        self._write([START_BYTE_1, START_BYTE_2, command, len(parameters)] + parameters)

    def _detect_hardware_version(self):
        warning = "Cutebot Pro v2 not confirmed."
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
            display.scroll("V2 NOT CONFIRMED")
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
            raise ValueError("motor must be MotorSelector.LEFT, MotorSelector.RIGHT, or MotorSelector.ALL")
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
            raise ValueError("motor must be MotorSelector.LEFT or MotorSelector.RIGHT")
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
            raise ValueError("motor must be MotorSelector.LEFT or MotorSelector.RIGHT")

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
            raise ValueError("motor must be MotorSelector.LEFT, MotorSelector.RIGHT, or MotorSelector.ALL")

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
            raise ValueError("light must be LightSelector.LEFT, LightSelector.RIGHT, or LightSelector.ALL")
        self._send(CMD_LIGHT, [light, abs(red), abs(green), abs(blue)])

    def set_neopixels(self, pixel_index, red, green, blue):
        if pixel_index not in (0, 1):
            raise ValueError("pixel_index must be 0 or 1")
        if red < 0 or red > 255 or green < 0 or green > 255 or blue < 0 or blue > 255:
            raise ValueError("RGB values must be in range 0..255")
        self._np[pixel_index] = (red, green, blue)
        self._np.show()

    def set_neopixels_random(self, delay_ms=200):
        if not isinstance(delay_ms, int) or delay_ms < 0:
            raise ValueError("delay_ms must be an integer >= 0")

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
        active_1 = 1 if ((state >> 0) & 1) == 0 else 0
        active_2 = 1 if ((state >> 1) & 1) == 0 else 0
        active_3 = 1 if ((state >> 2) & 1) == 0 else 0
        active_4 = 1 if ((state >> 3) & 1) == 0 else 0
        total = active_1 + active_2 + active_3 + active_4

        if total == 0:
            if hasattr(self, "_last_line_error"):
                return self._last_line_error
            return 0

        if total == 4:
            self._last_line_error = LINE_LOST
            return LINE_LOST

        error = int((active_1 * -3000 + active_2 * -1000 + active_3 * 1000 + active_4 * 3000) / total)
        self._last_line_error = error
        return error

    def get_controller_version(self):
        return self._controller_version

class CutebotProLineController:
    LEFT = -1
    STRAIGHT = 0
    RIGHT = 1
    AROUND = 2

    DEAD_END = 0
    T_INTERSECTION = 1
    FOUR_WAY = 2

    MAX_SPEED = 40
    MIN_SPEED = -55
    SEARCH_SPEED = 28
    TURN_SPEED = 34
    INTEGRAL_LIMIT = 8000
    LOST_LINE_TIMEOUT_MS = 700
    INTERSECTION_CONFIRM_MS = 70
    CENTER_ON_NODE_MS = 120
    TURN_TIMEOUT_MS = 1100
    TURN_SETTLE_MS = 80

    def __init__(self, robot):
        if robot is None:
            raise ValueError("robot must not be None")
        self.robot = robot
        self.last_error = 0
        self.integral_error = 0
        self.last_valid_error = 0
        self.all_black_started_ms = None
        self.lost_line_started_ms = None

    def _set_drive(self, left_speed, right_speed):
        if left_speed < self.MIN_SPEED:
            left_speed = self.MIN_SPEED
        elif left_speed > self.MAX_SPEED:
            left_speed = self.MAX_SPEED

        if right_speed < self.MIN_SPEED:
            right_speed = self.MIN_SPEED
        elif right_speed > self.MAX_SPEED:
            right_speed = self.MAX_SPEED

        self.robot.set_motors_speed(int(left_speed), int(right_speed))

    def _drive_forward_for(self, duration_ms, speed_value):
        start_ms = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start_ms) < duration_ms:
            self._set_drive(speed_value, speed_value)
            sleep(10)
        self.robot.set_motor_stop(MotorSelector.ALL)

    def _classify_intersection(self):
        self._drive_forward_for(self.CENTER_ON_NODE_MS, 24)
        state = self.robot.get_trackbit_state() & 0x0F
        active_1 = 1 if (state & 0x01) == 0 else 0
        active_2 = 1 if (state & 0x02) == 0 else 0
        active_3 = 1 if (state & 0x04) == 0 else 0
        active_4 = 1 if (state & 0x08) == 0 else 0
        active_count = active_1 + active_2 + active_3 + active_4
        if active_count == 0:
            return self.DEAD_END
        if (active_1 or active_2) and (active_3 or active_4):
            return self.FOUR_WAY
        return self.T_INTERSECTION

    def _find_line_after_turn(self, direction):
        start_ms = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start_ms) < self.TURN_TIMEOUT_MS:
            if direction == self.LEFT:
                self._set_drive(-self.TURN_SPEED, self.TURN_SPEED)
            elif direction == self.RIGHT:
                self._set_drive(self.TURN_SPEED, -self.TURN_SPEED)
            elif direction == self.AROUND:
                self._set_drive(self.TURN_SPEED, -self.TURN_SPEED)
            else:
                raise ValueError("direction must be LEFT, RIGHT, or AROUND")

            state = self.robot.get_trackbit_state() & 0x0F
            if state != 0x0F and state != 0x00:
                error_value = self.robot.get_offset()
                self.last_error = error_value
                self.last_valid_error = error_value
                sleep(self.TURN_SETTLE_MS)
                return True
            sleep(10)

        self.robot.set_motor_stop(MotorSelector.ALL)
        return False

    def _handle_intersection(self, base_speed):
        intersection_type = self._classify_intersection()

        if intersection_type == self.DEAD_END:
            self._drive_forward_for(80, -22)
            if not self._find_line_after_turn(self.AROUND):
                self.robot.set_motor_stop(MotorSelector.ALL)
                sleep(200)
            return

        if intersection_type == self.T_INTERSECTION:
            direction = random.choice((self.LEFT, self.RIGHT))
        else:
            direction = random.choice((self.LEFT, self.RIGHT, self.STRAIGHT))

        if direction == self.STRAIGHT:
            self._drive_forward_for(180, base_speed)
        else:
            self._find_line_after_turn(direction)

    def _search_for_line(self):
        if self.lost_line_started_ms is None:
            self.lost_line_started_ms = time.ticks_ms()

        if time.ticks_diff(time.ticks_ms(), self.lost_line_started_ms) > self.LOST_LINE_TIMEOUT_MS:
            self._drive_forward_for(80, -22)
            if not self._find_line_after_turn(self.AROUND):
                self.robot.set_motor_stop(MotorSelector.ALL)
                sleep(200)
            self.lost_line_started_ms = None
            return

        if self.last_valid_error < 0:
            self._set_drive(-self.SEARCH_SPEED, self.SEARCH_SPEED)
        elif self.last_valid_error > 0:
            self._set_drive(self.SEARCH_SPEED, -self.SEARCH_SPEED)
        else:
            self._set_drive(self.SEARCH_SPEED, self.SEARCH_SPEED)

        sleep(10)

    def pid_follow_step(self, base_speed=30, kp=0.020, ki=0.00002, kd=0.055):
        if not isinstance(base_speed, (int, float)):
            raise TypeError("base_speed must be numeric")
        if not isinstance(kp, (int, float)):
            raise TypeError("kp must be numeric")
        if not isinstance(ki, (int, float)):
            raise TypeError("ki must be numeric")
        if not isinstance(kd, (int, float)):
            raise TypeError("kd must be numeric")
        if base_speed < 0:
            raise ValueError("base_speed must be >= 0")

        state = self.robot.get_trackbit_state() & 0x0F

        if state == 0x0F:
            self.all_black_started_ms = None
            self._search_for_line()
            return

        self.lost_line_started_ms = None

        if state == 0x00:
            if self.all_black_started_ms is None:
                self.all_black_started_ms = time.ticks_ms()
            elif time.ticks_diff(time.ticks_ms(), self.all_black_started_ms) >= self.INTERSECTION_CONFIRM_MS:
                self._handle_intersection(base_speed)
                self.all_black_started_ms = None
            else:
                self._set_drive(base_speed, base_speed)
            return

        self.all_black_started_ms = None
        error_value = self.robot.get_offset()
        self.last_valid_error = error_value
        self.integral_error += error_value

        if self.integral_error < -self.INTEGRAL_LIMIT:
            self.integral_error = -self.INTEGRAL_LIMIT
        elif self.integral_error > self.INTEGRAL_LIMIT:
            self.integral_error = self.INTEGRAL_LIMIT

        correction = (
            kp * error_value +
            ki * self.integral_error +
            kd * (error_value - self.last_error)
        )
        self._set_drive(base_speed + correction, base_speed - correction)
        self.last_error = error_value
        sleep(10)

   def run(self):
        self.robot.set_neopixels(0, 0, 255, 0)
        self.robot.set_neopixels(1, 0, 255, 0)

        while True:
            try:
                self.pid_follow_step()
            except Exception as error:
                self.robot.set_motor_stop(MotorSelector.ALL)
                self.robot.set_neopixels(0, 255, 0, 0)
                self.robot.set_neopixels(1, 255, 0, 0)
                print("Runtime error: {}".format(error))
                sleep(500)
