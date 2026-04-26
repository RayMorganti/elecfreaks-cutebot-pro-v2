"""
If you want to see sonar sensor readings in the Shell area of
your code editor, keep the robot connected to your computer.
The script will run both motors at the same time.  They stop
when the sonar sensor detects an object 12 centimeters away.
Distance data from the sonar sensor is printed in the code
editor's Shell.  This will continue until the robt's power
is turned off.
"""

from microbit import sleep 
from cutebot_pro_v2 import CutebotPro, DistanceUnit, MotorSelector

robot = CutebotPro()
stop_distance = 12

try:
    
    while True:  # Start an infinite loop to keep checking the ultrasonic sensor.
        distance = robot.get_distance(DistanceUnit.CENTIMETERS)  # Read the ultrasonic distance in centimeters.
        print(distance)
        if distance > stop_distance:  
            robot.set_motors_speed(50, 50)  # Run both motors forward at 50% speed.
        elif distance > 0 and distance <= stop_distance: # If a valid reading is at or below the stop distance.
            robot.set_motor_stop(MotorSelector.ALL)  # Stop both motors.
            
        sleep(100)  # Wait 100 milliseconds before checking again.
        
except Exception as error:  # Catch any runtime error.
    print("Ultrasonic stop demo error:", error)  # Print the error message.
    robot.set_motor_stop(MotorSelector.ALL)  # Stop both motors for safety.
