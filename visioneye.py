import time
import pyautogui 
import pydirectinput
import cv2 as cv
import numpy as np

#use by find_obj then insert haystack img (livestream) and needle img(take from memory folder)
# image, object, copnfidence threshold
def Processed(hay,need,thresh):

    #image to find
    needle = cv.imread(need,cv.IMREAD_UNCHANGED)

    #compare vision with needle image
    result = cv.matchTemplate(hay,needle,cv.TM_CCOEFF_NORMED)
 
    #gets locations of all the different items above the confidence threshold
    threshold = thresh
    locations = np.where(result >= threshold)

    #turns it into an array of items with x and y coordinates
    locations = list(zip(*locations[::-1]))

    #basically if locations exist,
    if locations:
        #getting the size and shape of the box to draw the square around
        #takes size of picture in memory
        needle_w = needle.shape[1]
        needle_h = needle.shape[0]

        #color and type of line for the box
        line_color = (255,0,0)
        line_type = cv.LINE_4

        #for loop that draws squares around all the possible locations
        for loc in locations:
            top_left = loc
            bottom_right = (top_left[0]+needle_w,top_left[1]+needle_h)
            hay = cv.rectangle(hay, top_left, bottom_right, line_color, line_type)
    #output the img with the boxes
    cv.imshow('Vision', hay)