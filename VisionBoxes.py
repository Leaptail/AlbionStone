import time
import pyautogui 
import pydirectinput
import cv2 as cv
import numpy as np

#use by find_obj then insert haystack img (livestream) and needle img(take from memory folder)
# image, object, copnfidence threshold
def ProcessedImage(hay,need,thresh,maxresult=10):

    #image to find
    #getting the size and shape of the box to draw the square around
    needle = cv.imread(need,cv.IMREAD_UNCHANGED)
    needle_w = needle.shape[1]
    needle_h = needle.shape[0]

    #compare vision with needle image
    result = cv.matchTemplate(hay,needle,cv.TM_CCOEFF_NORMED)
 
    #gets locations of all the different items above the confidence threshold
    threshold = thresh
    locations = np.where(result >= threshold)

    #turns it into an array of items with x and y coordinates
    locations = list(zip(*locations[::-1]))
    rectangles = []

    #make array of rectangles
    for loc in locations:
        rect = [int(loc[0]),int(loc[1]),needle_w,needle_h]
        rectangles.append(rect)

    #group them together so no overlapping
    rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)

    #reduce rectangles to acceptable amounts
    if len(rectangles) > maxresult:
        rectangles = rectangles[:maxresult]

    #basically if locations exist,
    if len(rectangles):
        #color and type of line for the point
        markerC = (255,0,255)
        markerT = cv.MARKER_CROSS

        #for loop that draws points around all the possible locations
        for (x,y,w,h) in rectangles:
            cv.drawMarker(hay,(x+int(w/2),y+int(h/2)),markerC,markerT)

    #output the img with the boxes
    return hay