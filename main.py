import cv2 as cv
import time
from time import time
from WindowImageCapturing import capturewindow
from VisionBoxes import Vision
from threading import Thread
from botactions import Actions
from detector import Detection

# Terminates program when held
terminalbutton = 'p'

############Insert Name of window here ###########################################################
windowname = 'Albion Online Client'
##################################################################################################

loop_time = time()
detector = Detection()
detector.start()

while(True):

    # get an updated image of the game
    wincap = capturewindow(windowname)
    detector.update(wincap)

    #get items
    PointsScreen = Vision.getPoints(detector.rectangles)
    cv.imshow('Vision',Vision.ProcessImage(wincap,PointsScreen))

    #make new thread for bot

    # loop speed so i can see how shitty the code runs (its pretty decent now)
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    #loop breaker
    if cv.waitKey(1) == ord(terminalbutton):
        detector.stop()
        cv.destroyAllWindows()
        break

print('Finnish.')
