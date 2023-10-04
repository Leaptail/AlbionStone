
import cv2 as cv
import numpy as np
from time import time
from windowcap import window_cap
from githubss import capture_win_alt

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub


# initialize the WindowCapture class
wincap = capture_win_alt('New Tab - Google Chrome')

loop_time = time()
while(True):

    # get an updated image of the game
    screenshot = wincap

    cv.imshow('Computer Vision', screenshot)

    # debug the loop rate
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')

"""

import time
import pyautogui 
import pydirectinput
import cv2 as cv
import numpy as np
import win32gui, win32ui, win32con
from windowcap import window_cap

breakey = 'p'
#haystack_img = cv.imread('farm.PNG', cv.IMREAD_UNCHANGED)
#needle_img = cv.imread('memories/Tree/Tree1.PNG', cv.IMREAD_UNCHANGED)
wincap = window_cap('New Tab - Google Chrome')

while True:

    screenshots = wincap.getssh()
    cv.imshow('Vision', screenshots)

    if cv.waitKey(1) == ord('p'):
        cv.destroyAllWindows()
        break
    
cap.release()
cv.destroyAllWindows()
"""


