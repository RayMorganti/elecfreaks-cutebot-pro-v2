"""
Operate a 180, 270 or 360 degree positional (i.e., non-continuous)
servo connected to one of the robot's two servo ports.  Tested on a
GeekServo 360 degree non-continuous servo.

The following script is designed to control a 360 degree positional
servo connected to servo port S1.

When the script is run:

- the servo shaft rotates to the 90 degree position, then
- rotates to 0 after 5 seconds.

"""

from microbit import sleep
from cutebot_pro_v2 import CutebotPro, ServoPort, ServoType
    
try:
    robot = CutebotPro()
except Exception as error:
    display.scroll("init")
    print(error)

robot.set_positional_servo(ServoType.SERVO_360, ServoPort.S1, 90)
sleep(5000)
robot.set_positional_servo(ServoType.SERVO_360, ServoPort.S1, 0)
