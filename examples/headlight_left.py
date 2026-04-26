"""
Turn on the left headlight, and set its color to red.

Turn off the headlight after 10 seconds.
"""

from cutebot_pro_v2 import CutebotPro, LightSelector
from time import sleep

robot = CutebotPro()

try:  # Start a try block for basic error handling.
    robot.set_headlights(LightSelector.LEFT, 255, 0, 0)  # Turn on the left headlight and set it to red.
    sleep(10)  # Keep both headlights green for 10 seconds.
    robot.set_headlights(LightSelector.LEFT, 0, 0, 0)  # Turn off the headlight.
except Exception as error:  # Catch any runtime error.
    print("Headlight demo 1 error:", error)  # Print the error message.
    robot.set_headlights(LightSelector.LEFT, 0, 0, 0)  # Turn off all headlights for safety.
