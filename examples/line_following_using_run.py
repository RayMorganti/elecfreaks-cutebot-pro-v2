"""
Cutebot Pro line following using the run() method, which
allows a simpler script.  The run function includes a
loop that repeatedly calls pid_follow_step().
"""

from microbit import display 
from cutebot_pro_v2 import CutebotPro, CutebotProLineController

def main(): 
    robot = CutebotPro()
    display.show("F")
    controller = CutebotProLineController(robot)
    controller.run()

main() 
