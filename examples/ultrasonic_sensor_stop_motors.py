"""
Run both motors at the same time.  They stop when the sonar
sensor detects an object 12 centimeters away.  Information
from the sonar sensor is printed in Thonny's shell.

**How it works:**  
The robot motors start moving forward while the code repeatedly
checks information coming from the ultrasonic sensor. When an
object is detected at 12 cm or closer, both motors stop.

A reading of `0` means no valid distance was detected, so
the robot keeps moving.

**Suggestions for further exploration:**
- Place a flat object in front of the robot's sonar sensor
  to confirm the motors stop at the correct distance.
- Change SonarUnit.Centimeters to SonarUnit.Inches, and test again.

"""

from microbit import sleep  
from cutebot_pro_v2 import CutebotPro, DistanceUnit, MotorSelector  

robot = CutebotPro()  
stop_distance = 12  

try:  # Start a try block for basic error handling.
    
    while True:  # Start an infinite loop to keep checking the ultrasonic sensor.
        distance = robot.get_distance(DistanceUnit.CENTIMETERS)  # Read the ultrasonic distance in centimeters.
        print(distance)
        if distance > stop_distance:  
            robot.set_motors_speed(50, 50)  # Run both motors forward at 50% speed.
        elif distance > 0 and distance <= stop_distance: # If a valid reading is at or below the stop distance.
            robot.set_motor_stop(MotorSelector.ALL)  # Stop both motors.
            
        sleep(100)  
        
except Exception as error:  # Catch any runtime error.
    print("Ultrasonic stop demo error:", error)  
    robot.set_motor_stop(MotorSelector.ALL)  # Stop both motors for safety.
    