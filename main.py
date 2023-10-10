import cv2 as cv
import time
from time import time
from WindowImageCapturing import capturewindow2
from VisionBoxes import Vision
from threading import Thread
from botactions import Actions, BotState
from detector import Detection
from ActiveCapture import capturewindow
import win32gui
# Terminates program when held
terminalbutton = 'p'

############Insert Name of window here ###########################################################
windowname = 'Albion Online Client'
##################################################################################################

loop_time = time()

#Insert image you want to find here.
#wincap = capturewindow(windowname)
wincap = capturewindow2(windowname)
hwnd = win32gui.FindWindow(None, windowname)

#get window size for later
left, top, right, bottom = win32gui.GetClientRect(hwnd)
w = right - left
h = bottom - top


detector = Detection('MemoryItems/RoughStone/RocknStone.PNG')
bot = Actions((0,30),(w,h),'MemoryItems/RoughStone/RoughStoneTooltop.png')

#wincap.start()
detector.start()
bot.start()

while(True):

    # get an updated image of the game
    wincap = capturewindow2(windowname)
    #wincap = capturewindow(windowname)
    detector.update(wincap)

    #get items
    PointsScreen = Vision.getPoints(detector.rectangles)
    cv.imshow('Vision',Vision.ProcessImage(wincap,PointsScreen))

    #make new thread for bot
    if bot.state == BotState.INITIAL:
        # while bot is waiting to start, go ahead and start giving it some targets to work
        # on right away when it does start
        Pts = Vision.getPoints(detector.rectangles)
        bot.updatePoints(Pts)
    elif bot.state == BotState.SEARCHING:
        # when searching for something to click on next, the bot needs to know what the click
        # points are for the current detection results. it also needs an updated screenshot
        # to verify the hover tooltip once it has moved the mouse to that position
        Pts = Vision.getPoints(detector.rectangles)
        bot.updatePoints(Pts)
        bot.updateScreenshot(wincap)
    elif bot.state == BotState.MOVING:
        # when moving, we need fresh screenshots to determine when we've stopped moving
        bot.updateScreenshot(wincap)
    elif bot.state == BotState.MINING:
        # nothing is needed while we wait for the mining to finish
        pass

    # loop speed so i can see how shitty the code runs (its pretty decent now)
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    #loop breaker
    if cv.waitKey(1) == ord(terminalbutton):
        detector.stop()
        bot.stop()
        #wincap.stop()
        cv.destroyAllWindows()
        break

print('Finnish.')
