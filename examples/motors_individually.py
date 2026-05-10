"""
Run the left motor, right motor, both motors, and then stop.

How it works:

The `pwm_cruise_control(left_speed, right_speed)` controls left and right
motors independently.

This script first powers only the left motor, then only the right motor,
then stops everything.  A speed of `0` stops that motor.
"""

from microbit import sleep  # Import the sleep function from the microbit module.
from cutebot_pro_v2 import CutebotPro, MotorSelector  # Import the CutebotPro class and motor constants from the module.

robot = CutebotPro()  # Create a Cutebot Pro robot object.

try:  # Start a try block for basic error handling.
    robot.set_motors_speed(60, 0)  # Run left motor forward at 60% speed.
    sleep(5000)  # Wait for 5 seconds.
    robot.set_motors_speed(0, 60)  # Run the right motor forward at 60% speed.
    sleep(5000)  # Wait for 5 seconds.
    robot.set_motors_speed(60, 60) # Run both motors forward at 60% speed.
    sleep(5000)
    robot.set_motor_stop(MotorSelector.ALL)  # Stop both motors.
except Exception as error:  # Catch any runtime error.
    print("Motor demo 2 error:", error)  # Print the error message.
    robot.set_motor_stop(MotorSelector.ALL)  # Stop both motors for safety.
