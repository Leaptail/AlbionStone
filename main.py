import cv2 as cv
import time
from time import time
from WindowImageCapturing import capturewindow2
from VisionBoxes import Vision
from threading import Thread
from botactions import Actions
from detector import Detection
from ActiveCapture import capturewindow

# Terminates program when held
terminalbutton = 'p'

############Insert Name of window here ###########################################################
windowname = 'Albion Online Client'
##################################################################################################

loop_time = time()

#Insert image you want to find here.
wincap = capturewindow(windowname)
detector = Detection('MemoryItems/RoughStone/RocknStone.PNG')
bot = Actions((wincap.offsetx,wincap.offsety),(wincap.w,wincap.h),'MemoryItems/RoughStone/RoughStoneTooltop.png')

wincap.start()
detector.start()
bot.start()

while(True):

    # get an updated image of the game
    #wincap = capturewindow(windowname)
    detector.update(wincap.screenshot)

    #get items
    PointsScreen = Vision.getPoints(detector.rectangles)
    bot.update(wincap,PointsScreen)
    cv.imshow('Vision',Vision.ProcessImage(wincap.screenshot,PointsScreen))

    #make new thread for bot

    # loop speed so i can see how shitty the code runs (its pretty decent now)
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    #loop breaker
    if cv.waitKey(1) == ord(terminalbutton):
        detector.stop()
        bot.stop()
        wincap.stop()
        cv.destroyAllWindows()
        break

print('Finnish.')
