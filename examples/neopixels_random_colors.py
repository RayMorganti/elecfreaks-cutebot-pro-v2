"""
Repeatedly display random colors in the underside NeoPixels.

How it works:
- The set_neopixels_random() method is called repeatedly is this
  script's **while** loop.
- The method called by this script is non-blocking.
- Each time you call the method, it checks whether `delay_ms` has
  elapsed.
- If enough time has passed, the method updates one NeoPixel with
  a random colour, then switches to the other NeoPixel for the
  next call.
"""

from microbit import *
from cutebot_pro_v2 import CutebotPro

robot = CutebotPro()  # Create a robot instance.

while True:  # Run forever.
    robot.set_neopixels_random(200)
    sleep(20)  
