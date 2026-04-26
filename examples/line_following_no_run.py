"""
Line following for Cutebot Pro without using the
run() method.  The script repeatedly calls
pid_follow_step() in a loop.
"""

from microbit import display, sleep
from cutebot_pro_v2 import CutebotPro, CutebotProLineController, MotorSelector 

def main():  
    robot = None  
    controller = None 

    try:  
        robot = CutebotPro()  
        controller = CutebotProLineController(robot) 
        robot.set_neopixels(0, 0, 255, 0) 
        robot.set_neopixels(1, 0, 255, 0) 
        display.show("F")

        while True: 
            controller.pid_follow_step()

    except Exception as error:  
        if robot is not None: 
            robot.set_motor_stop(MotorSelector.ALL)  
            robot.set_neopixels(0, 255, 0, 0) 
            robot.set_neopixels(1, 255, 0, 0)
        display.show("X") 
        print("Error: {}".format(error)) 
        while True: 
            sleep(1000)

main()  

