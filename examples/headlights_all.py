"""
Turn on both headlights and set their colors to purple.
"""

from cutebot_pro_v2 import CutebotPro, LightSelector
from time import sleep

robot = CutebotPro()

try:  # Start a try block for basic error handling.
    robot.set_headlights(LightSelector.ALL, 255, 0, 255)  # Turn on both headlights and set them to purple.
    sleep(10)  # Keep both headlights green for 10 seconds.
    robot.set_headlights(LightSelector.ALL, 0, 0, 0)  # Turn off all headlights.
except Exception as error:  # Catch any runtime error.
    print("Headlight demo 1 error:", error)  # Print the error message.
    robot.set_headlights(LightSelector.ALL, 0, 0, 0)  # Turn off all headlights for safety.
