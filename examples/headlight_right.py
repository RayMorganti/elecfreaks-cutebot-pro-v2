"""
Turn on the right headlight, and set its color to blue.

Turn off the headlight after 10 seconds.
"""

from cutebot_pro_v2 import CutebotPro, LightSelector
from time import sleep

robot = CutebotPro()

try:  # Start a try block for basic error handling.
    robot.set_headlights(LightSelector.RIGHT, 0, 0, 255)  # Turn on the right headlight and set it to blue.
    sleep(10)  # Keep both headlights green for 10 seconds.
    robot.set_headlights(LightSelector.RIGHT, 0, 0, 0)  # Turn off the headlight.
except Exception as error:  # Catch any runtime error.
    print("Headlight demo 1 error:", error)  # Print the error message.
    robot.set_headlights(LightSelector.RIGHT, 0, 0, 0)  # Turn off the headlight for safety.
