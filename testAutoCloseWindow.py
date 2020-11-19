import threading, time, ctypes, ctypes.wintypes, math


WM_CLOSE = 0x0010
MB_OK = 0

# def worker(title,close_until_seconds):
#     time.sleep(close_until_seconds)
#     wd=ctypes.windll.user32.FindWindowA(0,title)
#     ctypes.windll.user32.SendMessageA(wd,0x0010,0,0)
#     return


def find_messagebox(title, threadid, processid):
    hwnd = ctypes.windll.user32.FindWindowA(None, title)
    if hwnd:
        p = ctypes.wintypes.DWORD()
        t = ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
        if p.value == processid and t == threadid:
            return hwnd
    return 0

#danilo callback return True to run again False to stop
def callbackHandler(abort, threadid, processid, title, callbackDelay, callbackFn):
    # give windows some time to create the message box
    time.sleep(math.max(callbackDelay, 0.2))
    while not abort.isSet() and callbackFn():
        time.sleep(callbackDelay)
    hwnd = find_messagebox(title, threadid, processid)
    if not abort.isSet() and hwnd:
        ctypes.windll.user32.PostMessageA(hwnd, WM_CLOSE, 0, 0)

def showWithCallback(text, title, callbackDelay, callbackFn):
    threadid = ctypes.windll.kernel32.GetCurrentThreadId()
    processid = ctypes.windll.kernel32.GetCurrentProcessId()
    abort = threading.Event()
    t = threading.Thread(target=callbackHandler, args=(abort, threadid, processid, title, callbackDelay, callbackFn))
    t.start()
    ctypes.windll.user32.MessageBoxW(0, text, title, MB_HELP | MB_YESNO | ICON_STOP)