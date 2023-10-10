import pydirectinput
from VisionBoxes import Vision
import time

class Actions:
    #def __init__():
    def clickPoint(points):
        if len(points)>0:
            target = points[0]
            pydirectinput.moveTo(x=target[0],y=target[1])
            pydirectinput.click()
            time.sleep(5)