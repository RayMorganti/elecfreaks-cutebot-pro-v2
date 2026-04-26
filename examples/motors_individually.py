"""
Run the left motor for 5 seconds, right motor for 5 seconds,
both motors for 5 seconds, and then stop.
"""
from cutebot_pro_v2 import CutebotPro, MotorSelector
from time import sleep

robot = CutebotPro()

try:  # Start a try block for basic error handling.
    robot.set_motors_speed(60, 0)  # Run left motor forward at 60% speed.
    sleep(5)  # Wait for 5 seconds.
    robot.set_motors_speed(0, 60)  # Run the right motor forward at 60% speed.
    sleep(5)  # Wait for 5 seconds.
    robot.set_motors_speed(60, 60) # Run both motors forward at 60% speed.
    sleep(5)
    robot.set_motor_stop(MotorSelector.ALL)  # Stop both motors.
except Exception as error:  # Catch any runtime error.
    print("Motor demo error:", error)  # Print the error message.
    robot.set_motor_stop(MotorSelector.ALL)  # Stop both motors for safety.
