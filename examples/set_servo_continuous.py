"""
Notes:
- This script is designed for use with a continuous rotation servo.
- Change `ServoPort.S1` to `ServoPort.S2`, `ServoPort.S3`, or
 `ServoPort.S4` if your servo is plugged into a different port.
- In this module, `set_continuous_servo_speed(port, speed)`
  accepts speeds from `-100` to `100`.
- `0` maps to the servo stop position near `1500 µs`, which is the
  typical stop signal for continuous rotation servos for hobby use.
- One sign of speed (+ or -) will produce clockwise rotation and the
  other sign will produce counter-clockwise rotation.
"""

from microbit import sleep
from cutebot_pro_v2 import CutebotPro, ServoPort

robot = CutebotPro()

# Choose the servo port where the continuous rotation
# servo is connected.
servo_port = ServoPort.S1  

# Send the stop command first so the servo starts
# from a safe neutral position.
robot.set_continuous_servo(servo_port, 0)

# Wait 2 seconds to let the servo settle at its stop
# pulse width near 1500 microseconds.
sleep(2000)  

# Run the servo at full speed in one direction using
# the maximum positive speed value.
robot.set_continuous_servo(servo_port, 100)

# Keep the servo turning in that direction for 3 seconds.
sleep(3000)  

# Stop the servo again by sending the neutral speed value.
robot.set_continuous_servo(servo_port, 0)

# Wait 2 seconds so the stop action is easy to observe.
sleep(2000)  

# Run the servo at full speed in the opposite direction
# using the maximum negative speed value.
robot.set_continuous_servo(servo_port, -100)

# Keep the servo turning in the opposite direction for 3 seconds.
sleep(3000)  

# Stop the servo before trying slower speeds.
robot.set_continuous_servo(servo_port, 0)

# Wait 2 seconds so the change in motion is clear.
sleep(2000)  

# Run the servo at about half speed in the positive
# direction.
robot.set_continuous_servo(servo_port, 50)

# Keep the servo turning at this slower speed for
# 3 seconds.
sleep(3000)  

# Stop the servo once more.
robot.set_continuous_servo(servo_port, 0)

# Pause 2 seconds before the final movement.
sleep(2000)  

# Run the servo at about half speed in the negative
# direction.
robot.set_continuous_servo(servo_port, -50)

# Keep the servo turning at this slower reverse speed
#for 3 seconds.
sleep(3000)  

# Stop the servo at the end of the demonstration.
robot.set_continuous_servo(servo_port, 0)
