import numpy as np
from ctypes import windll
import win32gui
import win32ui
from threading import Thread,Lock

class capturewindow:
    stopped = True
    lock = None
    screenshot = None
    w = 0
    h = 0
    hwnd = None
    cropx = 0
    cropy = 0 #30px
    offsetx = 0
    offsety = 0
    windowname = None

    def __init__(self, windowname):
        self.lock = Lock()
        self.windowname = windowname
        if self.windowname is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None,windowname)
            if not self.hwnd:
                raise Exception('window not found')
            
        windowrect = win32gui.GetWindowRect(self.hwnd)
        self.w = windowrect[2] - windowrect[0]
        self.h = windowrect[3] - windowrect[1]
        titlebarpixel = 30
        self.h = self.h - titlebarpixel

        self.offsetx = windowrect[0]+self.cropx
        self.offsety = windowrect[1]+self.cropy

    def getscreenshot(self):
            # Adapted from https://stackoverflow.com/questions/19695214/screenshot-of-inactive-window-printwindow-win32gui
        img = None
        #windll.user32.SetProcessDPIAware()
        self.hwnd = win32gui.FindWindow(None, self.windowname)

        #get window size for later
        left, top, right, bottom = win32gui.GetClientRect(self.hwnd)
        w = right - left
        h = bottom - top

        hwnd_dc = win32gui.GetWindowDC(self.hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()
        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(mfc_dc, w, h)
        save_dc.SelectObject(bitmap)

        # If Special K is running, this number is 3. If not, 1
        result = windll.user32.PrintWindow(self.hwnd, save_dc.GetSafeHdc(), 3)

        bmpinfo = bitmap.GetInfo()
        bmpstr = bitmap.GetBitmapBits(True)
        img = np.fromstring(bmpstr, dtype='uint8')
        img.shape = (bmpinfo["bmHeight"], bmpinfo["bmWidth"], 4)
        #img = np.frombuffer(bmpstr, dtype=np.uint8).reshape((bmpinfo["bmHeight"], bmpinfo["bmWidth"], 4))
        #img = np.ascontiguousarray(img)[..., :-1]  # make image C_CONTIGUOUS and drop alpha channel
        
        win32gui.DeleteObject(bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hwnd_dc)
        return img
    
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
            screenshot = self.getscreenshot()
            self.lock.acquire()
            self.screenshot = screenshot
            self.lock.release()