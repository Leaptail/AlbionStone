import cv2 as cv
import numpy as np

class Vision:
    def getPoints(rect):
        points=[]
        for(x,y,w,h) in rect:
            pointx = x+int(w/2)
            pointy = y+int(h/2)
            points.append((pointx,pointy))
        return points
    
    def ProcessImage(hay,points):
        if len(points):
        #color and type of line for the point
            markerC = (255,0,255)
            markerT = cv.MARKER_CROSS
            for (pointx,pointy) in points:
                cv.drawMarker(hay,(pointx,pointy),markerC,markerT)
        return hay

    def SimpleSeeItems(hay,need,thresh=0.5,maxresult=10):
        needle = cv.imread(need,cv.IMREAD_UNCHANGED)
        needle_w = needle.shape[1]
        needle_h = needle.shape[0]
        result = cv.matchTemplate(hay,needle,cv.TM_CCOEFF_NORMED)   #compare vision with needle image
        locations = np.where(result >= thresh)                      #gets locations of all the different items above the confidence threshold
        locations = list(zip(*locations[::-1]))                     #turns it into an array of items with x and y coordinates
        rectangles = []
        for loc in locations:                                       #make array of rectangles
            rect = [int(loc[0]),int(loc[1]),needle_w,needle_h]
            rectangles.append(rect)
        rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)#group them together so no overlapping
        if len(rectangles) > maxresult:                             #reduce rectangles to acceptable amounts
            rectangles = rectangles[:maxresult]
        return rectangles