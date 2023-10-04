
import cv2 as cv
import numpy as np
from time import time
from githubss import capture_win_alt

# Terminates program when held
terminalbutton = 'p'

# Insert Name of window here
wincap = capture_win_alt('New Tab - Google Chrome')

loop_time = time()

while(True):

    # get an updated image of the game
    screenshot = wincap

    cv.imshow('Computer Vision', screenshot)

    # debug the loop rate
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    #loop breaker
    if cv.waitKey(1) == ord(terminalbutton):
        cv.destroyAllWindows()
        break

print('Finnish.')
