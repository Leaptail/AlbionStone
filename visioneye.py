import time
import pyautogui 
import pydirectinput
import cv2 as cv
import numpy as np

"""
result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)
print(result)

threshold = 0.3
locations = np.where(result >= threshold)
print(locations)

locations = list(zip(*locations[::-1]))
print(locations)

if locations:
    print('found')

    needle_w = needle_img.shape[1]
    needle_h = needle_img.shape[0]
    line_color = (255,0,0)
    line_type = cv.LINE_4

    for loc in locations:
        top_left = loc
        bottom_right = (top_left[0]+needle_w,top_left[1]+needle_h)
        cv.rectangle(haystack_img, top_left, bottom_right, line_color, line_type)

    cv.imshow('Result', haystack_img)
    cv.waitKey()
else:
    print('not found')






#Debug code
#cv.imshow('Result', result)
#cv.waitKey()

"""









#min max of brightest and darkest pixel, get best match position
"""min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

print('%s' %str(max_loc))
print('%s' %str(max_val))

threshold = 0.8
if max_val >= threshold:
    print('found')

    #get dimension of needle image
    needle_w = needle_img.shape[1]
    needle_h = needle_img.shape[0]

    top_left = max_loc
    bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)

    cv.rectangle(haystack_img, top_left, bottom_right, color=(255,0,0), thickness=2, lineType=cv.LINE_4)
    print('%d , %d' % top_left, bottom_right)

    cv.imshow('Result', haystack_img)
    cv.waitKey()

else:
    print('none')"""