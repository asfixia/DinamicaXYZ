import threading, time, ctypes, ctypes.wintypes, math


class QMessageBox():
    messageBox = ctypes.windll.user32.MessageBoxW
    #setTimer = ctypes.windll.user32.SetTimerW #(NULL, NULL, int(timeout * 1000), NULL)
    IDABORT = 3 #The Abort button was selected.
    IDCONTINUE = 11 #The Continue button was selected.
    IDRETRY = 4 #The Retry button was selected.
    IDTRYAGAIN = 10 #The Try Again button was selected.
    IDYES = 6 #The Yes button was selected.
    Yes = 6
    IDNO = 7 #The No button was selected.
    No = 7
    IDCANCEL = 2 #The Cancel button was selected.
    Cancel = 2
    IDIGNORE = 5 #The Ignore button was selected.
    Discard = 5
    Information = 40
    IDOK = 1 #The OK button was selected.
    Ok = 1

    TOP_MOST = 0x40000
    MB_OK = 0x0
    MB_OKCXL = 0x01
    MB_YESNOCXL = 0x03
    MB_YESNO = 0x04
    MB_HELP = 0x4000
    ICON_EXLAIM = 0x30
    ICON_INFO = 0x40
    ICON_STOP = 0x10

    WM_CLOSE = 0x0010

    message = None
    title = None
    timeout = 1
    callback = None

    @staticmethod
    def find_messagebox(title, threadid, processid):
        hwnd = ctypes.windll.user32.FindWindowW(None, title)
        if hwnd:
            p = ctypes.wintypes.DWORD()
            t = ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
            if p.value == processid and t == threadid:
                return hwnd
        return 0

    @staticmethod
    def setCallback(callback):
        QMessageBox.callback = callback

    @staticmethod
    def setText(message):
        QMessageBox.message = message

    @staticmethod
    def setWindowTitle(title):
        QMessageBox.title = title

    @staticmethod
    def setIcon(icon):
        pass

    @staticmethod
    def setStandardButtons(buttons):
        pass

    @staticmethod
    def exec_():
        threadid = ctypes.windll.kernel32.GetCurrentThreadId()
        processid = ctypes.windll.kernel32.GetCurrentProcessId()
        abort = threading.Event()
        t = threading.Thread(target=QMessageBox.callbackHandler,
                             args=(abort, threadid, processid, QMessageBox.title, QMessageBox.timeout, QMessageBox.callback))
        t.start()
        return QMessageBox.question(None, QMessageBox.title, QMessageBox.message)

    @staticmethod
    def question(nsei, title, msg, defaultButton=None, buttons=None):
        return QMessageBox.messageBox(None, msg, title, 3)

    #danilo callback return True to run again False to stop
    @staticmethod
    def callbackHandler(abort, threadid, processid, title, callbackDelay, callbackFn):
        # give windows some time to create the message box
        time.sleep(max(callbackDelay, 0.2))
        currentTime = max(callbackDelay, 0.2)
        class btnWrapper:
            mustClose = False
            def done(self, state):
                self.mustClose = True
        curBtn = btnWrapper()
        while not curBtn.mustClose and not abort.isSet() and callbackFn(curBtn, currentTime):
            time.sleep(callbackDelay)
            currentTime = currentTime + callbackDelay
        hwnd = QMessageBox.find_messagebox(title, threadid, processid)
        if not abort.isSet() and hwnd:
            ctypes.windll.user32.PostMessageW(hwnd, QMessageBox.WM_CLOSE, 0, 0)

    @staticmethod
    def error(msg, defaultButton=None, buttons=None):
        return QMessageBox.messageBox(None, msg, "Error", 2)




