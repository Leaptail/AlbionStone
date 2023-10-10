import pydirectinput
from VisionBoxes import Vision
from threading import Thread, Lock
from time import time
import cv2 as cv
from math import sqrt

class BotState:
    INITIAL = 0
    SEARCH = 1
    MOVE = 2
    MINE = 3

class Actions:
    stopped = True
    lock = None
    points = []
    state = None
    screenshot = None
    prevscreen = None
    tooltipimage = None
    timestamp = None
    INITIALs = 6
    MINEs = 10
    threshold = 0.95
    windowoffset = (0,0)
    windoww = 0
    windowh = 0
    IGNOREradii = 130
    TTthresh = 0.95

    def __init__(self, windowoffset, windowsize, tooltipimage):
        self.lock = Lock()
        self.state = BotState.INITIAL
        self.timestamp = time()
        self.windowoffset = windowoffset
        self.windoww = windowsize[0]
        self.windowh = windowsize[1]
        self.tooltipimage = tooltipimage

    def stoppedmoving(self):
        if self.prevscreen is None:
            self.prevscreen = self.screenshot.copy()
            return False
        result = cv.matchTemplate(self.screenshot,self.prevscreen,cv.TM_CCOEFF_NORMED)
        similarity = result[0][0]
        if similarity>=self.threshold:
            return True
        self.prevscreen = self.screenshot.copy()
        return False

    def updateScreenshot(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def updatePoints(self, points):
        self.lock.acquire()
        self.points = points
        self.lock.release()
    
    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def ScreenOffset(self,pos):
        return (pos[0]+self.windowoffset[0],pos[1]+self.windowoffset[1])

    def targetsbydistance(self,targets):
        mypos = (self.windoww/2,self.windowh/2)
        def pythagoreandist(pos):
            return sqrt((pos[0]-mypos[0])**2+(pos[1]-mypos[1])**2)
        targets.sort(key=pythagoreandist)
        return targets
    
    def confirmtooltip(self):
        result = cv.matchtemplate(self.screenshot,self.tooltipimage,cv.TM_CCOEFF_NORMED)
        minV,maxV,minL,maxL = cv.minMaxLoc(result)
        if maxV>=self.TTthresh:
            return True
        return False

    def clicknextPoint(self):
        if len(self.points)>0:
            targets = self.targetsbydistance(self.points)
            targeti = 0
            found = False
            while not found and targeti <  len(self.points):
                if self.stopped:
                    break
                target = self.points[targeti]
                pydirectinput.moveTo(x=target[0],y=target[1])
                time.sleep(1)
                if self.confirmtooltip():
                    found = True
                    pydirectinput.click()
                targeti +=1
            return found

    def run(self):
        while not self.stopped:
            if self.state == BotState.INITIAL:
                if time() > self.timestamp+self.INITIALs:
                    self.lock.acquire()
                    self.state = BotState.SEARCH
                    self.lock.release()
            elif self.state == BotState.SEARCH:
                success = self.clicknextPoint()
                if not success:
                    success = self.clicknextPoint()
                if success:
                    self.lock.acquire()
                    self.state = BotState.MOVE
                    self.lock.release()
                else:
                    pass
            elif self.state == BotState.MOVE:
                if not self.stoppedmoving():
                    time.sleep(0.5)
                else:
                    self.lock.acquire()
                    self.state = BotState.MINE
                    self.lock.release()
            elif self.state == BotState.MINE:
                if time()>self.timestamp+self.MINEs:
                    self.lock.acquire()
                    self.state = BotState.SEARCH
                    self.lock.release()

        