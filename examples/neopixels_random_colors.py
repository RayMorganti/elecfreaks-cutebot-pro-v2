"""
Repeatedly display random colors on the underside NeoPixels,
until you turn off the robot.
"""

from microbit import sleep
from cutebot_pro_v2 import CutebotPro

robot = CutebotPro() 

while True:  # Run forever.
    robot.set_neopixels_random(200)
    sleep(20) 
