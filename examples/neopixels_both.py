"""
On the underside of the robot, set the left neopixel
to green and the right neopixel to red.  Turn them
off after 5 seconds.
"""

from cutebot_pro_v2 import CutebotPro
from time import sleep

bot = CutebotPro()

bot.set_neopixels(0,0,255,0)
bot.set_neopixels(1,255,0,0)
sleep(5)
bot.set_neopixels(0,0,0,0)
bot.set_neopixels(1,0,0,0)

