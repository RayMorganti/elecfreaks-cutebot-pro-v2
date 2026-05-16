"""
PID line following using the run() method.
"""

from microbit import display 
from cutebot_pro_v2 import CutebotPro, CutebotProLineController

def main(): 
    robot = CutebotPro()
    display.show("F")
    controller = CutebotProLineController(robot)
    controller.run()

main()
