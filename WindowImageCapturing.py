import numpy as np
from ctypes import windll
import win32gui
import win32ui

# captures images from inactive windows : 
# now works!!! on streamed or computers with dedicated gpus

def capturewindow2(window_name: str):
    # Adapted from https://stackoverflow.com/questions/19695214/screenshot-of-inactive-window-printwindow-win32gui

    img = None
    #windll.user32.SetProcessDPIAware()
    hwnd = win32gui.FindWindow(None, window_name)

    #get window size for later
    left, top, right, bottom = win32gui.GetClientRect(hwnd)
    w = right - left
    h = bottom - top

    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()
    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(mfc_dc, w, h)
    save_dc.SelectObject(bitmap)

    # If Special K is running, this number is 3. If not, 1
    result = windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 3)

    bmpinfo = bitmap.GetInfo()
    bmpstr = bitmap.GetBitmapBits(True)
    img = np.fromstring(bmpstr, dtype='uint8')
    img.shape = (bmpinfo["bmHeight"], bmpinfo["bmWidth"], 4)
    #img = np.frombuffer(bmpstr, dtype=np.uint8).reshape((bmpinfo["bmHeight"], bmpinfo["bmWidth"], 4))
    #img = np.ascontiguousarray(img)[..., :-1]  # make image C_CONTIGUOUS and drop alpha channel
    
    win32gui.DeleteObject(bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)
    
    return img