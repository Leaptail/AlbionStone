import cv2 as cv
import numpy as np
from time import sleep
from time import time
from githubss import capture_win_alt
from visioneye import Processed

# Terminates program when held
terminalbutton = 'p'

############Insert Name of window here ###########################################################
windowname = 'Albion Online Client'
##################################################################################################

loop_time = time()

while(True):

    # get an updated image of the game
    wincap = capture_win_alt(windowname)

    #time to add the green boxes here now
    #points = vision_roughstone.find(wincap, 0.5, 'rectangles')
    #Processed(wincap, 'Rock1.png', 0.6)
    cv.imshow('Vision', wincap)

    
    # loop speed so i can see how shitty the code runs (its pretty decent now)
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    #loop breaker
    if cv.waitKey(1) == ord(terminalbutton):
        cv.destroyAllWindows()
        break

print('Finnish.')
