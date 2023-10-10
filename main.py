import cv2 as cv
import time
from WindowImageCapturing import capturewindow
from VisionBoxes import ProcessedImage

# Terminates program when held
terminalbutton = 'p'

############Insert Name of window here ###########################################################
windowname = 'Albion Online Client'
##################################################################################################

loop_time = time()

while(True):

    # get an updated image of the game
    wincap = capturewindow(windowname)

    #show image with boxes
    cv.imshow('v',ProcessedImage(wincap, 'MemoryItems/RoughStone/Rock1.png', 0.5))

    # loop speed so i can see how shitty the code runs (its pretty decent now)
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    #loop breaker
    if cv.waitKey(1) == ord(terminalbutton):
        cv.destroyAllWindows()
        break

print('Finnish.')
