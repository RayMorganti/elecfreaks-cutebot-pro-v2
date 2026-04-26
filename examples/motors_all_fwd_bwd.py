"""
Run both motors simultaneously, forward for 5 seconds and 
backward for 5 seconds, then stop both motors.
"""
from cutebot_pro_v2 import CutebotPro, MotorSelector 
from time import sleep

robot = CutebotPro()

try:  # Start a try block for basic error handling.
    robot.set_motors_speed(60, 60) # Run both motors forward at 60% speed.    
    sleep(5)  # Wait for 5 seconds while the robot moves forward.
    robot.set_motors_speed(-60, -60)  # Run both motors backward at 60% speed.
    sleep(5)  # Wait for 5 seconds while the robot moves backward.
    robot.set_motor_stop(MotorSelector.ALL)  # Stop both motors.
except Exception as error:  # Catch any runtime error.
    print("Motor demo 1 error:", error)  # Print the error message.
    robot.set_motor_stop(MotorSelector.ALL)  # Stop both motors for safety.
