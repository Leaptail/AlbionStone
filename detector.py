import cv2 as cv
from threading import Thread, Lock
from VisionBoxes import Vision 

class Detection:
    stopped = True
    lock = None
    rectangles = []
    cascade = None
    needle = None
    screenshot = None

    def __init__(self,needle):
        self.lock = Lock()
        #load trained model
        self.needle = needle
        '''self.cascade = cv.CascadeClassifier(filepath)'''

    def update(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            if not self.screenshot is None:
                rectangles = Vision.SimpleSeeItems(self.screenshot,self.needle)
                self.lock.acquire()
                self.rectangles = rectangles
                self.lock.release()

    #def getrect():
