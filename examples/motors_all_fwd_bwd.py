"""
Run both motors simultaneously, forward and backward, and stop both motors.

**How it works:**

This script creates a robot object, drives both motors forward,
then backward, then stops both motors.  Positive speed values
move forward and negative values move backward.
"""
from microbit import sleep  # Import the sleep function from the microbit module.
from cutebot_pro_v2 import CutebotPro, MotorSelector # Import the CutebotPro class and motor constants from the module.

robot = CutebotPro()  # Create a Cutebot Pro robot object.

try:  # Start a try block for basic error handling.
    robot.set_motors_speed(60, 60) # Run both motors forward at 60% speed.    
    sleep(5000)  # Wait for 5 seconds while the robot moves forward.
    robot.set_motors_speed(-60, -60)  # Run both motors backward at 60% speed.
    sleep(5000)  # Wait for 5 seconds while the robot moves backward.
    robot.set_motor_stop(MotorSelector.ALL)  # Stop both motors.
except Exception as error:  # Catch any runtime error.
    print("Motor demo 1 error:", error)  # Print the error message.
    robot.set_motor_stop(MotorSelector.ALL)  # Stop both motors for safety.
