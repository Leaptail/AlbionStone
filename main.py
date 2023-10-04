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
wincap = window_cap('Albion Online Client')

while True:

    screenshots = wincap.getssh()
    cv.imshow('Vision', screenshots)

    if cv.waitKey(1) == ord('p'):
        cv.destroyAllWindows()
        break
    
cap.release()
cv.destroyAllWindows()

