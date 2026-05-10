"""
Turn on both of the bottom-side NeoPixels, and set their colors.
"""

from microbit import *
from cutebot_pro_v2 import CutebotPro

bot = CutebotPro()

bot.set_neopixels(0,0,255,0)
bot.set_neopixels(1,255,0,0)
sleep(5000)
bot.set_neopixels(0,0,0,0)
bot.set_neopixels(1,0,0,0)
