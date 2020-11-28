#!/usr/bin/python
# -*- coding: utf-8 -*-

# #Hack para corrigir o problema com o defaultencoding, dessa maneira funciona em qualquer computador que possua o encoding 'utf-8'.
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

version = '0.1'

import os
import json
from pathlib import Path
import webbrowser
# import sys
# import importlib
# # importlib.reload(sys)
# # sys.setdefaultencoding('UTF8')


isDinamica = False
try:
    dinamica.package("os")
    isDinamica = True
except:
    isDinamica = False


try:
    from osgeo import ogr, osr, gdal
except:
    import tempfile
    import shutil

    if isDinamica:
        print("Installing python GDAL")
        dinamica.package("wheel==0.33.6", None, "wheel")
        dinamica.package("wget==3.2", None, "wget")
        directory = tempfile.mkdtemp()
        gdalCompiledFile = os.path.join(directory, 'GDAL-2.4.1-cp37-cp37m-win_amd64.whl')
        wget.download("https://github.com/asfixia/rasterstats_wheel/raw/master/GDAL-2.4.1-cp37-cp37m-win_amd64.whl", gdalCompiledFile)
        dinamica.package("gdal", gdalCompiledFile)
        os.remove(gdalCompiledFile)

os.environ['GIT_PYTHON_REFRESH'] = 'quiet'
if isDinamica:
    dinamica.package("requests")
    dinamica.package("GitPython", None, "git")
    dinamica.package("xmltodict")
    dinamica.package("Pillow", None, "PIL")
else:
    import requests, xmltodict
    import git
    import PIL

try:
    import QMessageBox
except:
    pass

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







class Feedback():
    @staticmethod
    def pushConsoleInfo(message):
        print(message)

    @staticmethod
    def setProgress(percentage):
        print("Progress: " + str(percentage))

    @staticmethod
    def setProgressText(message):
        print(message)

    @staticmethod
    def isCanceled():
        return False




try:
    from colorize_rgb import applyLegendCsv, applyLegend, readLegend, prepareLegend
except:
    pass #Not in Dinamica Code

# try:
#     dinamica.package("PyPNG", None, "png")
# except:
#     pass
#
# import png
#
# s = ['110010010011',
#      '101011010100',
#      '110010110101',
#      '100010010011']
# s = [[int(c) for c in row] for row in s]
#
# palette=[(0x55,0x55,0x55), (0xff,0x99,0x99)]
# w = png.Writer(len(s[0]), len(s), palette=palette, bitdepth=1)
# f = open('png.png', 'wb')
# w.write(f, s)


from PIL import Image
import csv



class LegendEntry:
    def __init__(self, category, fromValue, toValue, categoryName, red, green, blue):
        self.category = int(category)
        self.fromValue = float(fromValue)
        self.toValue = float(toValue)
        self.categoryName = categoryName
        self.red = int(red)
        self.green = int(green)
        self.blue = int(blue)

    def getRGBA(self):
        return (self.red, self.green, self.blue, 255)

def applyLegend(pngPath, legendObj):
    with Image.open(pngPath) as im:
        im.convert('RGBA')
        background = Image.new("RGBA", (256, 256), (0, 0, 0, 255))
        pixdata = im.load()
        toData = background.load()

        width = 256
        height = 256
        for y in range(height):
            for x in range(width):
                curValue = pixdata[x, y][0] #+ pixdata[x, y][1]
                if pixdata[x, y] == (0, 0):
                    toData[x, y] = (0, 0, 0, 0)
                else:
                    toData[x, y] = getLegendForValue(curValue, legendObj).getRGBA()
        background.save(pngPath, "PNG")

def readLegend(csvPath):
    return prepareLegend([a for a in csv.reader(open(csvPath, "r", encoding="utf-8"), escapechar='\\',
                                 skipinitialspace=False, delimiter=',', quoting=csv.QUOTE_NONE)])

def applyLegendCsv(pngPath, legendPath):
    return applyLegend(pngPath, readLegend(legendPath))

def prepareLegend(csvLegend):
    result = []
    i = 0
    headTmp = csvLegend.pop(0)
    if not (len(headTmp) >= 7 and 'category' in headTmp[0].lower() and 'from' in headTmp[1].lower() and 'to' in headTmp[2].lower()
            and 'category_name' in headTmp[3].lower() and 'red' in headTmp[4].lower() and 'green' in headTmp[5].lower()
            and 'blue' in headTmp[6].lower()):
        raise Exception("The CSV Style is invalid please confirm the Fields: 'Category*', ' From', ' To', ' Category_Name', ' red', ' green', ' blue'")
    for elm in csvLegend:
        result.append(LegendEntry(elm[0], elm[1], elm[2], elm[3], elm[4], elm[5], elm[6]))
    return result

#Category*, From, To, Category_Name, red, green, blue,
def getLegendForValue(value, legend):
    return [l for l in legend if l.category == value][0]

# # # # dialect = csv.Dialect()
# # # # dialect.skipinitialspace = True
# # # # dialect.delimiter = ','
# # # # dialect.quoting = '"'
# # # # dialect.escapechar = '\\'
# # applyLegend(pngPath, prepareLegend(csv.DictReader(open('I:\\Danilo\\Trampo\\data_dir\\data\\laurel\\land_use_1992_2015\\land_use_1992_2015_7.sld', "r", encoding="utf-8"), escapechar='\\', skipinitialspace=False, delimiter=',', quoting=csv.QUOTE_NONE)))
# sldPath = 'I:\\Danilo\\Trampo\\data_dir\\data\\laurel\\land_use_1992_2015\\land_use_1992_2015_7.sld'
# pngPath = "C:\\Users\\Danilo\\AppData\\Local\\Temp\\outputDir\\iyield_rubber2\\1\\rgba\\4\\0005_0007.png"
# applyLegendCsv(pngPath, sldPath)


try:
    from UTILS import UTILS
except:
    pass #Not in Dinamica Code

import re
import time
import math
import os
import unicodedata
import tempfile
from http import HTTPStatus
from urllib.parse import urlencode
import requests
from xml.sax.saxutils import escape
from zipfile import ZipFile

isDinamica = False
try:
    dinamica.package("os")
    isDinamica = True
except:
    isDinamica = False

try:
    from QMessageBox import QMessageBox
except:
    pass #Not in Dinamica Code

try:
    from qgis.PyQt.QtWidgets import QMessageBox
    from qgis.PyQt.QtCore import QTimer
    from qgis.core import (QgsProject, QgsCoordinateTransform, QgsMessageLog, QgsVectorLayer, QgsRasterLayer)
except:
    pass #Not in QGIS

import random
import string

class UTILS:

    #Danilo o zip precisa deletar dps
    @staticmethod
    def zipFiles(dir, pattern):
        curTmpFile = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
        compPattern = re.compile(pattern)
        # create a ZipFile object
        with ZipFile(curTmpFile, 'w') as zipObj:
            # Iterate over all the files in directory
            for folderName, subfolders, filenames in os.walk(dir):
                for filename in filenames:
                    if not compPattern.match(filename):
                        continue
                    # create complete filepath of file in directory
                    filePath = os.path.join(folderName, filename)
                    # Add file to zip
                    zipObj.write(filePath, os.path.basename(filePath))
            return curTmpFile
        return None

    @staticmethod
    def getFileSize(dir, pattern):
        total = 0
        compPattern = re.compile(pattern)
        for folderName, subfolders, filenames in os.walk(dir):
            for filename in filenames:
                if not compPattern.match(filename):
                    continue
                filePath = os.path.join(folderName, filename)
                if os.path.isfile(filePath):
                    total = total + os.path.getsize(filePath)
        return total

    @staticmethod
    def checkForCanceled(feedback, msg='Cancelling'):
        if feedback.isCanceled():
            feedback.pushConsoleInfo(msg)
            raise Exception("User canceled the plugin execution.")

    #Danilo //Danilo return a  TemporaryFile when works
    #Danilo o zip precisa deletar
    @staticmethod
    def generateZipLayer(layer):
        print("Generating zip for " + layer.name() + " layer.")
        sourceUri = layer.dataProvider().dataSourceUri()
        absolutePath = None
        if isinstance(layer, QgsRasterLayer):
            if '.tiff' in sourceUri:
                absolutePath = sourceUri[:(sourceUri.index(".tiff") + 5)]
            elif '.tif' in sourceUri:
                absolutePath = sourceUri[:(sourceUri.index(".tif") + 4)]
            else:
                print("Only tiff and tif is allowable to download.")
        elif isinstance(layer, QgsVectorLayer):
            if '.shp' in sourceUri:
                absolutePath = sourceUri[:(sourceUri.index(".shp") + 4)]
            else:
                print("Only shp file is allowable to download.")
        if absolutePath is not None:
            fileName = os.path.basename(absolutePath)
            fileNameWithoutExt = os.path.splitext(fileName)[0]
            dirName = os.path.dirname(absolutePath)
            zipFile = UTILS.zipFiles(dirName + os.path.sep, fileNameWithoutExt + "*")
            zipFile.close()
            if os.path.getsize(zipFile.name) > 2e9:
                print("The map filesize is greater than the GitHub 2Gb limit. (all files in this folder starting with " + fileNameWithoutExt + " were included.")
            else:
                return zipFile
        return None


    @staticmethod
    def runLongTask(function, feedback, waitMessage="Please Wait", secondsReport=60, *args, **kwArgs):
        from concurrent import futures
        # feedback.setProgress(1)
        stepTimer = 0.5
        totalTime = 0
        with futures.ThreadPoolExecutor(max_workers=1) as executor:
            job = executor.submit(function, *args, **kwArgs)
            elapsedTime = 0
            while job.done() == False:
                time.sleep(stepTimer)
                elapsedTime = elapsedTime + stepTimer
                totalTime = totalTime + stepTimer
                if elapsedTime > secondsReport:
                    cancelMsg = "\nCancelling, please wait the current step to finish gracefully." if feedback.isCanceled() else ''
                    feedback.pushConsoleInfo("Elapsed " + str(round(totalTime)) + "s: " + waitMessage + cancelMsg)
                    elapsedTime = 0
                # if canCancelNow and feedback.isCanceled():
                #     feedback.pushConsoleInfo("Job starting to cancel.")
                #     job.cancel()
            feedback.pushConsoleInfo("Elapsed " + str(round(totalTime)) + "s on this step.")
            # UTILS.checkForCanceled(feedback)
            return job.result()

    """
    Use safer names.
    """
    @staticmethod
    def normalizeName(name, isFilename=True, escapeXml=True, removeAccents=True):
        normalized = name
        if escapeXml:
            normalized = UTILS.escapeXml(normalized)
        if removeAccents:
            normalized = UTILS.strip_accents(normalized)
        if isFilename:
            normalized = UTILS.escapeFilename(normalized)
        return normalized.lower()

    @staticmethod
    def escapeFilename(content):
        return re.sub(r"\W", "_", content)

    #https://pynative.com/python-generate-random-string/
    @staticmethod
    def randomString(stringLength=27):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))

    @staticmethod
    def sendReport(dictParam):
        req = requests.get(url='http://csr.ufmg.br/imagery/save_reports.php?' + urlencode(dictParam))
        if req.status_code == HTTPStatus.OK:
            return req.text
        else:
            return ''

    #Return the map extents in the given projection
    @staticmethod
    def getMapExtent(layer, projection):
        mapExtent = layer.extent()
        projection.validate()
        layer.crs().validate()
        src_to_proj = QgsCoordinateTransform(layer.crs(), projection, QgsProject.instance().transformContext() if getattr(layer, "transformContext", None) is None else layer.transformContext())
        return src_to_proj.transformBoundingBox(mapExtent)

    @staticmethod
    def escapeXml(content):
        return escape(content)

    @staticmethod
    def strip_accents(s):
       return ''.join(c for c in unicodedata.normalize('NFD', s)
                      if unicodedata.category(c) != 'Mn')

    # TMS functions taken from https://alastaira.wordpress.com/2011/07/06/converting-tms-tile-coordinates-to-googlebingosm-tile-coordinates/ #spellok
    @staticmethod
    def tms(ytile, zoom):
        n = 2.0 ** zoom
        ytile = n - ytile - 1
        return int(ytile)

    # Math functions taken from https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames #spellok
    @staticmethod
    def deg2num(lat_deg, lon_deg, zoom):
        QgsMessageLog.logMessage(" e ".join([str(lat_deg), str(lon_deg), str(zoom)]), tag="Processing")
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** zoom
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
        return (xtile, ytile)

    # Math functions taken from https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames #spellok
    @staticmethod
    def num2deg(xtile, ytile, zoom):
        n = 2.0 ** zoom
        lon_deg = xtile / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
        lat_deg = math.degrees(lat_rad)
        return (lat_deg, lon_deg)

    # This function gets a system variable
    # it was necessary to use this instead of os.environ["PATH"] because QGIS overwrites the path variable
    # the win32 libraries appear not to be part of the standard python install, but they are included in the
    # python version that comes with QGIS
    @staticmethod
    def getenv_system(varname, default=''):
        try:
            import os
            import win32api
            import win32con
            v = default
            try:
                rkey = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,
                                           'SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment')
                try:
                    v = str(win32api.RegQueryValueEx(rkey, varname)[0])
                    v = win32api.ExpandEnvironmentStrings(v)
                except:
                    pass
            finally:
                win32api.RegCloseKey(rkey)
            return v
        except:
            return ''

    @staticmethod
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    # https://stackoverflow.com/questions/377017/test-if-executable-exists-in-python/12611523
    @staticmethod
    def which(program):
        fpath, fname = os.path.split(program)
        if fpath:
            if UTILS.is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                exe_file = os.path.join(path, program)
                if UTILS.is_exe(exe_file):
                    return exe_file
            for path in UTILS.getenv_system("PATH").split(os.pathsep):
                exe_file = os.path.join(path, program)
                if UTILS.is_exe(exe_file):
                    return exe_file

        return None

class UserInterrupted(Exception):
    pass

# class TimedMessageBox(QMessageBox):
#     def __init__(self, timeout, message, callback):
#         super(TimedMessageBox, self).__init__()
#         self.timeout = timeout
#         self.callback = callback
#
#     def intervalCallback(self):
#         self.callback()
#         QTimer().singleShot(self.timeout*1000, self.intervalCallback)
#
#     def showEvent(self, event):
#         QTimer().singleShot(self.timeout*1000, self.intervalCallback)
#         super(TimedMessageBox, self).showEvent(event)


try:
    from GitHub import GitHub
except:
    pass #Not in Dinamica Code

import re
import os
import random
import webbrowser
import requests
import time
import json
import glob
import tempfile
import platform
import subprocess
from http import HTTPStatus
from requests import request
from datetime import datetime
from time import sleep



isDinamica = False
try:
    dinamica.package("os")
    isDinamica = True
except:
    isDinamica = False

try:
    from UTILS import UTILS
    from QMessageBox import QMessageBox
except:
    pass #Not in Dinamica Code

try:
    from qgis.PyQt.QtWidgets import QMessageBox
except:
    pass #Not in QGIS

class GitHub:

    originName = "mappia"
    releaseName = "Map_Download"
    githubApi = 'https://api.github.com/'

    personal_token = ''

    @staticmethod
    def testLogin(user, token):
        return requests.get(url=GitHub.githubApi + 'user', auth=(user, token)).status_code == 200

    @staticmethod
    def prepareEnvironment(gitExecutable):
        if not gitExecutable:
            return
        gitProgramFolder = os.path.dirname(gitExecutable)
        #feedback.pushConsoleInfo(gitProgramFolder) #cinza escondido
        #feedback.setProgressText(gitExecutable) #preto
        os.environ['GIT_PYTHON_GIT_EXECUTABLE'] = gitExecutable
        #initialPath = os.environ['PATH']
        os.environ['GIT_PYTHON_REFRESH'] = 'quiet'
        import git
        git.refresh(gitExecutable)
        try:
            os.environ['PATH'].split(os.pathsep).index(gitProgramFolder)
        except:
            os.environ["PATH"] = gitProgramFolder + os.pathsep + os.environ["PATH"]

    @staticmethod
    def install_git(mustAskUser):
        def userConfirmed():
            return QMessageBox.Yes == QMessageBox.question(None, "Required GIT executable was not found",
                                                           "Click 'YES' to start download and continue, otherwise please select the executable manually.",
                                                           defaultButton=QMessageBox.Yes,
                                                           buttons=(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel))

        if not ("Windows" in platform.system() or "CYGWIN_NT" in platform.system()):
            QMessageBox.question(None, "Failed to find GIT executable", "Please install git in your system and fill the parameter GIT executable path.")
        if (not mustAskUser or userConfirmed()) == False:
            return ''

        def download_file(url, toDir):
            local_filename = os.path.join(toDir, url.split('/')[-1])
            # NOTE the stream=True parameter below
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
            return local_filename

        tmpDir = tempfile.mkdtemp()
        gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.25.1.windows.1/PortableGit-2.25.1-64-bit.7z.exe"
        # QMessageBox.information(None, "Starting GIT download", "This step will take some time, it depends on your internet speed.\nClick 'OK' to continue.", defaultButton=QMessageBox.Ok, buttons=QMessageBox.Ok)
        selfExtractor = download_file(gitUrl, tmpDir)
        portableGit = os.path.join(tmpDir, "portablegit")
        if (not os.path.isfile(selfExtractor)):
            return ''
        subprocess.check_output([selfExtractor, '-o', portableGit, "-y"])
        return os.path.join(portableGit, 'mingw64', 'bin', 'git.exe')

    @staticmethod
    def getGitExe():
        gitExe = ''
        try:
            gitExe = os.environ['GIT_PYTHON_GIT_EXECUTABLE']
        except:
            pass
        return gitExe

    @staticmethod
    def getRepositorySize(user, repository, password):
        response = GitHub._request('GET', 'https://api.github.com/repos/' + user + "/" + repository, token=password,
                                   headers={'Content-Type': 'application/json'})
        try:
            if response.status_code == 200:
                return json.loads(response.content)['size']
        except:
            print("Failed to get the repository size, ignoring it.")
            return None
        return None

    @staticmethod
    def getGitUrl(githubUser, githubRepository):
        return "https://github.com/" + githubUser + "/" + githubRepository + "/"

    #No password to allow using configured SSHKey.
    @staticmethod
    def getGitPassUrl(user, repository, password):
        if password is None or not password:
            return GitHub.getGitUrl(user, repository)
        return "https://" + user + ":" + password + "@github.com/" + user + "/" + repository + "/"

    @staticmethod
    def lsremote(url):
        import git
        remote_refs = {}
        g = git.cmd.Git()
        for ref in g.ls_remote(url).split('\n'):
            hash_ref_list = ref.split('\t')
            remote_refs[hash_ref_list[1]] = hash_ref_list[0]
        return remote_refs

    @staticmethod
    def existsRepository(user, repository):
        try:
            #feedback.pushConsoleInfo("URL: " + GitHub.getGitUrl(user, repository))
            resp = requests.get(GitHub.getGitUrl(user, repository))
            if resp.status_code == 200:
                return True
            else:
                return False
            #result = GitHub.lsremote(GitHub.getGitUrl(user, repository))
        except:
            return False

    @staticmethod
    def configUser(repo, user):
        repo.git.config("user.email", user)
        repo.git.config("user.name", user)

    @staticmethod
    def getRepository(folder, user, repository, password, feedback):
        from git import Repo
        from git import InvalidGitRepositoryError

        # #Não está funcionando a validação #FIXME Repository creation verification is not working (Modify the create Repo function to verify the creation)
        # #feedback.pushConsoleInfo(user + ' at ' + repository)
        # if not GitHub.existsRepository(user, repository):
        #     feedback.pushConsoleInfo("The repository " + repository + " doesn't exists.\nPlease create a new one at https://github.com/new .")
        #     return None

        #Cria ou pega o repositório atual.
        repo = None
        if not os.path.exists(folder) or (os.path.exists(folder) and not os.listdir(folder)):
            repoSize = GitHub.getRepositorySize(user, repository, password)
            if repoSize is not None:
                repoSize = str(repoSize) + "(kb)"
            else:
                repoSize = ''
            feedback.pushConsoleInfo("Cloning git repository: " + GitHub.getGitUrl(user, repository) + "\nPlease wait, it will download all maps in your repository. " + repoSize)
            repo = GitInteractive.cloneRepo(user, repository, folder, feedback)#Repo.clone_from(GitHub.getGitUrl(user, repository), folder, recursive=True, progress=GitHub.getGitProgressReport(feedback))
            assert (os.path.exists(folder))
            assert(repo)
        else:
            try:
                repo = Repo(folder)
                repoUrl = repo.git.remote("-v")
                expectedUrl = GitHub.getGitUrl(user, repository)
                if repoUrl and not (expectedUrl in re.compile("[\\n\\t ]").split(repoUrl)):
                    feedback.pushConsoleInfo("Your remote URL " + repoUrl + " does not match the expected url " + expectedUrl)
                    return False
            except InvalidGitRepositoryError as e:
                feedback.pushConsoleInfo("The destination folder must be a repository or an empty folder. Reason: " + str(e))
                #repo = Repo.init(folder, bare=False)
        return repo

    @staticmethod
    def isOptionsOk(folder, user, repository, feedback, ghPassword=None, mustAskUser=False):
        try:
            #Cria ou pega o repositório atual.
            repo = GitHub.getRepository(folder, user, repository, ghPassword, feedback)
            if not repo:
                return False
            GitHub.configUser(repo, user)
            if repo.git.status("--porcelain"):
                response = not mustAskUser or QMessageBox.question(None, "Local repository is not clean.",
                                     "The folder have local changes, we need to fix to continue.\nClick 'DISCARD' to discard changes, 'YES' to commit changes, otherwise click 'CANCEL' to cancel and resolve manually.",
                                     buttons=(QMessageBox.Discard | QMessageBox.Yes | QMessageBox.Cancel),
                                     defaultButton=QMessageBox.Discard)
                if not mustAskUser or response == QMessageBox.Yes:
                    feedback.pushConsoleInfo("Pulling remote repository changes to your directory.")
                    GitHub.tryPullRepository(repo, user, repository, feedback)  # Danilo
                    feedback.pushConsoleInfo("Adding all files in folder")
                    GitHub.addFiles(repo, user, repository, feedback)
                    feedback.pushConsoleInfo("Adding all files in folder")
                    GitHub.gitCommit(repo, msg="QGIS - Adding all files in folder " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"), feedback=feedback)
                    feedback.pushConsoleInfo("QGIS - Sending changes to Github")
                    # try:
                    #     UTILS.runLongTask(repo.git.pull, feedback, 'Pease wait, pulling changes.', 30)
                    # except:
                    #     pass
                    GitHub.pushChanges(repo, user, repository, ghPassword, feedback)
                elif response == QMessageBox.Discard:
                    repo.git.clean("-df")
                    repo.git.checkout('--', '.')
                else:
                    feedback.pushConsoleInfo("Error: Local repository is not clean.\nPlease commit the changes made to local repository before run.\nUse: git add * and git commit -m \"MSG\"")
                    return False
            else:
                try:
                    GitHub.tryPullRepository(repo, user, repository, feedback)
                    feedback.pushConsoleInfo("Git: Checking out changes.")
                    repo.git.checkout('--', '.')
                except:
                    pass
            return True
        except Exception as ex:
            feedback.pushConsoleInfo("Canceled due to: {0}".format(ex))
            return False

    @staticmethod
    def findGitExe(gitExe, found_git, mustAskUser):
        if (not gitExe or not os.path.isfile(gitExe)) and (not 'GIT_PYTHON_GIT_EXECUTABLE' in os.environ or not os.path.isfile(os.environ['GIT_PYTHON_GIT_EXECUTABLE'])) and (not found_git or os.path.isfile(found_git)):
            gitExe = GitHub.install_git(mustAskUser)
        return gitExe

    @staticmethod
    def tryPullRepository(repo, ghUser, gitRepository, feedback):
        GitHub.configUser(repo, ghUser)
        try:
            feedback.pushConsoleInfo("Git: Pulling remote repository current state.")
            # UTILS.runLongTask(repo.git.pull, feedback, 'Pease wait, pulling changes.', 30, " -s recursive -X ours " + GitHub.getGitUrl(user, repository) + "master")
            UTILS.runLongTask(repo.git.pull, feedback, 'Pease wait, pulling changes.', 30, "-s", "recursive", "-X", "ours", GitHub.getGitUrl(ghUser, gitRepository), "master")
            feedback.pushConsoleInfo("Before fetch changes.")
            UTILS.runLongTask(repo.git.fetch, feedback, 'Please wait, fetching changes.', 30, GitHub.getGitUrl(ghUser, gitRepository), "master")
            feedback.pushConsoleInfo("Git: Doing checkout.")
            UTILS.runLongTask(repo.git.checkout, feedback, 'Please wait, doing checkout', 30, "--ours")
        except:
            pass

    @staticmethod
    def createRepo(ghRepository, ghUser, ghPassword, outputDir, feedback):
        if len(os.listdir(outputDir)) > 0:
            Feedback.pushConsoleInfo("Cant use selected folder, its not empty, please select an empty folder.")
            return False
        payload = {
            'name': ghRepository,
            'description': 'Repository cointaining maps of the mappia publisher.',
            'branch': 'master',
            'auto_init': 'false'
        }
        feedback.pushConsoleInfo("Creating the new repository: " + ghRepository)
        resp = requests.post(GitHub.githubApi + 'user/repos', auth=(ghUser, ghPassword), data=json.dumps(payload))
        if resp.status_code == 201:
            sleep(2)
            import git
            repo = GitHub.getRepository(outputDir, ghUser, gitRepository, ghPassword, feedback)
            with open(os.path.join(outputDir, 'README'), 'w') as f:
                f.write('empty')
            repo.git.add(['README'])
            repo.git.commit(m='Setting master head.')
            repo.remotes.origin.push()
            return True
        else:
            return False

    @staticmethod
    def runLongTask(function, feedback, waitMessage="Please Wait", secondsReport=60, *args, **kwArgs):
        from concurrent import futures
        # feedback.setProgress(1)
        stepTimer = 0.5
        totalTime = 0
        with futures.ThreadPoolExecutor(max_workers=1) as executor:
            job = executor.submit(function, *args, **kwArgs)
            elapsedTime = 0
            while job.done() == False:
                time.sleep(stepTimer)
                elapsedTime = elapsedTime + stepTimer
                totalTime = totalTime + stepTimer
                if elapsedTime > secondsReport:
                    cancelMsg = "\nCancelling, please wait the current step to finish gracefully." if feedback.isCanceled() else ''
                    feedback.pushConsoleInfo("Elapsed " + str(round(totalTime)) + "s: " + waitMessage + cancelMsg)
                    elapsedTime = 0
                # if canCancelNow and feedback.isCanceled():
                #     feedback.pushConsoleInfo("Job starting to cancel.")
                #     job.cancel()
            feedback.pushConsoleInfo("Elapsed " + str(round(totalTime)) + "s on this step.")
            # UTILS.checkForCanceled(feedback)
            return job.result()


    @staticmethod
    def getGitCredentials(curUser, curPass, mustAskUser):
        state = UTILS.randomString()
        if (not curUser):
            curUser = ''
        if (curPass is None or not curPass or not curUser) or (GitHub.testLogin(curUser, curPass) == False and (mustAskUser or QMessageBox.question(
                None, "Credentials required", "Please inform your credentials, could we open login link for you?") == QMessageBox.Yes)):
            url = 'https://github.com/login/oauth/authorize?redirect_uri=https://csr.ufmg.br/imagery/get_key.php&client_id=10b28a388b0e66e87cee&login=' + curUser + '&scope=read:user%20repo&state=' + state
            credentials = {
                'value': None
            }
            GitHub.getCredentials(state)
            webbrowser.open(url, 1)
            isFirstOpen = True
            def checkLoginValidation(btn, timeSpent):
                credentials['value'] = credentials['value'] or GitHub.getCredentials(state)
                if credentials['value'] and not mustAskUser:
                    btn.done(0)
                return True
            while not credentials['value']:
                sleep(1)
                auxMsg = '' if isFirstOpen else '\n\nWaiting validation, re-openning the authorization github page.\nPlease login on a Github account to continue.'
                isFirstOpen = False
                response = CustomMessageBox.showWithCallback(2000,
                      "Steps to confirm your credentials:\n1) Enter credentials\n2) click to 'authorize Mappia' \n3) Wait and Click 'YES' to confirm.\n Or 'NO' to cancel.\nOpenning the github authentication link in browser." + auxMsg,
                      "Please confirm credentials at Github site to continue", checkLoginValidation, buttons=QMessageBox.Yes | QMessageBox.No)
                credentials['value'] = credentials['value'] or GitHub.getCredentials(state)
                if response == QMessageBox.Yes and not credentials['value']:
                    webbrowser.open(url, 2)
                elif response != QMessageBox.Yes and not credentials['value']:
                    return (None, None)
            return (credentials['value']['user'], credentials['value']['token'])
        return (curUser, curPass)

    @staticmethod
    def addFiles(repo, user, repository, feedback):
        return GitInteractive.addFiles(repo, user, repository, feedback)

    @staticmethod
    def gitCommit(repo, msg, feedback):
        return GitInteractive.gitCommit(repo, msg, feedback)

    @staticmethod
    def pushChanges(repo, user, repository, password, feedback):
        return GitInteractive.pushChanges(repo, user, repository, password, feedback)

    @staticmethod
    def publishTilesToGitHub(outputDir, ghUser, gitRepository, feedback, version, ghPassword=None):
        import git
        feedback.pushConsoleInfo('Github found commiting to your account.')

        repo = GitHub.getRepository(outputDir, ghUser, gitRepository, ghPassword, feedback)

        now = datetime.now()
        # https://stackoverflow.com/questions/6565357/git-push-requires-username-and-password
        repo.git.config("credential.helper", " ", "store")
        GitHub.tryPullRepository(repo, ghUser, gitRepository, feedback) #Danilo
        feedback.pushConsoleInfo('Git: Add all generated tiles to your repository.')
        GitHub.addFiles(repo, ghUser, gitRepository, feedback)
        #feedback.pushConsoleInfo("Git: Mergin.")
        #repo.git.merge("-s recursive", "-X ours")
        #feedback.pushConsoleInfo("Git: Pushing changes.")
        try:
            repo.git.push(GitHub.getGitUrl(ghUser, gitRepository), "master:refs/heads/master")
        except:
            pass
        if repo.index.diff(None) or repo.untracked_files:
            feedback.pushConsoleInfo("No changes, nothing to commit.")
            return None
        feedback.pushConsoleInfo("Git: Committing changes. -------------2")
        try:
            GitHub.gitCommit(repo, "QGIS - " + now.strftime("%d/%m/%Y %H:%M:%S") + " version: " + version, feedback)
        except git.exc.GitCommandError as e:
            print("Warning: reason " + str(e))
        # feedback.pushConsoleInfo("CREATING TAG")
        # tag = now.strftime("%Y%m%d-%H%M%S")
        # new_tag = repo.create_tag(tag, message='Automatic tag "{0}"'.format(tag))
        # repo.remotes[originName].push(new_tag)
        feedback.pushConsoleInfo("Git: Pushing modifications to remote repository.")
        GitHub.pushChanges(repo, ghUser, gitRepository, ghPassword, feedback)
        return None

    @staticmethod
    def getCredentials(secret):
        #Danilo #FIXME colocar UNIQUE no BD
        resp = requests.get('https://csr.ufmg.br/imagery/verify_key.php?state=' + secret)
        if resp.status_code == 200:
            return json.loads(resp.text)
        else:
            return None

    # @staticmethod
    # def getAccessToken(curUser, curPass):
    #     def isNotToken(content):
    #         return not re.match(r'^[a-z0-9]{40}$', content)
    #     # def createTokenFromPass(user, password):
    #     #     params = {
    #     #         "scopes": ["repo", "write:org"],
    #     #         "note": "Mappia Access (" + str(random.uniform(0, 1) * 100000) + ")"
    #     #     }
    #     #     resp = requests.post(url=GitHub.githubApi + 'authorizations', headers={'content-type': 'application/json'}, auth=(user, password), data=json.dumps(params))
    #     #     if resp.status_code == HTTPStatus.CREATED:
    #     #         return json.loads(resp.text)["token"]
    #     #     elif resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
    #     #         #deveria tentar mais uma vez
    #     #         return None
    #     #     elif resp.status_code == HTTPStatus.UNAUTHORIZED:
    #     #         QMessageBox.warning(None, "Mappia Publisher Error", "Failed to login, please check if the entered username/password is valid at (https://github.com/login)")
    #     #         raise Exception("Error: Failed to login, please Verify the entered username/password.")
    #     #     else:
    #     #         QMessageBox.warning(None, "Mappia Publisher Error", "Failed to create a new token. Response code: " + str(resp.status_code) + " Content: " + str(resp.text))
    #     #         raise Exception("Error: Failed to create token. Response code: " + str(resp.status_code) + " Content: " + str(resp.text))
    #     foundToken = None
    #     if not GitHub.testLogin(curUser, curPass):
    #         QMessageBox.warning(None, "Mappia Publisher Error",
    #                             "Failed to login, please check if the entered username/password is valid at (https://github.com/login)")
    #         Exception("Error: Failed to login.")
    #         foundToken = None
    #     elif not isNotToken(curPass) and GitHub.testLogin(curUser, curPass):
    #         foundToken = curPass
    #     elif GitHub.personal_token and not isNotToken(GitHub.personal_token) and GitHub.testLogin(curUser, GitHub.personal_token):
    #         foundToken = GitHub.personal_token
    #     # elif QMessageBox.question(None, "Key required instead of password.", "Want the mappia to automatically create a key for you? Otherwise please access the link: https://github.com/settings/tokens to create the key.", defaultButton=QMessageBox.Yes) == QMessageBox.Yes:
    #     #     retries = 1
    #     #     token = None
    #     #     while token is None and retries <= 5:
    #     #         token = createTokenFromPass(curUser, curPass)
    #     #         retries = retries + 1
    #     #     if token is None:
    #     #         if QMessageBox.question(None, "The token creation have failed. Want to open the creation link?", defaultButton=QMessageBox.Yes) == QMessageBox.Yes:
    #     #             webbrowser.open_new('https://github.com/settings/tokens')
    #     #         raise Exception("Error: Something goes wrong creating the token. Opening the browser, please create your token manually at https://github.com/settings/tokens and enable enable the scope group 'repo'. Please copy the resulting text.")
    #     #     GitHub.personal_token = token
    #     #     QMessageBox.warning(None, "Information", "Created the following token, please copy it to use later '" + token + "'.")
    #     #     foundToken = token
    #     else:
    #         foundToken = None
    #     return foundToken


    @staticmethod
    def _request(*args, **kwargs):
        with_auth = kwargs.pop("with_auth", True)
        token = kwargs.pop("token", '')
        if not token:
            token = os.environ.get("GITHUB_TOKEN", None)
        if token and with_auth:
            kwargs["auth"] = (token, 'x-oauth-basic')
        for _ in range(3):
            response = request(*args, **kwargs)
            is_travis = os.getenv("TRAVIS", None) is not None
            if is_travis and 400 <= response.status_code < 500:
                print("Retrying in 1s (%s Client Error: %s for url: %s)" % (
                    response.status_code, response.reason, response.url))
                time.sleep(1)
                continue
            break
        return response

    @staticmethod
    def _recursive_gh_get(href, items, password=None):
        """Recursively get list of GitHub objects.

        See https://developer.github.com/v3/guides/traversing-with-pagination/
        """
        response = GitHub._request('GET', href, token=password)
        response.raise_for_status()
        items.extend(response.json())
        if "link" not in response.headers:
            return
        # links = link_header.parse(response.headers["link"])
        # rels = {link.rel: link.href for link in links.links}
        # if "next" in rels:
        #     ghRelease._recursive_gh_get(rels["next"], items)

    #Return a list of assets in commit 'releaseName' within this repository.
    @staticmethod
    def getAssets(user, repository, password, tagName):
        release = GitHub.getRelease(user, repository, password, tagName)
        if not release:
            raise Exception('Release with tag_name {0} not found'.format(tagName))
        assets = []
        GitHub._recursive_gh_get(GitHub.githubApi + 'repos/{0}/releases/{1}/assets'.format(
            user + "/" + repository, release["id"]), assets, password)
        return assets

    #If exists get the release with name 'releaseName'.
    @staticmethod
    def getRelease(user, repository, password, tagName):
        def _getRelease(href, password, tagName):
            releaseResp = GitHub._request('GET', href, token=password)
            releaseResp.raise_for_status()
            result = None
            for curResp in releaseResp.json():
                if (curResp and (curResp['tag_name'] == tagName)):
                    result = curResp
                    break
            if result is None and 'link' in releaseResp.headers:
                raise Exception("Please report: not implemented yet." + json.dumps(releaseResp.headers["link"]))
        # if 'link' in releaseResp.headers: #Danilo precisa implementar ainda
        #add resp to curResp.
        #     # links = link_header.parse(response.headers["link"])
        #     # rels = {link.rel: link.href for link in links.links}
        #     # if "next" in rels:
        #     #     ghRelease._recursive_gh_get(rels["next"], items, token)
        #     # Danilo preciso fazer o parse
            return result
        return _getRelease(GitHub.githubApi + 'repos/' + user + "/" + repository + "/releases", password, tagName)

    #Create the download tag or report a error.
    @staticmethod
    def createDownloadTag(user, repository, password, feedback):
        data = {
            'tag_name': GitHub.releaseName,
            'name': GitHub.releaseName,
            'body': GitHub.releaseName,
            'draft': False,
            'prerelease': False
        }
        response = GitHub._request('POST', GitHub.githubApi + 'repos/' + user + "/" + repository + "/releases", token=password, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        if (response.status_code == 422) and GitHub.getRelease(user, repository, password, GitHub.releaseName) is not None: #vou considerar q ja está criado
            pass
        else:
            response.raise_for_status()

    #Try to add the 'uploadFile' as a layer asset.
    @staticmethod
    def addReleaseFile(user, password, repository, maxRetry, forceUpdateFile, uploadFile, layer, feedback):
        if uploadFile is None:
            return None
        releaseRef = GitHub.getRelease(user, repository, password, GitHub.releaseName)

        if releaseRef is None or releaseRef['upload_url'] is None:
            raise Exception("Release '" + GitHub.releaseName + "' was not found")
        assets = GitHub.getAssets(user, repository, password, GitHub.releaseName)
        uploadUrl = releaseRef['upload_url']
        if "{" in uploadUrl:
            uploadUrl = uploadUrl[:uploadUrl.index("{")]
        basename = UTILS.normalizeName(os.path.basename(layer.name())) + str(os.path.splitext(uploadFile)[1])
        #Example: #'https://github.com/asfixia/Mappia_Example_t/releases/download/Map_Download/distance_to_deforested.tif'
        fileDownloadPath = 'https://github.com/' + user + "/" + repository + "/releases/download/" + GitHub.releaseName + "/" + basename

        for asset in assets:
            if asset["name"] == basename:
                # See https://developer.github.com/v3/repos/releases/#response-for-upstream-failure  # noqa: E501
                if asset["state"] == "new" or asset["state"] == "uploaded": #override the old file if last upload failed or update if 'forceUpdateFile' is true.
                    if asset["state"] == "uploaded" and not forceUpdateFile:
                        feedback.setProgressText("File %s already uploaded." % asset['name'])
                        return fileDownloadPath
                    if asset["state"] == "new":
                        feedback.setProgressText("  deleting %s (invalid asset "
                              "with state set to 'new')" % asset['name'])
                    else:
                        feedback.setProgressText("Updating file %s." % asset['name'])
                    url = (
                            GitHub.githubApi
                            + 'repos/{0}/releases/assets/{1}'.format(user + "/" + repository, asset['id'])
                    )
                    response = GitHub._request('DELETE', url, token=password)
                    response.raise_for_status()

        file_size = os.path.getsize(uploadFile)
        feedback.setProgressText("  Uploading %s of size %s (MB)" % (basename, str(file_size / 10e5)))

        url = '{0}?name={1}'.format(uploadUrl, basename)

        # Attempt upload
        with open(uploadFile, 'rb') as f:
            with progress_reporter_cls(
                    label=basename, length=file_size, feedback=feedback) as reporter:
                response = GitHub._request(
                    'POST', url, headers={'Content-Type': 'application/octet-stream'},
                    data=_ProgressFileReader(f, reporter), token=password)
                data = response.json()

        if response.status_code == 502 and maxRetry > 1:
            feedback.setProgressText("Retrying (upload failed with status_code=502)")
            return GitHub.addReleaseFile(user, password, repository, maxRetry - 1, forceUpdateFile, uploadFile, layer, feedback)
        elif response.status_code == 502 and maxRetry <= 1:
            return None
        else:
            response.raise_for_status()
        return fileDownloadPath

####################################### AUX CLASS ##########################

class progress_reporter_cls(object):
    reportProgress = False

    def __init__(self, label='', length=0, feedback=None):
        self.label = label
        self.length = length
        self.total = 0
        self.lastReport = 0
        self.feedback = feedback

    def update(self, chunk_size):
        self.total = self.total + chunk_size
        if self.feedback is not None and self.total > (self.lastReport + (self.length * 0.1)):
            self.feedback.setProgressText('Total: ' + str(self.total / 1000) + " (kb)")
            self.lastReport = self.total
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        pass

#Wrapper used to capture File IO read progress.
class _ProgressFileReader(object):
    def __init__(self, stream, reporter):
        self._stream = stream
        self._reporter = reporter

    def read(self, _size):
        _chunk = self._stream.read(_size)
        self._reporter.update(len(_chunk))
        return _chunk

    def __getattr__(self, attr):
        return getattr(self._stream, attr)

class CustomMessageBox(QMessageBox):
    def __init__(self, *__args):
        QMessageBox.__init__(self)
        self.timeout = 0
        self.callback = None
        self.currentTime = 0

    def showEvent(self, QShowEvent):
        self.currentTime = 0
        if self.autoclose:
            self.startTimer(self.timeout)

    def timerEvent(self, event):
        # try:
        if self.isHidden():
            self.killTimer(event.timerId())
            self.deleteLayer()
        else:
            self.currentTime += 1
            self.callback(self, self.currentTime)
        # except:
        #     self.quit()
        # if self.currentTime >= self.timeout:
        #     self.done(0)

    @staticmethod
    def showWithCallback(timeoutMsCallback, message, title, callback, icon=QMessageBox.Information, buttons=QMessageBox.Ok):
        w = CustomMessageBox()
        w.autoclose = True
        w.callback = callback
        try:
            w.setCallback(callback)
        except:
            pass
        w.timeout = timeoutMsCallback
        w.setText(message)
        w.setWindowTitle(title)
        w.setIcon(icon)
        w.setStandardButtons(buttons)
        return w.exec_()

class GitInteractive() :

    @staticmethod
    def cloneRepo(user, repository, folder, feedback):
        from git import Repo
        return UTILS.runLongTask(Repo.clone_from, feedback, waitMessage="Please wait to complete the download.",
                                   secondsReport=15, url=GitHub.getGitUrl(user, repository), to_path=folder,
                                   recursive=True)

    @staticmethod
    def pushChanges(repo, user, repository, password, feedback):
        return UTILS.runLongTask(repo.git.push, feedback, 'Please wait, uploading changes.', 30,
                                          GitHub.getGitPassUrl(user, repository, password), "master:refs/heads/master")

    @staticmethod
    def gitCommit(repo, msg, feedback):
        return UTILS.runLongTask(repo.git.commit, feedback, 'Please wait, uploading changes.', 30, m=msg)

    @staticmethod
    def addFiles(repo, user, repository, feedback):
        originName = "mappia"
        try:
            repo.git.remote("add", originName, GitHub.getGitUrl(user, repository))
        except:
            repo.git.remote("set-url", originName, GitHub.getGitUrl(user, repository))
        return UTILS.runLongTask(repo.git.add, feedback, waitMessage='Please wait, identifying changes on your repository.', secondsReport=30, all=True) # Adiciona todos arquivos


try:
    from Feedback import Feedback
except:
    pass #Not in Dinamica Code

class Feedback():
    @staticmethod
    def pushConsoleInfo(message):
        print(message)

    @staticmethod
    def setProgress(percentage):
        print("Progress: " + str(percentage))

    @staticmethod
    def setProgressText(message):
        print(message)

    @staticmethod
    def isCanceled():
        return False





try:
    from gdal2tiles_local import generateTileForMap
except:
    pass #Not in Dinamica Code

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ******************************************************************************
#  $Id$
#
# Project:  Google Summer of Code 2007, 2008 (http://code.google.com/soc/)
# Support:  BRGM (http://www.brgm.fr)
# Purpose:  Convert a raster into TMS (Tile Map Service) tiles in a directory.
#           - generate Google Earth metadata (KML SuperOverlay)
#           - generate simple HTML viewer based on Google Maps and OpenLayers
#           - support of global tiles (Spherical Mercator) for compatibility
#               with interactive web maps a la Google Maps
# Author:   Klokan Petr Pridal, klokan at klokan dot cz
# Web:      http://www.klokan.cz/projects/gdal2tiles/
# GUI:      http://www.maptiler.org/
#
###############################################################################
# Copyright (c) 2008, Klokan Petr Pridal
# Copyright (c) 2010-2013, Even Rouault <even dot rouault at mines-paris dot org>
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
# ******************************************************************************



import math
from multiprocessing import Pipe, Pool, Process, Manager
import os
import tempfile
import shutil
import sys
import time
from uuid import uuid4
from xml.etree import ElementTree

from osgeo import gdal
from osgeo import osr

try:
    from colorize_rgb import applyLegend
except:
    pass #Not in Dinamica Code

try:
    from PIL import Image
    import numpy
    import osgeo.gdal_array as gdalarray
except Exception:
    # 'antialias' resampling is not available
    pass

__version__ = "$Id$"

resampling_list = ('average', 'near', 'bilinear', 'cubic', 'cubicspline', 'lanczos',  'antialias')
profile_list = ('mercator', 'geodetic', 'raster')
webviewer_list = ('all', 'google', 'openlayers', 'leaflet', 'none')

# =============================================================================
# =============================================================================
# =============================================================================

__doc__globalmaptiles = """
globalmaptiles.py

Global Map Tiles as defined in Tile Map Service (TMS) Profiles
==============================================================

Functions necessary for generation of global tiles used on the web.
It contains classes implementing coordinate conversions for:

  - GlobalMercator (based on EPSG:3857)
       for Google Maps, Yahoo Maps, Bing Maps compatible tiles
  - GlobalGeodetic (based on EPSG:4326)
       for OpenLayers Base Map and Google Earth compatible tiles

More info at:

http://wiki.osgeo.org/wiki/Tile_Map_Service_Specification
http://wiki.osgeo.org/wiki/WMS_Tiling_Client_Recommendation
http://msdn.microsoft.com/en-us/library/bb259689.aspx
http://code.google.com/apis/maps/documentation/overlays.html#Google_Maps_Coordinates

Created by Klokan Petr Pridal on 2008-07-03.
Google Summer of Code 2008, project GDAL2Tiles for OSGEO.

In case you use this class in your product, translate it to another language
or find it useful for your project please let me know.
My email: klokan at klokan dot cz.
I would like to know where it was used.

Class is available under the open-source GDAL license (www.gdal.org).
"""

MAXZOOMLEVEL = 32


class GlobalMercator(object):
    r"""
    TMS Global Mercator Profile
    ---------------------------

    Functions necessary for generation of tiles in Spherical Mercator projection,
    EPSG:3857.

    Such tiles are compatible with Google Maps, Bing Maps, Yahoo Maps,
    UK Ordnance Survey OpenSpace API, ...
    and you can overlay them on top of base maps of those web mapping applications.

    Pixel and tile coordinates are in TMS notation (origin [0,0] in bottom-left).

    What coordinate conversions do we need for TMS Global Mercator tiles::

         LatLon      <->       Meters      <->     Pixels    <->       Tile

     WGS84 coordinates   Spherical Mercator  Pixels in pyramid  Tiles in pyramid
         lat/lon            XY in meters     XY pixels Z zoom      XYZ from TMS
        EPSG:4326           EPSG:387
         .----.              ---------               --                TMS
        /      \     <->     |       |     <->     /----/    <->      Google
        \      /             |       |           /--------/          QuadTree
         -----               ---------         /------------/
       KML, public         WebMapService         Web Clients      TileMapService

    What is the coordinate extent of Earth in EPSG:3857?

      [-20037508.342789244, -20037508.342789244, 20037508.342789244, 20037508.342789244]
      Constant 20037508.342789244 comes from the circumference of the Earth in meters,
      which is 40 thousand kilometers, the coordinate origin is in the middle of extent.
      In fact you can calculate the constant as: 2 * math.pi * 6378137 / 2.0
      $ echo 180 85 | gdaltransform -s_srs EPSG:4326 -t_srs EPSG:3857
      Polar areas with abs(latitude) bigger then 85.05112878 are clipped off.

    What are zoom level constants (pixels/meter) for pyramid with EPSG:3857?

      whole region is on top of pyramid (zoom=0) covered by 256x256 pixels tile,
      every lower zoom level resolution is always divided by two
      initialResolution = 20037508.342789244 * 2 / 256 = 156543.03392804062

    What is the difference between TMS and Google Maps/QuadTree tile name convention?

      The tile raster itself is the same (equal extent, projection, pixel size),
      there is just different identification of the same raster tile.
      Tiles in TMS are counted from [0,0] in the bottom-left corner, id is XYZ.
      Google placed the origin [0,0] to the top-left corner, reference is XYZ.
      Microsoft is referencing tiles by a QuadTree name, defined on the website:
      http://msdn2.microsoft.com/en-us/library/bb259689.aspx

    The lat/lon coordinates are using WGS84 datum, yes?

      Yes, all lat/lon we are mentioning should use WGS84 Geodetic Datum.
      Well, the web clients like Google Maps are projecting those coordinates by
      Spherical Mercator, so in fact lat/lon coordinates on sphere are treated as if
      the were on the WGS84 ellipsoid.

      From MSDN documentation:
      To simplify the calculations, we use the spherical form of projection, not
      the ellipsoidal form. Since the projection is used only for map display,
      and not for displaying numeric coordinates, we don't need the extra precision
      of an ellipsoidal projection. The spherical projection causes approximately
      0.33 percent scale distortion in the Y direction, which is not visually
      noticeable.

    How do I create a raster in EPSG:3857 and convert coordinates with PROJ.4?

      You can use standard GIS tools like gdalwarp, cs2cs or gdaltransform.
      All of the tools supports -t_srs 'epsg:3857'.

      For other GIS programs check the exact definition of the projection:
      More info at http://spatialreference.org/ref/user/google-projection/
      The same projection is designated as EPSG:3857. WKT definition is in the
      official EPSG database.

      Proj4 Text:
        +proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0
        +k=1.0 +units=m +nadgrids=@null +no_defs

      Human readable WKT format of EPSG:3857:
         PROJCS["Google Maps Global Mercator",
             GEOGCS["WGS 84",
                 DATUM["WGS_1984",
                     SPHEROID["WGS 84",6378137,298.257223563,
                         AUTHORITY["EPSG","7030"]],
                     AUTHORITY["EPSG","6326"]],
                 PRIMEM["Greenwich",0],
                 UNIT["degree",0.0174532925199433],
                 AUTHORITY["EPSG","4326"]],
             PROJECTION["Mercator_1SP"],
             PARAMETER["central_meridian",0],
             PARAMETER["scale_factor",1],
             PARAMETER["false_easting",0],
             PARAMETER["false_northing",0],
             UNIT["metre",1,
                 AUTHORITY["EPSG","9001"]]]
    """

    def __init__(self, tileSize=256):
        "Initialize the TMS Global Mercator pyramid"
        self.tileSize = tileSize
        self.initialResolution = 2 * math.pi * 6378137 / self.tileSize
        # 156543.03392804062 for tileSize 256 pixels
        self.originShift = 2 * math.pi * 6378137 / 2.0
        # 20037508.342789244

    def LatLonToMeters(self, lat, lon):
        "Converts given lat/lon in WGS84 Datum to XY in Spherical Mercator EPSG:3857"

        mx = lon * self.originShift / 180.0
        my = math.log(math.tan((90 + lat) * math.pi / 360.0)) / (math.pi / 180.0)

        my = my * self.originShift / 180.0
        return mx, my

    def MetersToLatLon(self, mx, my):
        "Converts XY point from Spherical Mercator EPSG:3857 to lat/lon in WGS84 Datum"

        lon = (mx / self.originShift) * 180.0
        lat = (my / self.originShift) * 180.0

        lat = 180 / math.pi * (2 * math.atan(math.exp(lat * math.pi / 180.0)) - math.pi / 2.0)
        return lat, lon

    def PixelsToMeters(self, px, py, zoom):
        "Converts pixel coordinates in given zoom level of pyramid to EPSG:3857"

        res = self.Resolution(zoom)
        mx = px * res - self.originShift
        my = py * res - self.originShift
        return mx, my

    def MetersToPixels(self, mx, my, zoom):
        "Converts EPSG:3857 to pyramid pixel coordinates in given zoom level"

        res = self.Resolution(zoom)
        px = (mx + self.originShift) / res
        py = (my + self.originShift) / res
        return px, py

    def PixelsToTile(self, px, py):
        "Returns a tile covering region in given pixel coordinates"

        tx = int(math.ceil(px / float(self.tileSize)) - 1)
        ty = int(math.ceil(py / float(self.tileSize)) - 1)
        return tx, ty

    def PixelsToRaster(self, px, py, zoom):
        "Move the origin of pixel coordinates to top-left corner"

        mapSize = self.tileSize << zoom
        return px, mapSize - py

    def MetersToTile(self, mx, my, zoom):
        "Returns tile for given mercator coordinates"

        px, py = self.MetersToPixels(mx, my, zoom)
        return self.PixelsToTile(px, py)

    def TileBounds(self, tx, ty, zoom):
        "Returns bounds of the given tile in EPSG:3857 coordinates"

        minx, miny = self.PixelsToMeters(tx*self.tileSize, ty*self.tileSize, zoom)
        maxx, maxy = self.PixelsToMeters((tx+1)*self.tileSize, (ty+1)*self.tileSize, zoom)
        return (minx, miny, maxx, maxy)

    def TileLatLonBounds(self, tx, ty, zoom):
        "Returns bounds of the given tile in latitude/longitude using WGS84 datum"

        bounds = self.TileBounds(tx, ty, zoom)
        minLat, minLon = self.MetersToLatLon(bounds[0], bounds[1])
        maxLat, maxLon = self.MetersToLatLon(bounds[2], bounds[3])

        return (minLat, minLon, maxLat, maxLon)

    def Resolution(self, zoom):
        "Resolution (meters/pixel) for given zoom level (measured at Equator)"

        # return (2 * math.pi * 6378137) / (self.tileSize * 2**zoom)
        return self.initialResolution / (2**zoom)

    def ZoomForPixelSize(self, pixelSize):
        "Maximal scaledown zoom of the pyramid closest to the pixelSize."

        for i in range(MAXZOOMLEVEL):
            if pixelSize > self.Resolution(i):
                if i != -1:
                    return i-1
                else:
                    return 0    # We don't want to scale up

    def GoogleTile(self, tx, ty, zoom):
        "Converts TMS tile coordinates to Google Tile coordinates"

        # coordinate origin is moved from bottom-left to top-left corner of the extent
        return tx, (2**zoom - 1) - ty

    def QuadTree(self, tx, ty, zoom):
        "Converts TMS tile coordinates to Microsoft QuadTree"

        quadKey = ""
        ty = (2**zoom - 1) - ty
        for i in range(zoom, 0, -1):
            digit = 0
            mask = 1 << (i-1)
            if (tx & mask) != 0:
                digit += 1
            if (ty & mask) != 0:
                digit += 2
            quadKey += str(digit)

        return quadKey


class GlobalGeodetic(object):
    r"""
    TMS Global Geodetic Profile
    ---------------------------

    Functions necessary for generation of global tiles in Plate Carre projection,
    EPSG:4326, "unprojected profile".

    Such tiles are compatible with Google Earth (as any other EPSG:4326 rasters)
    and you can overlay the tiles on top of OpenLayers base map.

    Pixel and tile coordinates are in TMS notation (origin [0,0] in bottom-left).

    What coordinate conversions do we need for TMS Global Geodetic tiles?

      Global Geodetic tiles are using geodetic coordinates (latitude,longitude)
      directly as planar coordinates XY (it is also called Unprojected or Plate
      Carre). We need only scaling to pixel pyramid and cutting to tiles.
      Pyramid has on top level two tiles, so it is not square but rectangle.
      Area [-180,-90,180,90] is scaled to 512x256 pixels.
      TMS has coordinate origin (for pixels and tiles) in bottom-left corner.
      Rasters are in EPSG:4326 and therefore are compatible with Google Earth.

         LatLon      <->      Pixels      <->     Tiles

     WGS84 coordinates   Pixels in pyramid  Tiles in pyramid
         lat/lon         XY pixels Z zoom      XYZ from TMS
        EPSG:4326
         .----.                ----
        /      \     <->    /--------/    <->      TMS
        \      /         /--------------/
         -----        /--------------------/
       WMS, KML    Web Clients, Google Earth  TileMapService
    """

    def __init__(self, tmscompatible, tileSize=256):
        self.tileSize = tileSize
        if tmscompatible is not None:
            # Defaults the resolution factor to 0.703125 (2 tiles @ level 0)
            # Adhers to OSGeo TMS spec
            # http://wiki.osgeo.org/wiki/Tile_Map_Service_Specification#global-geodetic
            self.resFact = 180.0 / self.tileSize
        else:
            # Defaults the resolution factor to 1.40625 (1 tile @ level 0)
            # Adheres OpenLayers, MapProxy, etc default resolution for WMTS
            self.resFact = 360.0 / self.tileSize

    def LonLatToPixels(self, lon, lat, zoom):
        "Converts lon/lat to pixel coordinates in given zoom of the EPSG:4326 pyramid"

        res = self.resFact / 2**zoom
        px = (180 + lon) / res
        py = (90 + lat) / res
        return px, py

    def PixelsToTile(self, px, py):
        "Returns coordinates of the tile covering region in pixel coordinates"

        tx = int(math.ceil(px / float(self.tileSize)) - 1)
        ty = int(math.ceil(py / float(self.tileSize)) - 1)
        return tx, ty

    def LonLatToTile(self, lon, lat, zoom):
        "Returns the tile for zoom which covers given lon/lat coordinates"

        px, py = self.LonLatToPixels(lon, lat, zoom)
        return self.PixelsToTile(px, py)

    def Resolution(self, zoom):
        "Resolution (arc/pixel) for given zoom level (measured at Equator)"

        return self.resFact / 2**zoom

    def ZoomForPixelSize(self, pixelSize):
        "Maximal scaledown zoom of the pyramid closest to the pixelSize."

        for i in range(MAXZOOMLEVEL):
            if pixelSize > self.Resolution(i):
                if i != 0:
                    return i-1
                else:
                    return 0    # We don't want to scale up

    def TileBounds(self, tx, ty, zoom):
        "Returns bounds of the given tile"
        res = self.resFact / 2**zoom
        return (
            tx*self.tileSize*res - 180,
            ty*self.tileSize*res - 90,
            (tx+1)*self.tileSize*res - 180,
            (ty+1)*self.tileSize*res - 90
        )

    def TileLatLonBounds(self, tx, ty, zoom):
        "Returns bounds of the given tile in the SWNE form"
        b = self.TileBounds(tx, ty, zoom)
        return (b[1], b[0], b[3], b[2])


class Zoomify(object):
    """
    Tiles compatible with the Zoomify viewer
    ----------------------------------------
    """

    def __init__(self, width, height, tilesize=256, tileformat='jpg'):
        """Initialization of the Zoomify tile tree"""

        self.tilesize = tilesize
        self.tileformat = tileformat
        imagesize = (width, height)
        tiles = (math.ceil(width / tilesize), math.ceil(height / tilesize))

        # Size (in tiles) for each tier of pyramid.
        self.tierSizeInTiles = []
        self.tierSizeInTiles.append(tiles)

        # Image size in pixels for each pyramid tierself
        self.tierImageSize = []
        self.tierImageSize.append(imagesize)

        while (imagesize[0] > tilesize or imagesize[1] > tilesize):
            imagesize = (math.floor(imagesize[0] / 2), math.floor(imagesize[1] / 2))
            tiles = (math.ceil(imagesize[0] / tilesize), math.ceil(imagesize[1] / tilesize))
            self.tierSizeInTiles.append(tiles)
            self.tierImageSize.append(imagesize)

        self.tierSizeInTiles.reverse()
        self.tierImageSize.reverse()

        # Depth of the Zoomify pyramid, number of tiers (zoom levels)
        self.numberOfTiers = len(self.tierSizeInTiles)

        # Number of tiles up to the given tier of pyramid.
        self.tileCountUpToTier = []
        self.tileCountUpToTier[0] = 0
        for i in range(1, self.numberOfTiers+1):
            self.tileCountUpToTier.append(
                self.tierSizeInTiles[i-1][0] * self.tierSizeInTiles[i-1][1] +
                self.tileCountUpToTier[i-1]
            )

    def tilefilename(self, x, y, z):
        """Returns filename for tile with given coordinates"""

        tileIndex = x + y * self.tierSizeInTiles[z][0] + self.tileCountUpToTier[z]
        return os.path.join("TileGroup%.0f" % math.floor(tileIndex / 256),
                            "%s-%s-%s.%s" % (z, x, y, self.tileformat))


class GDALError(Exception):
    pass


def exit_with_error(message, details=""):
    # Message printing and exit code kept from the way it worked using the OptionParser (in case
    # someone parses the error output)
    sys.stderr.write("Usage: gdal2tiles_local.py [options] input_file [output]\n\n")
    sys.stderr.write("gdal2tiles_local.py: error: %s\n" % message)
    if details:
        sys.stderr.write("\n\n%s\n" % details)

    sys.exit(2)


def generate_kml(tx, ty, tz, tileext, tilesize, tileswne, options, children=None, **args):
    """
    Template for the KML. Returns filled string.
    """
    if not children:
        children = []

    args['tx'], args['ty'], args['tz'] = tx, ty, tz
    args['tileformat'] = tileext
    if 'tilesize' not in args:
        args['tilesize'] = tilesize

    if 'minlodpixels' not in args:
        args['minlodpixels'] = int(args['tilesize'] / 2)
    if 'maxlodpixels' not in args:
        args['maxlodpixels'] = int(args['tilesize'] * 8)
    if children == []:
        args['maxlodpixels'] = -1

    if tx is None:
        tilekml = False
        args['title'] = options.title
    else:
        tilekml = True
        args['title'] = "%d/%d/%d.kml" % (tz, tx, ty)
        args['south'], args['west'], args['north'], args['east'] = tileswne(tx, ty, tz)

    if tx == 0:
        args['drawOrder'] = 2 * tz + 1
    elif tx is not None:
        args['drawOrder'] = 2 * tz
    else:
        args['drawOrder'] = 0

    url = options.url
    if not url:
        if tilekml:
            url = "../../"
        else:
            url = ""

    s = """<?xml version="1.0" encoding="utf-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>%(title)s</name>
    <description></description>
    <Style>
      <ListStyle id="hideChildren">
        <listItemType>checkHideChildren</listItemType>
      </ListStyle>
    </Style>""" % args
    if tilekml:
        s += """
    <Region>
      <LatLonAltBox>
        <north>%(north).14f</north>
        <south>%(south).14f</south>
        <east>%(east).14f</east>
        <west>%(west).14f</west>
      </LatLonAltBox>
      <Lod>
        <minLodPixels>%(minlodpixels)d</minLodPixels>
        <maxLodPixels>%(maxlodpixels)d</maxLodPixels>
      </Lod>
    </Region>
    <GroundOverlay>
      <drawOrder>%(drawOrder)d</drawOrder>
      <Icon>
        <href>%(ty)d.%(tileformat)s</href>
      </Icon>
      <LatLonBox>
        <north>%(north).14f</north>
        <south>%(south).14f</south>
        <east>%(east).14f</east>
        <west>%(west).14f</west>
      </LatLonBox>
    </GroundOverlay>
""" % args

    for cx, cy, cz in children:
        csouth, cwest, cnorth, ceast = tileswne(cx, cy, cz)
        s += """
    <NetworkLink>
      <name>%d/%d/%d.%s</name>
      <Region>
        <LatLonAltBox>
          <north>%.14f</north>
          <south>%.14f</south>
          <east>%.14f</east>
          <west>%.14f</west>
        </LatLonAltBox>
        <Lod>
          <minLodPixels>%d</minLodPixels>
          <maxLodPixels>-1</maxLodPixels>
        </Lod>
      </Region>
      <Link>
        <href>%s%d/%d/%d.kml</href>
        <viewRefreshMode>onRegion</viewRefreshMode>
        <viewFormat/>
      </Link>
    </NetworkLink>
        """ % (cz, cx, cy, args['tileformat'], cnorth, csouth, ceast, cwest,
               args['minlodpixels'], url, cz, cx, cy)

    s += """      </Document>
</kml>
    """
    return s


def scale_query_to_tile(dsquery, dstile, tiledriver, options, tilefilename=''):
    """Scales down query dataset to the tile dataset"""

    querysize = dsquery.RasterXSize
    tilesize = dstile.RasterXSize
    tilebands = dstile.RasterCount

    if options.resampling == 'average':

        # Function: gdal.RegenerateOverview()
        for i in range(1, tilebands+1):
            # Black border around NODATA
            res = gdal.RegenerateOverview(dsquery.GetRasterBand(i), dstile.GetRasterBand(i),
                                          'average')
            if res != 0:
                exit_with_error("RegenerateOverview() failed on %s, error %d" % (
                    tilefilename, res))

    elif options.resampling == 'antialias':

        # Scaling by PIL (Python Imaging Library) - improved Lanczos
        array = numpy.zeros((querysize, querysize, tilebands), numpy.uint8)
        for i in range(tilebands):
            array[:, :, i] = gdalarray.BandReadAsArray(dsquery.GetRasterBand(i+1),
                                                       0, 0, querysize, querysize)
        im = Image.fromarray(array, 'RGBA')     # Always four bands
        im1 = im.resize((tilesize, tilesize), Image.ANTIALIAS)
        if os.path.exists(tilefilename):
            im0 = Image.open(tilefilename)
            im1 = Image.composite(im1, im0, im1)
        im1.save(tilefilename, tiledriver)

    else:

        if options.resampling == 'near':
            gdal_resampling = gdal.GRA_NearestNeighbour

        elif options.resampling == 'bilinear':
            gdal_resampling = gdal.GRA_Bilinear

        elif options.resampling == 'cubic':
            gdal_resampling = gdal.GRA_Cubic

        elif options.resampling == 'cubicspline':
            gdal_resampling = gdal.GRA_CubicSpline

        elif options.resampling == 'lanczos':
            gdal_resampling = gdal.GRA_Lanczos

        # Other algorithms are implemented by gdal.ReprojectImage().
        dsquery.SetGeoTransform((0.0, tilesize / float(querysize), 0.0, 0.0, 0.0,
                                 tilesize / float(querysize)))
        dstile.SetGeoTransform((0.0, 1.0, 0.0, 0.0, 0.0, 1.0))

        res = gdal.ReprojectImage(dsquery, dstile, None, None, gdal_resampling)
        if res != 0:
            exit_with_error("ReprojectImage() failed on %s, error %d" % (tilefilename, res))


def setup_no_data_values(input_dataset, options):
    """
    Extract the NODATA values from the dataset or use the passed arguments as override if any
    """
    in_nodata = []
    if options.srcnodata:
        nds = list(map(float, options.srcnodata.split(',')))
        if len(nds) < input_dataset.RasterCount:
            in_nodata = (nds * input_dataset.RasterCount)[:input_dataset.RasterCount]
        else:
            in_nodata = nds
    else:
        for i in range(1, input_dataset.RasterCount+1):
            raster_no_data = input_dataset.GetRasterBand(i).GetNoDataValue()
            if raster_no_data is not None:
                in_nodata.append(raster_no_data)

    if options.verbose:
        print("NODATA: %s" % in_nodata)

    return in_nodata


def setup_input_srs(input_dataset, options):
    """
    Determines and returns the Input Spatial Reference System (SRS) as an osr object and as a
    WKT representation

    Uses in priority the one passed in the command line arguments. If None, tries to extract them
    from the input dataset
    """

    input_srs = None
    input_srs_wkt = None

    if options.s_srs:
        input_srs = osr.SpatialReference()
        input_srs.SetFromUserInput(options.s_srs)
        input_srs_wkt = input_srs.ExportToWkt()
    else:
        input_srs_wkt = input_dataset.GetProjection()
        if not input_srs_wkt and input_dataset.GetGCPCount() != 0:
            input_srs_wkt = input_dataset.GetGCPProjection()
        if input_srs_wkt:
            input_srs = osr.SpatialReference()
            input_srs.ImportFromWkt(input_srs_wkt)

    return input_srs, input_srs_wkt


def setup_output_srs(input_srs, options):
    """
    Setup the desired SRS (based on options)
    """
    output_srs = osr.SpatialReference()

    if options.profile == 'mercator':
        output_srs.ImportFromEPSG(3857)
    elif options.profile == 'geodetic':
        output_srs.ImportFromEPSG(4326)
    else:
        output_srs = input_srs

    return output_srs


def has_georeference(dataset):
    return (dataset.GetGeoTransform() != (0.0, 1.0, 0.0, 0.0, 0.0, 1.0) or
            dataset.GetGCPCount() != 0)


def reproject_dataset(from_dataset, from_srs, to_srs, options=None):
    """
    Returns the input dataset in the expected "destination" SRS.
    If the dataset is already in the correct SRS, returns it unmodified
    """
    if not from_srs or not to_srs:
        raise GDALError("from and to SRS must be defined to reproject the dataset")

    if (from_srs.ExportToProj4() != to_srs.ExportToProj4()) or (from_dataset.GetGCPCount() != 0):
        to_dataset = gdal.AutoCreateWarpedVRT(from_dataset,
                                              from_srs.ExportToWkt(), to_srs.ExportToWkt())

        if options and options.verbose:
            print("Warping of the raster by AutoCreateWarpedVRT (result saved into 'tiles.vrt')")
            to_dataset.GetDriver().CreateCopy("tiles.vrt", to_dataset)

        return to_dataset
    else:
        return from_dataset


def add_gdal_warp_options_to_string(vrt_string, warp_options):
    if not warp_options:
        return vrt_string

    vrt_root = ElementTree.fromstring(vrt_string)
    options = vrt_root.find("GDALWarpOptions")

    if options is None:
        return vrt_string

    for key, value in warp_options.items():
        tb = ElementTree.TreeBuilder()
        tb.start("Option", {"name": key})
        tb.data(value)
        tb.end("Option")
        elem = tb.close()
        options.insert(0, elem)

    return ElementTree.tostring(vrt_root).decode()


def update_no_data_values(warped_vrt_dataset, nodata_values, options=None):
    """
    Takes an array of NODATA values and forces them on the WarpedVRT file dataset passed
    """
    # TODO: gbataille - Seems that I forgot tests there
    if nodata_values != []:
        temp_file = gettempfilename('-gdal2tiles.vrt')
        warped_vrt_dataset.GetDriver().CreateCopy(temp_file, warped_vrt_dataset)
        with open(temp_file, 'r') as f:
            vrt_string = f.read()

        vrt_string = add_gdal_warp_options_to_string(
            vrt_string, {"INIT_DEST": "NO_DATA", "UNIFIED_SRC_NODATA": "YES"})

# TODO: gbataille - check the need for this replacement. Seems to work without
#         # replace BandMapping tag for NODATA bands....
#         for i in range(len(nodata_values)):
#             s = s.replace(
#                 '<BandMapping src="%i" dst="%i"/>' % ((i+1), (i+1)),
#                 """
# <BandMapping src="%i" dst="%i">
# <SrcNoDataReal>%i</SrcNoDataReal>
# <SrcNoDataImag>0</SrcNoDataImag>
# <DstNoDataReal>%i</DstNoDataReal>
# <DstNoDataImag>0</DstNoDataImag>
# </BandMapping>
#                 """ % ((i+1), (i+1), nodata_values[i], nodata_values[i]))

        # save the corrected VRT
        with open(temp_file, 'w') as f:
            f.write(vrt_string)

        corrected_dataset = gdal.Open(temp_file)
        os.unlink(temp_file)

        # set NODATA_VALUE metadata
        corrected_dataset.SetMetadataItem(
            'NODATA_VALUES', ' '.join([str(i) for i in nodata_values]))

        if options and options.verbose:
            print("Modified warping result saved into 'tiles1.vrt'")
            # TODO: gbataille - test replacing that with a gdal write of the dataset (more
            # accurately what's used, even if should be the same
            with open("tiles1.vrt", "w") as f:
                f.write(vrt_string)

        return corrected_dataset


def add_alpha_band_to_string_vrt(vrt_string):
    # TODO: gbataille - Old code speak of this being equivalent to gdalwarp -dstalpha
    # To be checked

    vrt_root = ElementTree.fromstring(vrt_string)

    index = 0
    nb_bands = 0
    for subelem in list(vrt_root):
        if subelem.tag == "VRTRasterBand":
            nb_bands += 1
            color_node = subelem.find("./ColorInterp")
            if color_node is not None and color_node.text == "Alpha":
                raise Exception("Alpha band already present")
        else:
            if nb_bands:
                # This means that we are one element after the Band definitions
                break

        index += 1

    tb = ElementTree.TreeBuilder()
    tb.start("VRTRasterBand",
             {'dataType': "Byte", "band": str(nb_bands + 1), "subClass": "VRTWarpedRasterBand"})
    tb.start("ColorInterp", {})
    tb.data("Alpha")
    tb.end("ColorInterp")
    tb.end("VRTRasterBand")
    elem = tb.close()

    vrt_root.insert(index, elem)

    warp_options = vrt_root.find(".//GDALWarpOptions")
    tb = ElementTree.TreeBuilder()
    tb.start("DstAlphaBand", {})
    tb.data(str(nb_bands + 1))
    tb.end("DstAlphaBand")
    elem = tb.close()
    warp_options.append(elem)

    # TODO: gbataille - this is a GDALWarpOptions. Why put it in a specific place?
    tb = ElementTree.TreeBuilder()
    tb.start("Option", {"name": "INIT_DEST"})
    tb.data("0")
    tb.end("Option")
    elem = tb.close()
    warp_options.append(elem)

    return ElementTree.tostring(vrt_root).decode()


def update_alpha_value_for_non_alpha_inputs(warped_vrt_dataset, options=None):
    """
    Handles dataset with 1 or 3 bands, i.e. without alpha channel, in the case the nodata value has
    not been forced by options
    """
    if warped_vrt_dataset.RasterCount in [1, 3]:
        tempfilename = gettempfilename('-gdal2tiles.vrt')
        warped_vrt_dataset.GetDriver().CreateCopy(tempfilename, warped_vrt_dataset)
        with open(tempfilename) as f:
            orig_data = f.read()
        alpha_data = add_alpha_band_to_string_vrt(orig_data)
        with open(tempfilename, 'w') as f:
            f.write(alpha_data)

        warped_vrt_dataset = gdal.Open(tempfilename)
        os.unlink(tempfilename)

        if options and options.verbose:
            print("Modified -dstalpha warping result saved into 'tiles1.vrt'")
            # TODO: gbataille - test replacing that with a gdal write of the dataset (more
            # accurately what's used, even if should be the same
            with open("tiles1.vrt", "w") as f:
                f.write(alpha_data)

    return warped_vrt_dataset


def nb_data_bands(dataset):
    """
    Return the number of data (non-alpha) bands of a gdal dataset
    """
    alphaband = dataset.GetRasterBand(1).GetMaskBand()
    if ((alphaband.GetMaskFlags() & gdal.GMF_ALPHA) or
            dataset.RasterCount == 4 or
            dataset.RasterCount == 2):
        return dataset.RasterCount - 1
    else:
        return dataset.RasterCount


def gettempfilename(suffix):
    """Returns a temporary filename"""
    if '_' in os.environ:
        # tempfile.mktemp() crashes on some Wine versions (the one of Ubuntu 12.04 particularly)
        if os.environ['_'].find('wine') >= 0:
            tmpdir = '.'
            if 'TMP' in os.environ:
                tmpdir = os.environ['TMP']
            import time
            import random
            random.seed(time.time())
            random_part = 'file%d' % random.randint(0, 1000000000)
            return os.path.join(tmpdir, random_part + suffix)

    return tempfile.mktemp(suffix)


def create_base_tile(tile_job_info, tile_detail, options, queue=None):
    gdal.AllRegister()

    dataBandsCount = tile_job_info.nb_data_bands
    output = tile_job_info.output_file_path
    tileext = tile_job_info.tile_extension
    tilesize = tile_job_info.tile_size
    options = tile_job_info.options

    tilebands = dataBandsCount + 1
    ds = gdal.Open(tile_job_info.src_file, gdal.GA_ReadOnly)
    mem_drv = gdal.GetDriverByName('MEM')
    out_drv = gdal.GetDriverByName(tile_job_info.tile_driver)
    alphaband = ds.GetRasterBand(1).GetMaskBand()

    tx = tile_detail.tx
    ty = tile_detail.ty
    tz = tile_detail.tz
    rx = tile_detail.rx
    ry = tile_detail.ry
    rxsize = tile_detail.rxsize
    rysize = tile_detail.rysize
    wx = tile_detail.wx
    wy = tile_detail.wy
    wxsize = tile_detail.wxsize
    wysize = tile_detail.wysize
    querysize = tile_detail.querysize

    # Tile dataset in memory
    tilefilename = os.path.join(
        output, str(tz), '{0:04d}'.format(tx) + "_" + '{0:04d}'.format(ty) + "." + tileext)
    dstile = mem_drv.Create('', tilesize, tilesize, tilebands)

    data = alpha = None

    if options.verbose:
        print("\tReadRaster Extent: ",
              (rx, ry, rxsize, rysize), (wx, wy, wxsize, wysize))

    # Query is in 'nearest neighbour' but can be bigger in then the tilesize
    # We scale down the query to the tilesize by supplied algorithm.

    if rxsize != 0 and rysize != 0 and wxsize != 0 and wysize != 0:
        data = ds.ReadRaster(rx, ry, rxsize, rysize, wxsize, wysize,
                             band_list=list(range(1, dataBandsCount+1)))
        alpha = alphaband.ReadRaster(rx, ry, rxsize, rysize, wxsize, wysize)

    # The tile in memory is a transparent file by default. Write pixel values into it if
    # any
    if data:
        if tilesize == querysize:
            # Use the ReadRaster result directly in tiles ('nearest neighbour' query)
            dstile.WriteRaster(wx, wy, wxsize, wysize, data,
                               band_list=list(range(1, dataBandsCount+1)))
            dstile.WriteRaster(wx, wy, wxsize, wysize, alpha, band_list=[tilebands])

            # Note: For source drivers based on WaveLet compression (JPEG2000, ECW,
            # MrSID) the ReadRaster function returns high-quality raster (not ugly
            # nearest neighbour)
            # TODO: Use directly 'near' for WaveLet files
        else:
            # Big ReadRaster query in memory scaled to the tilesize - all but 'near'
            # algo
            dsquery = mem_drv.Create('', querysize, querysize, tilebands)
            # TODO: fill the null value in case a tile without alpha is produced (now
            # only png tiles are supported)
            dsquery.WriteRaster(wx, wy, wxsize, wysize, data,
                                band_list=list(range(1, dataBandsCount+1)))
            dsquery.WriteRaster(wx, wy, wxsize, wysize, alpha, band_list=[tilebands])

            scale_query_to_tile(dsquery, dstile, tile_job_info.tile_driver, options,
                                tilefilename=tilefilename)
            del dsquery

    # Force freeing the memory to make sure the C++ destructor is called and the memory as well as
    # the file locks are released
    del ds
    del data

    if options.resampling != 'antialias':
        # Write a copy of tile to png/jpg
        out_drv.CreateCopy(tilefilename, dstile, strict=0)

    del dstile

    options.generatedFiles.append(tilefilename)
    # applyLegend(tilefilename, options.legendObj)

    # # Create a KML file for this tile.
    # if tile_job_info.kml:
    #     kmlfilename = os.path.join(output, str(tz), str(tx), '%d.kml' % ty)
    #     if not options.resume or not os.path.exists(kmlfilename):
    #         with open(kmlfilename, 'wb') as f:
    #             f.write(generate_kml(
    #                 tx, ty, tz, tile_job_info.tile_extension, tile_job_info.tile_size,
    #                 tile_job_info.tile_swne, tile_job_info.options
    #             ).encode('utf-8'))

    if queue:
        queue.put("tile %s %s %s" % (tx, ty, tz))


def create_overview_tiles(tile_job_info, output_folder, options):
    """Generation of the overview tiles (higher in the pyramid) based on existing tiles"""
    mem_driver = gdal.GetDriverByName('MEM')
    tile_driver = tile_job_info.tile_driver
    out_driver = gdal.GetDriverByName(tile_driver)

    tilebands = tile_job_info.nb_data_bands + 1

    # Usage of existing tiles: from 4 underlying tiles generate one as overview.

    tcount = 0
    for tz in range(tile_job_info.tmaxz - 1, tile_job_info.tminz - 1, -1):
        tminx, tminy, tmaxx, tmaxy = tile_job_info.tminmax[tz]
        tcount += (1 + abs(tmaxx-tminx)) * (1 + abs(tmaxy-tminy))

    ti = 0

    if tcount == 0:
        return

    if not options.quiet:
        print("Generating Overview Tiles:")

    progress_bar = ProgressBar(tcount)
    progress_bar.start()

    for tz in range(tile_job_info.tmaxz - 1, tile_job_info.tminz - 1, -1):
        tminx, tminy, tmaxx, tmaxy = tile_job_info.tminmax[tz]
        for ty in range(tmaxy, tminy - 1, -1):
            for tx in range(tminx, tmaxx + 1):

                ti += 1
                ytile = GDAL2Tiles.getYtile(ty, tz, options)
                tilefilename = os.path.join(output_folder,
                                            str(tz),
                                            #str(tx),
                                            #"%s.%s" % (ytile, tile_job_info.tile_extension))
                                            '{0:04d}'.format(tx) + "_" + '{0:04d}'.format(ytile) + "." + tile_job_info.tile_extension)

                if options.verbose:
                    print(ti, '/', tcount, tilefilename)

                if options.resume and os.path.exists(tilefilename):
                    if options.verbose:
                        print("Tile generation skipped because of --resume")
                    else:
                        progress_bar.log_progress()
                    continue

                # Create directories for the tile
                if not os.path.exists(os.path.dirname(tilefilename)):
                    os.makedirs(os.path.dirname(tilefilename))

                dsquery = mem_driver.Create('', 2 * tile_job_info.tile_size,
                                            2 * tile_job_info.tile_size, tilebands)
                # TODO: fill the null value
                dstile = mem_driver.Create('', tile_job_info.tile_size, tile_job_info.tile_size,
                                           tilebands)

                # TODO: Implement more clever walking on the tiles with cache functionality
                # probably walk should start with reading of four tiles from top left corner
                # Hilbert curve

                children = []
                # Read the tiles and write them to query window
                for y in range(2 * ty, 2 * ty + 2):
                    for x in range(2 * tx, 2 * tx + 2):
                        minx, miny, maxx, maxy = tile_job_info.tminmax[tz + 1]
                        if x >= minx and x <= maxx and y >= miny and y <= maxy:
                            ytile2 = GDAL2Tiles.getYtile(y, tz+1, options)
                            dsquerytile = gdal.Open(
                                os.path.join(output_folder, str(tz + 1),
                                             '{0:04d}'.format(x) + "_" + '{0:04d}'.format(ytile2) + "." + tile_job_info.tile_extension),
                                             #str(x), "%s.%s" % (ytile2, tile_job_info.tile_extension)),
                                gdal.GA_ReadOnly)
                            if (ty == 0 and y == 1) or (ty != 0 and (y % (2 * ty)) != 0):
                                tileposy = 0
                            else:
                                tileposy = tile_job_info.tile_size
                            if tx:
                                tileposx = x % (2 * tx) * tile_job_info.tile_size
                            elif tx == 0 and x == 1:
                                tileposx = tile_job_info.tile_size
                            else:
                                tileposx = 0
                            dsquery.WriteRaster(
                                tileposx, tileposy, tile_job_info.tile_size,
                                tile_job_info.tile_size,
                                dsquerytile.ReadRaster(0, 0,
                                                       tile_job_info.tile_size,
                                                       tile_job_info.tile_size),
                                band_list=list(range(1, tilebands + 1)))
                            children.append([x, y, tz + 1])

                scale_query_to_tile(dsquery, dstile, tile_driver, options,
                                    tilefilename=tilefilename)
                # Write a copy of tile to png/jpg
                if options.resampling != 'antialias':
                    # Write a copy of tile to png/jpg
                    out_driver.CreateCopy(tilefilename, dstile, strict=0)

                del dstile

                options.generatedFiles.append(tilefilename)
                # applyLegend(tilefilename, options.legendObj)

                if options.verbose:
                    print("\tbuild from zoom", tz + 1,
                          " tiles:", (2 * tx, 2 * ty), (2 * tx + 1, 2 * ty),
                          (2 * tx, 2 * ty + 1), (2 * tx + 1, 2 * ty + 1))

                # # Create a KML file for this tile.
                # if tile_job_info.kml:
                #     with open(os.path.join(
                #         output_folder,
                #         '%d/%d/%d.kml' % (tz, tx, ty)
                #     ), 'wb') as f:
                #         f.write(generate_kml(
                #             tx, ty, tz, tile_job_info.tile_extension, tile_job_info.tile_size,
                #             get_tile_swne(tile_job_info, options), options, children
                #         ).encode('utf-8'))

                if not options.verbose and not options.quiet:
                    progress_bar.log_progress()


def optparse_init():
    """Prepare the option parser for input (argv)"""

    from optparse import OptionParser, OptionGroup
    usage = "Usage: %prog [options] input_file [output]"
    p = OptionParser(usage, version="%prog " + __version__)
    p.add_option("-p", "--profile", dest='profile',
                 type='choice', choices=profile_list,
                 help=("Tile cutting profile (%s) - default 'mercator' "
                       "(Google Maps compatible)" % ",".join(profile_list)))
    p.add_option("-r", "--resampling", dest="resampling",
                 type='choice', choices=resampling_list,
                 help="Resampling method (%s) - default 'average'" % ",".join(resampling_list))
    p.add_option("-s", "--s_srs", dest="s_srs", metavar="SRS",
                 help="The spatial reference system used for the source input data")
    p.add_option("-z", "--zoom", dest="zoom",
                 help="Zoom levels to render (format:'2-5' or '10').")
    p.add_option("-e", "--resume", dest="resume", action="store_true",
                 help="Resume mode. Generate only missing files.")
    p.add_option("-a", "--srcnodata", dest="srcnodata", metavar="NODATA",
                 help="NODATA transparency value to assign to the input data")
    p.add_option("-d", "--tmscompatible", dest="tmscompatible", action="store_true",
                 help=("When using the geodetic profile, specifies the base resolution "
                       "as 0.703125 or 2 tiles at zoom level 0."))
    p.add_option("-x", "--xyz", 
                 action='store_true', dest='xyz',
                 help="Use XYZ tile numbering instead of TMS")
    p.add_option("-v", "--verbose",
                 action="store_true", dest="verbose",
                 help="Print status messages to stdout")
    p.add_option("-q", "--quiet",
                 action="store_true", dest="quiet",
                 help="Disable messages and status to stdout")
    p.add_option("--processes",
                 dest="nb_processes",
                 type='int',
                 help="Number of processes to use for tiling")

    # KML options
    g = OptionGroup(p, "KML (Google Earth) options",
                    "Options for generated Google Earth SuperOverlay metadata")
    g.add_option("-k", "--force-kml", dest='kml', action="store_true",
                 help=("Generate KML for Google Earth - default for 'geodetic' profile and "
                       "'raster' in EPSG:4326. For a dataset with different projection use "
                       "with caution!"))
    g.add_option("-n", "--no-kml", dest='kml', action="store_false",
                 help="Avoid automatic generation of KML files for EPSG:4326")
    g.add_option("-u", "--url", dest='url',
                 help="URL address where the generated tiles are going to be published")
    p.add_option_group(g)

    # HTML options
    g = OptionGroup(p, "Web viewer options",
                    "Options for generated HTML viewers a la Google Maps")
    g.add_option("-w", "--webviewer", dest='webviewer', type='choice', choices=webviewer_list,
                 help="Web viewer to generate (%s) - default 'all'" % ",".join(webviewer_list))
    g.add_option("-t", "--title", dest='title',
                 help="Title of the map")
    g.add_option("-c", "--copyright", dest='copyright',
                 help="Copyright for the map")
    g.add_option("-g", "--googlekey", dest='googlekey',
                 help="Google Maps API key from http://code.google.com/apis/maps/signup.html")
    g.add_option("-b", "--bingkey", dest='bingkey',
                 help="Bing Maps API key from https://www.bingmapsportal.com/")
    p.add_option_group(g)

    p.set_defaults(verbose=False, profile="mercator", kml=False, url='', zoom='0-2', xyz=True,
                   webviewer='none', copyright='', resampling='near', resume=False,
                   googlekey='INSERT_YOUR_KEY_HERE', bingkey='INSERT_YOUR_KEY_HERE',
                   processes=1)

    return p


def process_args(argv):
    parser = optparse_init()
    options, args = parser.parse_args(args=argv)

    # Args should be either an input file OR an input file and an output folder
    if (len(args) == 0):
        exit_with_error("You need to specify at least an input file as argument to the script")
    if (len(args) > 2):
        exit_with_error("Processing of several input files is not supported.",
                        "Please first use a tool like gdal_vrtmerge.py or gdal_merge.py on the "
                        "files: gdal_vrtmerge.py -o merged.vrt %s" % " ".join(args))

    input_file = args[0]
    if not os.path.isfile(input_file):
        exit_with_error("The provided input file %s does not exist or is not a file" % input_file)

    if len(args) == 2:
        output_folder = args[1]
    else:
        output_folder = os.path.basename(input_file)

    options = options_post_processing(options, input_file, output_folder)

    return input_file, output_folder, options


def options_post_processing(options, input_file, output_folder):
    if not options.title:
        options.title = os.path.basename(input_file)

    if options.url and not options.url.endswith('/'):
        options.url += '/'
    if options.url:
        out_path = output_folder
        if out_path.endswith("/"):
            out_path = out_path[:-1]
        options.url += os.path.basename(out_path) + '/'

    # Supported options
    if options.resampling == 'average':
        try:
            if gdal.RegenerateOverview:
                pass
        except Exception:
            exit_with_error("'average' resampling algorithm is not available.",
                            "Please use -r 'near' argument or upgrade to newer version of GDAL.")

    elif options.resampling == 'antialias':
        try:
            if numpy:     # pylint:disable=W0125
                pass
        except Exception:
            exit_with_error("'antialias' resampling algorithm is not available.",
                            "Install PIL (Python Imaging Library) and numpy.")

    try:
        os.path.basename(input_file).encode('ascii')
    except UnicodeEncodeError:
        full_ascii = False
    else:
        full_ascii = True

    # LC_CTYPE check
    if not full_ascii and 'UTF-8' not in os.environ.get("LC_CTYPE", ""):
        if not options.quiet:
            print("\nWARNING: "
                  "You are running gdal2tiles_local.py with a LC_CTYPE environment variable that is "
                  "not UTF-8 compatible, and your input file contains non-ascii characters. "
                  "The generated sample googlemaps, openlayers or "
                  "leaflet files might contain some invalid characters as a result\n")

    # Output the results
    if options.verbose:
        print("Options:", options)
        print("Input:", input_file)
        print("Output:", output_folder)
        print("Cache: %s MB" % (gdal.GetCacheMax() / 1024 / 1024))
        print('')

    return options


class TileDetail(object):
    tx = 0
    ty = 0
    tz = 0
    rx = 0
    ry = 0
    rxsize = 0
    rysize = 0
    wx = 0
    wy = 0
    wxsize = 0
    wysize = 0
    querysize = 0

    def __init__(self, **kwargs):
        for key in kwargs:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

    def __unicode__(self):
        return "TileDetail %s\n%s\n%s\n" % (self.tx, self.ty, self.tz)

    def __str__(self):
        return "TileDetail %s\n%s\n%s\n" % (self.tx, self.ty, self.tz)

    def __repr__(self):
        return "TileDetail %s\n%s\n%s\n" % (self.tx, self.ty, self.tz)


class TileJobInfo(object):
    """
    Plain object to hold tile job configuration for a dataset
    """
    src_file = ""
    nb_data_bands = 0
    output_file_path = ""
    tile_extension = ""
    tile_size = 0
    tile_driver = None
    kml = False
    tminmax = []
    tminz = 0
    tmaxz = 0
    in_srs_wkt = 0
    out_geo_trans = []
    ominy = 0
    is_epsg_4326 = False
    options = None

    def __init__(self, **kwargs):
        for key in kwargs:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

    def __unicode__(self):
        return "TileJobInfo %s\n" % (self.src_file)

    def __str__(self):
        return "TileJobInfo %s\n" % (self.src_file)

    def __repr__(self):
        return "TileJobInfo %s\n" % (self.src_file)


class Gdal2TilesError(Exception):
    pass


class GDAL2Tiles(object):

    def __init__(self, input_file, output_folder, options):
        """Constructor function - initialization"""
        self.out_drv = None
        self.mem_drv = None
        self.warped_input_dataset = None
        self.out_srs = None
        self.nativezoom = None
        self.tminmax = None
        self.tsize = None
        self.mercator = None
        self.geodetic = None
        self.alphaband = None
        self.dataBandsCount = None
        self.out_gt = None
        self.tileswne = None
        self.swne = None
        self.ominx = None
        self.omaxx = None
        self.omaxy = None
        self.ominy = None

        self.input_file = None
        self.output_folder = None

        # Tile format
        self.tilesize = 256
        self.tiledriver = 'PNG'
        self.tileext = 'png'
        self.tmp_dir = tempfile.mkdtemp()
        self.tmp_vrt_filename = os.path.join(self.tmp_dir, str(uuid4()) + '.vrt')

        # Should we read bigger window of the input raster and scale it down?
        # Note: Modified later by open_input()
        # Not for 'near' resampling
        # Not for Wavelet based drivers (JPEG2000, ECW, MrSID)
        # Not for 'raster' profile
        self.scaledquery = True
        # How big should be query window be for scaling down
        # Later on reset according the chosen resampling algorightm
        self.querysize = 4 * self.tilesize

        # Should we use Read on the input file for generating overview tiles?
        # Note: Modified later by open_input()
        # Otherwise the overview tiles are generated from existing underlying tiles
        self.overviewquery = False

        self.input_file = input_file
        self.output_folder = output_folder
        self.options = options

        if self.options.resampling == 'near':
            self.querysize = self.tilesize

        elif self.options.resampling == 'bilinear':
            self.querysize = self.tilesize * 2

        # User specified zoom levels
        self.tminz = None
        self.tmaxz = None
        if self.options.zoom:
            minmax = self.options.zoom.split('-', 1)
            minmax.extend([''])
            zoom_min, zoom_max = minmax[:2]
            self.tminz = int(zoom_min)
            if zoom_max:
                self.tmaxz = int(zoom_max)
            else:
                self.tmaxz = int(zoom_min)

        # KML generation
        self.kml = self.options.kml

    # -------------------------------------------------------------------------
    def open_input(self):
        """Initialization of the input raster, reprojection if necessary"""
        gdal.AllRegister()

        self.out_drv = gdal.GetDriverByName(self.tiledriver)
        self.mem_drv = gdal.GetDriverByName('MEM')

        if not self.out_drv:
            raise Exception("The '%s' driver was not found, is it available in this GDAL build?",
                            self.tiledriver)
        if not self.mem_drv:
            raise Exception("The 'MEM' driver was not found, is it available in this GDAL build?")

        # Open the input file

        if self.input_file:
            input_dataset = gdal.Open(self.input_file, gdal.GA_ReadOnly)
        else:
            raise Exception("No input file was specified")

        if self.options.verbose:
            print("Input file:",
                  "( %sP x %sL - %s bands)" % (input_dataset.RasterXSize,
                                               input_dataset.RasterYSize,
                                               input_dataset.RasterCount))

        if not input_dataset:
            # Note: GDAL prints the ERROR message too
            exit_with_error("It is not possible to open the input file '%s'." % self.input_file)

        # Read metadata from the input file
        if input_dataset.RasterCount == 0:
            exit_with_error("Input file '%s' has no raster band" % self.input_file)

        if input_dataset.GetRasterBand(1).GetRasterColorTable():
            exit_with_error(
                "Please convert this file to RGB/RGBA and run gdal2tiles on the result.",
                "From paletted file you can create RGBA file (temp.vrt) by:\n"
                "gdal_translate -of vrt -expand rgba %s temp.vrt\n"
                "then run:\n"
                "gdal2tiles temp.vrt" % self.input_file
            )

        in_nodata = setup_no_data_values(input_dataset, self.options)

        if self.options.verbose:
            print("Preprocessed file:",
                  "( %sP x %sL - %s bands)" % (input_dataset.RasterXSize,
                                               input_dataset.RasterYSize,
                                               input_dataset.RasterCount))

        in_srs, self.in_srs_wkt = setup_input_srs(input_dataset, self.options)

        self.out_srs = setup_output_srs(in_srs, self.options)

        # If input and output reference systems are different, we reproject the input dataset into
        # the output reference system for easier manipulation

        self.warped_input_dataset = None

        if self.options.profile in ('mercator', 'geodetic'):

            if not in_srs:
                exit_with_error(
                    "Input file has unknown SRS.",
                    "Use --s_srs ESPG:xyz (or similar) to provide source reference system.")

            if not has_georeference(input_dataset):
                exit_with_error(
                    "There is no georeference - neither affine transformation (worldfile) "
                    "nor GCPs. You can generate only 'raster' profile tiles.",
                    "Either gdal2tiles with parameter -p 'raster' or use another GIS "
                    "software for georeference e.g. gdal_transform -gcp / -a_ullr / -a_srs"
                )

            if ((in_srs.ExportToProj4() != self.out_srs.ExportToProj4()) or
                    (input_dataset.GetGCPCount() != 0)):
                self.warped_input_dataset = reproject_dataset(
                    input_dataset, in_srs, self.out_srs)

                if in_nodata:
                    self.warped_input_dataset = update_no_data_values(
                        self.warped_input_dataset, in_nodata, options=self.options)
                else:
                    self.warped_input_dataset = update_alpha_value_for_non_alpha_inputs(
                        self.warped_input_dataset, options=self.options)

            if self.warped_input_dataset and self.options.verbose:
                print("Projected file:", "tiles.vrt", "( %sP x %sL - %s bands)" % (
                    self.warped_input_dataset.RasterXSize,
                    self.warped_input_dataset.RasterYSize,
                    self.warped_input_dataset.RasterCount))

        if not self.warped_input_dataset:
            self.warped_input_dataset = input_dataset

        #Salva o arquivo reprojetado
        self.warped_input_dataset.GetDriver().CreateCopy(self.tmp_vrt_filename,
                                                         self.warped_input_dataset)

        # Get alpha band (either directly or from NODATA value)
        self.alphaband = self.warped_input_dataset.GetRasterBand(1).GetMaskBand()
        self.dataBandsCount = nb_data_bands(self.warped_input_dataset)

        # KML test
        self.isepsg4326 = False
        srs4326 = osr.SpatialReference()
        srs4326.ImportFromEPSG(4326)
        if self.out_srs and srs4326.ExportToProj4() == self.out_srs.ExportToProj4():
            self.kml = True
            self.isepsg4326 = True
            if self.options.verbose:
                print("KML autotest OK!")

        # Read the georeference
        self.out_gt = self.warped_input_dataset.GetGeoTransform()

        # Test the size of the pixel

        # Report error in case rotation/skew is in geotransform (possible only in 'raster' profile)
        if (self.out_gt[2], self.out_gt[4]) != (0, 0):
            exit_with_error("Georeference of the raster contains rotation or skew. "
                            "Such raster is not supported. Please use gdalwarp first.")

        # Here we expect: pixel is square, no rotation on the raster

        # Output Bounds - coordinates in the output SRS
        self.ominx = self.out_gt[0]
        self.omaxx = self.out_gt[0] + self.warped_input_dataset.RasterXSize * self.out_gt[1]
        self.omaxy = self.out_gt[3]
        self.ominy = self.out_gt[3] - self.warped_input_dataset.RasterYSize * self.out_gt[1]
        # Note: maybe round(x, 14) to avoid the gdal_translate behaviour, when 0 becomes -1e-15

        if self.options.verbose:
            print("Bounds (output srs):", round(self.ominx, 13), self.ominy, self.omaxx, self.omaxy)

        # Calculating ranges for tiles in different zoom levels
        if self.options.profile == 'mercator':

            self.mercator = GlobalMercator()

            # Function which generates SWNE in LatLong for given tile
            self.tileswne = self.mercator.TileLatLonBounds

            # Generate table with min max tile coordinates for all zoomlevels
            self.tminmax = list(range(0, 32))
            for tz in range(0, 32):
                tminx, tminy = self.mercator.MetersToTile(self.ominx, self.ominy, tz)
                tmaxx, tmaxy = self.mercator.MetersToTile(self.omaxx, self.omaxy, tz)
                # crop tiles extending world limits (+-180,+-90)
                tminx, tminy = max(0, tminx), max(0, tminy)
                tmaxx, tmaxy = min(2**tz-1, tmaxx), min(2**tz-1, tmaxy)
                self.tminmax[tz] = (tminx, tminy, tmaxx, tmaxy)

            # TODO: Maps crossing 180E (Alaska?)

            # Get the minimal zoom level (map covers area equivalent to one tile)
            if self.tminz is None:
                self.tminz = self.mercator.ZoomForPixelSize(
                    self.out_gt[1] *
                    max(self.warped_input_dataset.RasterXSize,
                        self.warped_input_dataset.RasterYSize) /
                    float(self.tilesize))

            # Get the maximal zoom level
            # (closest possible zoom level up on the resolution of raster)
            if self.tmaxz is None:
                self.tmaxz = self.mercator.ZoomForPixelSize(self.out_gt[1])

            if self.options.verbose:
                print("Bounds (latlong):",
                      self.mercator.MetersToLatLon(self.ominx, self.ominy),
                      self.mercator.MetersToLatLon(self.omaxx, self.omaxy))
                print('MinZoomLevel:', self.tminz)
                print("MaxZoomLevel:",
                      self.tmaxz,
                      "(",
                      self.mercator.Resolution(self.tmaxz),
                      ")")

        if self.options.profile == 'geodetic':

            self.geodetic = GlobalGeodetic(self.options.tmscompatible)

            # Function which generates SWNE in LatLong for given tile
            self.tileswne = self.geodetic.TileLatLonBounds

            # Generate table with min max tile coordinates for all zoomlevels
            self.tminmax = list(range(0, 32))
            for tz in range(0, 32):
                tminx, tminy = self.geodetic.LonLatToTile(self.ominx, self.ominy, tz)
                tmaxx, tmaxy = self.geodetic.LonLatToTile(self.omaxx, self.omaxy, tz)
                # crop tiles extending world limits (+-180,+-90)
                tminx, tminy = max(0, tminx), max(0, tminy)
                tmaxx, tmaxy = min(2**(tz+1)-1, tmaxx), min(2**tz-1, tmaxy)
                self.tminmax[tz] = (tminx, tminy, tmaxx, tmaxy)

            # TODO: Maps crossing 180E (Alaska?)

            # Get the maximal zoom level
            # (closest possible zoom level up on the resolution of raster)
            if self.tminz is None:
                self.tminz = self.geodetic.ZoomForPixelSize(
                    self.out_gt[1] *
                    max(self.warped_input_dataset.RasterXSize,
                        self.warped_input_dataset.RasterYSize) /
                    float(self.tilesize))

            # Get the maximal zoom level
            # (closest possible zoom level up on the resolution of raster)
            if self.tmaxz is None:
                self.tmaxz = self.geodetic.ZoomForPixelSize(self.out_gt[1])

            if self.options.verbose:
                print("Bounds (latlong):", self.ominx, self.ominy, self.omaxx, self.omaxy)

        if self.options.profile == 'raster':

            def log2(x):
                return math.log10(x) / math.log10(2)

            self.nativezoom = int(
                max(math.ceil(log2(self.warped_input_dataset.RasterXSize/float(self.tilesize))),
                    math.ceil(log2(self.warped_input_dataset.RasterYSize/float(self.tilesize)))))

            if self.options.verbose:
                print("Native zoom of the raster:", self.nativezoom)

            # Get the minimal zoom level (whole raster in one tile)
            if self.tminz is None:
                self.tminz = 0

            # Get the maximal zoom level (native resolution of the raster)
            if self.tmaxz is None:
                self.tmaxz = self.nativezoom

            # Generate table with min max tile coordinates for all zoomlevels
            self.tminmax = list(range(0, self.tmaxz+1))
            self.tsize = list(range(0, self.tmaxz+1))
            for tz in range(0, self.tmaxz+1):
                tsize = 2.0**(self.nativezoom-tz)*self.tilesize
                tminx, tminy = 0, 0
                tmaxx = int(math.ceil(self.warped_input_dataset.RasterXSize / tsize)) - 1
                tmaxy = int(math.ceil(self.warped_input_dataset.RasterYSize / tsize)) - 1
                self.tsize[tz] = math.ceil(tsize)
                self.tminmax[tz] = (tminx, tminy, tmaxx, tmaxy)

            # Function which generates SWNE in LatLong for given tile
            if self.kml and self.in_srs_wkt:
                ct = osr.CoordinateTransformation(in_srs, srs4326)

                def rastertileswne(x, y, z):
                    pixelsizex = (2**(self.tmaxz-z) * self.out_gt[1])       # X-pixel size in level
                    west = self.out_gt[0] + x*self.tilesize*pixelsizex
                    east = west + self.tilesize*pixelsizex
                    south = self.ominy + y*self.tilesize*pixelsizex
                    north = south + self.tilesize*pixelsizex
                    if not self.isepsg4326:
                        # Transformation to EPSG:4326 (WGS84 datum)
                        west, south = ct.TransformPoint(west, south)[:2]
                        east, north = ct.TransformPoint(east, north)[:2]
                    return south, west, north, east

                self.tileswne = rastertileswne
            else:
                self.tileswne = lambda x, y, z: (0, 0, 0, 0)   # noqa

    def generate_metadata(self):
        """
        Generation of main metadata files and HTML viewers (metadata related to particular
        tiles are generated during the tile processing).
        """

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        if self.options.profile == 'mercator':

            south, west = self.mercator.MetersToLatLon(self.ominx, self.ominy)
            north, east = self.mercator.MetersToLatLon(self.omaxx, self.omaxy)
            south, west = max(-85.05112878, south), max(-180.0, west)
            north, east = min(85.05112878, north), min(180.0, east)
            self.swne = (south, west, north, east)

            # Generate googlemaps.html
            if self.options.webviewer in ('all', 'google') and self.options.profile == 'mercator':
                if (not self.options.resume or not
                        os.path.exists(os.path.join(self.output_folder, 'googlemaps.html'))):
                    with open(os.path.join(self.output_folder, 'googlemaps.html'), 'wb') as f:
                        f.write(self.generate_googlemaps().encode('utf-8'))

            # Generate openlayers.html
            if self.options.webviewer in ('all', 'openlayers'):
                if (not self.options.resume or not
                        os.path.exists(os.path.join(self.output_folder, 'openlayers.html'))):
                    with open(os.path.join(self.output_folder, 'openlayers.html'), 'wb') as f:
                        f.write(self.generate_openlayers().encode('utf-8'))

            # Generate leaflet.html
            if self.options.webviewer in ('all', 'leaflet'):
                if (not self.options.resume or not
                        os.path.exists(os.path.join(self.output_folder, 'leaflet.html'))):
                    with open(os.path.join(self.output_folder, 'leaflet.html'), 'wb') as f:
                        f.write(self.generate_leaflet().encode('utf-8'))

        elif self.options.profile == 'geodetic':

            west, south = self.ominx, self.ominy
            east, north = self.omaxx, self.omaxy
            south, west = max(-90.0, south), max(-180.0, west)
            north, east = min(90.0, north), min(180.0, east)
            self.swne = (south, west, north, east)

            # Generate openlayers.html
            if self.options.webviewer in ('all', 'openlayers'):
                if (not self.options.resume or not
                        os.path.exists(os.path.join(self.output_folder, 'openlayers.html'))):
                    with open(os.path.join(self.output_folder, 'openlayers.html'), 'wb') as f:
                        f.write(self.generate_openlayers().encode('utf-8'))

        elif self.options.profile == 'raster':

            west, south = self.ominx, self.ominy
            east, north = self.omaxx, self.omaxy

            self.swne = (south, west, north, east)

            # Generate openlayers.html
            if self.options.webviewer in ('all', 'openlayers'):
                if (not self.options.resume or not
                        os.path.exists(os.path.join(self.output_folder, 'openlayers.html'))):
                    with open(os.path.join(self.output_folder, 'openlayers.html'), 'wb') as f:
                        f.write(self.generate_openlayers().encode('utf-8'))

        # Generate tilemapresource.xml.
        if not self.options.resume or not os.path.exists(os.path.join(self.output_folder, 'tilemapresource.xml')):
            with open(os.path.join(self.output_folder, 'tilemapresource.xml'), 'wb') as f:
                f.write(self.generate_tilemapresource().encode('utf-8'))

        if self.kml:
            # TODO: Maybe problem for not automatically generated tminz
            # The root KML should contain links to all tiles in the tminz level
            children = []
            xmin, ymin, xmax, ymax = self.tminmax[self.tminz]
            for x in range(xmin, xmax+1):
                for y in range(ymin, ymax+1):
                    children.append([x, y, self.tminz])
            # Generate Root KML
            if self.kml:
                if (not self.options.resume or not
                        os.path.exists(os.path.join(self.output_folder, 'doc.kml'))):
                    with open(os.path.join(self.output_folder, 'doc.kml'), 'wb') as f:
                        f.write(generate_kml(
                            None, None, None, self.tileext, self.tilesize, self.tileswne,
                            self.options, children
                        ).encode('utf-8'))

    def generate_base_tiles(self):
        """
        Generation of the base tiles (the lowest in the pyramid) directly from the input raster
        """

        if not self.options.quiet:
            print("Generating Base Tiles:")

        if self.options.verbose:
            print('')
            print("Tiles generated from the max zoom level:")
            print("----------------------------------------")
            print('')

        # Set the bounds
        tminx, tminy, tmaxx, tmaxy = self.tminmax[self.tmaxz]

        ds = self.warped_input_dataset
        tilebands = self.dataBandsCount + 1
        querysize = self.querysize

        if self.options.verbose:
            print("dataBandsCount: ", self.dataBandsCount)
            print("tilebands: ", tilebands)

        tcount = (1+abs(tmaxx-tminx)) * (1+abs(tmaxy-tminy))
        ti = 0

        tile_details = []

        tz = self.tmaxz
        for ty in range(tmaxy, tminy-1, -1):
            for tx in range(tminx, tmaxx+1):

                ti += 1
                ytile = GDAL2Tiles.getYtile(ty, tz, self.options)
                tilefilename = os.path.join(
                    self.output_folder, str(tz), '{0:04d}'.format(tx) + "_" + '{0:04d}'.format(ytile) + "." + self.tileext)
                if self.options.verbose:
                    print(ti, '/', tcount, tilefilename)

                if self.options.resume and os.path.exists(tilefilename):
                    if self.options.verbose:
                        print("Tile generation skipped because of --resume")
                    continue

                # Create directories for the tile
                if not os.path.exists(os.path.dirname(tilefilename)):
                    os.makedirs(os.path.dirname(tilefilename))

                if self.options.profile == 'mercator':
                    # Tile bounds in EPSG:3857
                    b = self.mercator.TileBounds(tx, ty, tz)
                elif self.options.profile == 'geodetic':
                    b = self.geodetic.TileBounds(tx, ty, tz)

                # Don't scale up by nearest neighbour, better change the querysize
                # to the native resolution (and return smaller query tile) for scaling

                if self.options.profile in ('mercator', 'geodetic'):
                    rb, wb = self.geo_query(ds, b[0], b[3], b[2], b[1])

                    # Pixel size in the raster covering query geo extent
                    nativesize = wb[0] + wb[2]
                    if self.options.verbose:
                        print("\tNative Extent (querysize", nativesize, "): ", rb, wb)

                    # Tile bounds in raster coordinates for ReadRaster query
                    rb, wb = self.geo_query(ds, b[0], b[3], b[2], b[1], querysize=querysize)

                    rx, ry, rxsize, rysize = rb
                    wx, wy, wxsize, wysize = wb

                else:     # 'raster' profile:

                    tsize = int(self.tsize[tz])   # tilesize in raster coordinates for actual zoom
                    xsize = self.warped_input_dataset.RasterXSize     # size of the raster in pixels
                    ysize = self.warped_input_dataset.RasterYSize
                    if tz >= self.nativezoom:
                        querysize = self.tilesize

                    rx = (tx) * tsize
                    rxsize = 0
                    if tx == tmaxx:
                        rxsize = xsize % tsize
                    if rxsize == 0:
                        rxsize = tsize

                    rysize = 0
                    if ty == tmaxy:
                        rysize = ysize % tsize
                    if rysize == 0:
                        rysize = tsize
                    ry = ysize - (ty * tsize) - rysize

                    wx, wy = 0, 0
                    wxsize = int(rxsize/float(tsize) * self.tilesize)
                    wysize = int(rysize/float(tsize) * self.tilesize)
                    if wysize != self.tilesize:
                        wy = self.tilesize - wysize

                # Read the source raster if anything is going inside the tile as per the computed
                # geo_query
                tile_details.append(
                    TileDetail(
                        tx=tx, ty=ytile, tz=tz, rx=rx, ry=ry, rxsize=rxsize, rysize=rysize, wx=wx,
                        wy=wy, wxsize=wxsize, wysize=wysize, querysize=querysize,
                    )
                )

        conf = TileJobInfo(
            src_file=self.tmp_vrt_filename,
            nb_data_bands=self.dataBandsCount,
            output_file_path=self.output_folder,
            tile_extension=self.tileext,
            tile_driver=self.tiledriver,
            tile_size=self.tilesize,
            kml=self.kml,
            tminmax=self.tminmax,
            tminz=self.tminz,
            tmaxz=self.tmaxz,
            in_srs_wkt=self.in_srs_wkt,
            out_geo_trans=self.out_gt,
            ominy=self.ominy,
            is_epsg_4326=self.isepsg4326,
            options=self.options,
        )

        return conf, tile_details

    def geo_query(self, ds, ulx, uly, lrx, lry, querysize=0):
        """
        For given dataset and query in cartographic coordinates returns parameters for ReadRaster()
        in raster coordinates and x/y shifts (for border tiles). If the querysize is not given, the
        extent is returned in the native resolution of dataset ds.

        raises Gdal2TilesError if the dataset does not contain anything inside this geo_query
        """
        geotran = ds.GetGeoTransform()
        rx = int((ulx - geotran[0]) / geotran[1] + 0.001)
        ry = int((uly - geotran[3]) / geotran[5] + 0.001)
        rxsize = int((lrx - ulx) / geotran[1] + 0.5)
        rysize = int((lry - uly) / geotran[5] + 0.5)

        if not querysize:
            wxsize, wysize = rxsize, rysize
        else:
            wxsize, wysize = querysize, querysize

        # Coordinates should not go out of the bounds of the raster
        wx = 0
        if rx < 0:
            rxshift = abs(rx)
            wx = int(wxsize * (float(rxshift) / rxsize))
            wxsize = wxsize - wx
            rxsize = rxsize - int(rxsize * (float(rxshift) / rxsize))
            rx = 0
        if rx+rxsize > ds.RasterXSize:
            wxsize = int(wxsize * (float(ds.RasterXSize - rx) / rxsize))
            rxsize = ds.RasterXSize - rx

        wy = 0
        if ry < 0:
            ryshift = abs(ry)
            wy = int(wysize * (float(ryshift) / rysize))
            wysize = wysize - wy
            rysize = rysize - int(rysize * (float(ryshift) / rysize))
            ry = 0
        if ry+rysize > ds.RasterYSize:
            wysize = int(wysize * (float(ds.RasterYSize - ry) / rysize))
            rysize = ds.RasterYSize - ry

        return (rx, ry, rxsize, rysize), (wx, wy, wxsize, wysize)

    def generate_tilemapresource(self):
        """
        Template for tilemapresource.xml. Returns filled string. Expected variables:
          title, north, south, east, west, isepsg4326, projection, publishurl,
          zoompixels, tilesize, tileformat, profile
        """

        args = {}
        args['title'] = self.options.title
        args['south'], args['west'], args['north'], args['east'] = self.swne
        args['tilesize'] = self.tilesize
        args['tileformat'] = self.tileext
        args['publishurl'] = self.options.url
        args['profile'] = self.options.profile

        if self.options.profile == 'mercator':
            args['srs'] = "EPSG:3857"
        elif self.options.profile == 'geodetic':
            args['srs'] = "EPSG:4326"
        elif self.options.s_srs:
            args['srs'] = self.options.s_srs
        elif self.out_srs:
            args['srs'] = self.out_srs.ExportToWkt()
        else:
            args['srs'] = ""

        s = """<?xml version="1.0" encoding="utf-8"?>
    <TileMap version="1.0.0" tilemapservice="http://tms.osgeo.org/1.0.0">
      <Title>%(title)s</Title>
      <Abstract></Abstract>
      <SRS>%(srs)s</SRS>
      <BoundingBox minx="%(west).14f" miny="%(south).14f" maxx="%(east).14f" maxy="%(north).14f"/>
      <Origin x="%(west).14f" y="%(south).14f"/>
      <TileFormat width="%(tilesize)d" height="%(tilesize)d" mime-type="image/%(tileformat)s" extension="%(tileformat)s"/>
      <TileSets profile="%(profile)s">
""" % args    # noqa
        for z in range(self.tminz, self.tmaxz+1):
            if self.options.profile == 'raster':
                s += """        <TileSet href="%s%d" units-per-pixel="%.14f" order="%d"/>\n""" % (
                    args['publishurl'], z, (2**(self.nativezoom-z) * self.out_gt[1]), z)
            elif self.options.profile == 'mercator':
                s += """        <TileSet href="%s%d" units-per-pixel="%.14f" order="%d"/>\n""" % (
                    args['publishurl'], z, 156543.0339/2**z, z)
            elif self.options.profile == 'geodetic':
                s += """        <TileSet href="%s%d" units-per-pixel="%.14f" order="%d"/>\n""" % (
                    args['publishurl'], z, 0.703125/2**z, z)
        s += """      </TileSets>
    </TileMap>
    """
        return s

    def generate_googlemaps(self):
        """
        Template for googlemaps.html implementing Overlay of tiles for 'mercator' profile.
        It returns filled string. Expected variables:
        title, googlemapskey, north, south, east, west, minzoom, maxzoom, tilesize, tileformat,
        publishurl
        """
        args = {}
        args['title'] = self.options.title
        args['googlemapskey'] = self.options.googlekey
        args['south'], args['west'], args['north'], args['east'] = self.swne
        args['minzoom'] = self.tminz
        args['maxzoom'] = self.tmaxz
        args['tilesize'] = self.tilesize
        args['tileformat'] = self.tileext
        args['publishurl'] = self.options.url
        args['copyright'] = self.options.copyright

        s = r"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml">
              <head>
                <title>%(title)s</title>
                <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
                <meta http-equiv='imagetoolbar' content='no'/>
                <style type="text/css"> v\:* {behavior:url(#default#VML);}
                    html, body { overflow: hidden; padding: 0; height: 100%%; width: 100%%; font-family: 'Lucida Grande',Geneva,Arial,Verdana,sans-serif; }
                    body { margin: 10px; background: #fff; }
                    h1 { margin: 0; padding: 6px; border:0; font-size: 20pt; }
                    #header { height: 43px; padding: 0; background-color: #eee; border: 1px solid #888; }
              #subheader { height: 12px; text-align: right; font-size: 10px; color: #555;}
              #map { height: 95%%; border: 1px solid #888; }
          </style>
          <script src='http://maps.google.com/maps?file=api&amp;v=2&amp;key=%(googlemapskey)s'></script>
          <script>
          //<![CDATA[

          /*
                 * Constants for given map
                 * TODO: read it from tilemapresource.xml
                 */

                var mapBounds = new GLatLngBounds(new GLatLng(%(south)s, %(west)s), new GLatLng(%(north)s, %(east)s));
                var mapMinZoom = %(minzoom)s;
                var mapMaxZoom = %(maxzoom)s;

                var opacity = 0.75;
                var map;
                var hybridOverlay;

                /*
                 * Create a Custom Opacity GControl
                 * http://www.maptiler.org/google-maps-overlay-opacity-control/
                 */

                var CTransparencyLENGTH = 58;
                // maximum width that the knob can move (slide width minus knob width)

                function CTransparencyControl( overlay ) {
                    this.overlay = overlay;
                    this.opacity = overlay.getTileLayer().getOpacity();
                }
                CTransparencyControl.prototype = new GControl();

                // This function positions the slider to match the specified opacity
                CTransparencyControl.prototype.setSlider = function(pos) {
                    var left = Math.round((CTransparencyLENGTH*pos));
                    this.slide.left = left;
                    this.knob.style.left = left+"px";
                    this.knob.style.top = "0px";
                }

                // This function reads the slider and sets the overlay opacity level
                CTransparencyControl.prototype.setOpacity = function() {
                    // set the global variable
                    opacity = this.slide.left/CTransparencyLENGTH;
                    this.map.clearOverlays();
                    this.map.addOverlay(this.overlay, { zPriority: 0 });
                    if (this.map.getCurrentMapType() == G_HYBRID_MAP) {
                        this.map.addOverlay(hybridOverlay);
                    }
                }

                // This gets called by the API when addControl(new CTransparencyControl())
                CTransparencyControl.prototype.initialize = function(map) {
                    var that=this;
                    this.map = map;

                    // Is this MSIE, if so we need to use AlphaImageLoader
                    var agent = navigator.userAgent.toLowerCase();
                    if ((agent.indexOf("msie") > -1) && (agent.indexOf("opera") < 1)){this.ie = true} else {this.ie = false}

                    // create the background graphic as a <div> containing an image
                    var container = document.createElement("div");
                    container.style.width="70px";
                    container.style.height="21px";

                    // Handle transparent PNG files in MSIE
                    if (this.ie) {
                      var loader = "filter:progid:DXImageTransform.Microsoft.AlphaImageLoader(src='http://www.maptiler.org/img/opacity-slider.png', sizingMethod='crop');";
                      container.innerHTML = '<div style="height:21px; width:70px; ' +loader+ '" ></div>';
                    } else {
                      container.innerHTML = '<div style="height:21px; width:70px; background-image: url(http://www.maptiler.org/img/opacity-slider.png)" ></div>';
                    }

                    // create the knob as a GDraggableObject
                    // Handle transparent PNG files in MSIE
                    if (this.ie) {
                      var loader = "progid:DXImageTransform.Microsoft.AlphaImageLoader(src='http://www.maptiler.org/img/opacity-slider.png', sizingMethod='crop');";
                      this.knob = document.createElement("div");
                      this.knob.style.height="21px";
                      this.knob.style.width="13px";
                  this.knob.style.overflow="hidden";
                      this.knob_img = document.createElement("div");
                      this.knob_img.style.height="21px";
                      this.knob_img.style.width="83px";
                      this.knob_img.style.filter=loader;
                  this.knob_img.style.position="relative";
                  this.knob_img.style.left="-70px";
                      this.knob.appendChild(this.knob_img);
                    } else {
                      this.knob = document.createElement("div");
                      this.knob.style.height="21px";
                      this.knob.style.width="13px";
                      this.knob.style.backgroundImage="url(http://www.maptiler.org/img/opacity-slider.png)";
                      this.knob.style.backgroundPosition="-70px 0px";
                    }
                    container.appendChild(this.knob);
                    this.slide=new GDraggableObject(this.knob, {container:container});
                    this.slide.setDraggableCursor('pointer');
                    this.slide.setDraggingCursor('pointer');
                    this.container = container;

                    // attach the control to the map
                    map.getContainer().appendChild(container);

                    // init slider
                    this.setSlider(this.opacity);

                    // Listen for the slider being moved and set the opacity
                    GEvent.addListener(this.slide, "dragend", function() {that.setOpacity()});
                    //GEvent.addListener(this.container, "click", function( x, y ) { alert(x, y) });

                    return container;
                  }

                  // Set the default position for the control
                  CTransparencyControl.prototype.getDefaultPosition = function() {
                    return new GControlPosition(G_ANCHOR_TOP_RIGHT, new GSize(7, 47));
                  }

                /*
                 * Full-screen Window Resize
                 */

                function getWindowHeight() {
                    if (self.innerHeight) return self.innerHeight;
                    if (document.documentElement && document.documentElement.clientHeight)
                        return document.documentElement.clientHeight;
                    if (document.body) return document.body.clientHeight;
                    return 0;
                }

                function getWindowWidth() {
                    if (self.innerWidth) return self.innerWidth;
                    if (document.documentElement && document.documentElement.clientWidth)
                        return document.documentElement.clientWidth;
                    if (document.body) return document.body.clientWidth;
                    return 0;
                }

                function resize() {
                    var map = document.getElementById("map");
                    var header = document.getElementById("header");
                    var subheader = document.getElementById("subheader");
                    map.style.height = (getWindowHeight()-80) + "px";
                    map.style.width = (getWindowWidth()-20) + "px";
                    header.style.width = (getWindowWidth()-20) + "px";
                    subheader.style.width = (getWindowWidth()-20) + "px";
                    // map.checkResize();
                }


                /*
                 * Main load function:
                 */

                function load() {

                   if (GBrowserIsCompatible()) {

                      // Bug in the Google Maps: Copyright for Overlay is not correctly displayed
                      var gcr = GMapType.prototype.getCopyrights;
                      GMapType.prototype.getCopyrights = function(bounds,zoom) {
                          return ["%(copyright)s"].concat(gcr.call(this,bounds,zoom));
                      }

                      map = new GMap2( document.getElementById("map"), { backgroundColor: '#fff' } );

                      map.addMapType(G_PHYSICAL_MAP);
                      map.setMapType(G_PHYSICAL_MAP);

                      map.setCenter( mapBounds.getCenter(), map.getBoundsZoomLevel( mapBounds ));

                      hybridOverlay = new GTileLayerOverlay( G_HYBRID_MAP.getTileLayers()[1] );
                      GEvent.addListener(map, "maptypechanged", function() {
                        if (map.getCurrentMapType() == G_HYBRID_MAP) {
                            map.addOverlay(hybridOverlay);
                        } else {
                           map.removeOverlay(hybridOverlay);
                        }
                      } );

                      var tilelayer = new GTileLayer(GCopyrightCollection(''), mapMinZoom, mapMaxZoom);
                      var mercator = new GMercatorProjection(mapMaxZoom+1);
                      tilelayer.getTileUrl = function(tile,zoom) {
                          if ((zoom < mapMinZoom) || (zoom > mapMaxZoom)) {
                              return "http://www.maptiler.org/img/none.png";
                          }
                          var ymax = 1 << zoom;
                          var y = ymax - tile.y -1;
                          var tileBounds = new GLatLngBounds(
                              mercator.fromPixelToLatLng( new GPoint( (tile.x)*256, (tile.y+1)*256 ) , zoom ),
                              mercator.fromPixelToLatLng( new GPoint( (tile.x+1)*256, (tile.y)*256 ) , zoom )
                          );
                          if (mapBounds.intersects(tileBounds)) {
                              return zoom+"/"+tile.x+"/"+y+".png";
                          } else {
                              return "http://www.maptiler.org/img/none.png";
                          }
                      }
                      // IE 7-: support for PNG alpha channel
                      // Unfortunately, the opacity for whole overlay is then not changeable, either or...
                      tilelayer.isPng = function() { return true;};
                      tilelayer.getOpacity = function() { return opacity; }

                      overlay = new GTileLayerOverlay( tilelayer );
                      map.addOverlay(overlay);

                      map.addControl(new GLargeMapControl());
                      map.addControl(new GHierarchicalMapTypeControl());
                      map.addControl(new CTransparencyControl( overlay ));
        """ % args    # noqa
        if self.kml:
            s += """
                      map.addMapType(G_SATELLITE_3D_MAP);
                      map.getEarthInstance(getEarthInstanceCB);
        """
        s += """

                      map.enableContinuousZoom();
                      map.enableScrollWheelZoom();

                      map.setMapType(G_HYBRID_MAP);
                   }
                   resize();
                }
        """
        if self.kml:
            s += """
                function getEarthInstanceCB(object) {
                   var ge = object;

                   if (ge) {
                       var url = document.location.toString();
                       url = url.substr(0,url.lastIndexOf('/'))+'/doc.kml';
                       var link = ge.createLink("");
                       if ("%(publishurl)s") { link.setHref("%(publishurl)s/doc.kml") }
                       else { link.setHref(url) };
                       var networkLink = ge.createNetworkLink("");
                       networkLink.setName("TMS Map Overlay");
                       networkLink.setFlyToView(true);
                       networkLink.setLink(link);
                       ge.getFeatures().appendChild(networkLink);
                   } else {
                       // alert("You should open a KML in Google Earth");
                       // add div with the link to generated KML... - maybe JavaScript redirect to the URL of KML?
                   }
                }
        """ % args    # noqa
        s += """
                onresize=function(){ resize(); };

                //]]>
                </script>
              </head>
              <body onload="load()">
                  <div id="header"><h1>%(title)s</h1></div>
                  <div id="subheader">Generated by <a href="http://www.klokan.cz/projects/gdal2tiles/">GDAL2Tiles</a>, Copyright &copy; 2008 <a href="http://www.klokan.cz/">Klokan Petr Pridal</a>,  <a href="http://www.gdal.org/">GDAL</a> &amp; <a href="http://www.osgeo.org/">OSGeo</a> <a href="http://code.google.com/soc/">GSoC</a>
            <!-- PLEASE, LET THIS NOTE ABOUT AUTHOR AND PROJECT SOMEWHERE ON YOUR WEBSITE, OR AT LEAST IN THE COMMENT IN HTML. THANK YOU -->
                  </div>
                   <div id="map"></div>
              </body>
            </html>
        """ % args    # noqa

        return s

    def generate_leaflet(self):
        """
        Template for leaflet.html implementing overlay of tiles for 'mercator' profile.
        It returns filled string. Expected variables:
        title, north, south, east, west, minzoom, maxzoom, tilesize, tileformat, publishurl
        """

        args = {}
        args['title'] = self.options.title.replace('"', '\\"')
        args['htmltitle'] = self.options.title
        args['south'], args['west'], args['north'], args['east'] = self.swne
        args['centerlon'] = (args['north'] + args['south']) / 2.
        args['centerlat'] = (args['west'] + args['east']) / 2.
        args['minzoom'] = self.tminz
        args['maxzoom'] = self.tmaxz
        args['beginzoom'] = self.tmaxz
        args['tilesize'] = self.tilesize  # not used
        args['tileformat'] = self.tileext
        args['publishurl'] = self.options.url  # not used
        args['copyright'] = self.options.copyright.replace('"', '\\"')

        s = """<!DOCTYPE html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <meta name='viewport' content='width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no' />
            <title>%(htmltitle)s</title>

            <!-- Leaflet -->
            <link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.7.5/leaflet.css" />
            <script src="http://cdn.leafletjs.com/leaflet-0.7.5/leaflet.js"></script>

            <style>
                body { margin:0; padding:0; }
                body, table, tr, td, th, div, h1, h2, input { font-family: "Calibri", "Trebuchet MS", "Ubuntu", Serif; font-size: 11pt; }
                #map { position:absolute; top:0; bottom:0; width:100%%; } /* full size */
                .ctl {
                    padding: 2px 10px 2px 10px;
                    background: white;
                    background: rgba(255,255,255,0.9);
                    box-shadow: 0 0 15px rgba(0,0,0,0.2);
                    border-radius: 5px;
                    text-align: right;
                }
                .title {
                    font-size: 18pt;
                    font-weight: bold;
                }
                .src {
                    font-size: 10pt;
                }

            </style>

        </head>
        <body>

        <div id="map"></div>

        <script>
        /* **** Leaflet **** */

        // Base layers
        //  .. OpenStreetMap
        var osm = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'});

        //  .. CartoDB Positron
        var cartodb = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'});

        //  .. OSM Toner
        var toner = L.tileLayer('http://{s}.tile.stamen.com/toner/{z}/{x}/{y}.png', {attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.'});

        //  .. White background
        var white = L.tileLayer("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQAAAAEAAQMAAABmvDolAAAAA1BMVEX///+nxBvIAAAAH0lEQVQYGe3BAQ0AAADCIPunfg43YAAAAAAAAAAA5wIhAAAB9aK9BAAAAABJRU5ErkJggg==");

        // Overlay layers (TMS)
        var lyr = L.tileLayer('./{z}/{x}/{y}.%(tileformat)s', {tms: true, opacity: 0.7, attribution: "%(copyright)s"});

        // Map
        var map = L.map('map', {
            center: [%(centerlon)s, %(centerlat)s],
            zoom: %(beginzoom)s,
            minZoom: %(minzoom)s,
            maxZoom: %(maxzoom)s,
            layers: [osm]
        });

        var basemaps = {"OpenStreetMap": osm, "CartoDB Positron": cartodb, "Stamen Toner": toner, "Without background": white}
        var overlaymaps = {"Layer": lyr}

        // Title
        var title = L.control();
        title.onAdd = function(map) {
            this._div = L.DomUtil.create('div', 'ctl title');
            this.update();
            return this._div;
        };
        title.update = function(props) {
            this._div.innerHTML = "%(title)s";
        };
        title.addTo(map);

        // Note
        var src = 'Generated by <a href="http://www.klokan.cz/projects/gdal2tiles/">GDAL2Tiles</a>, Copyright &copy; 2008 <a href="http://www.klokan.cz/">Klokan Petr Pridal</a>,  <a href="http://www.gdal.org/">GDAL</a> &amp; <a href="http://www.osgeo.org/">OSGeo</a> <a href="http://code.google.com/soc/">GSoC</a>';
        var title = L.control({position: 'bottomleft'});
        title.onAdd = function(map) {
            this._div = L.DomUtil.create('div', 'ctl src');
            this.update();
            return this._div;
        };
        title.update = function(props) {
            this._div.innerHTML = src;
        };
        title.addTo(map);


        // Add base layers
        L.control.layers(basemaps, overlaymaps, {collapsed: false}).addTo(map);

        // Fit to overlay bounds (SW and NE points with (lat, lon))
        map.fitBounds([[%(south)s, %(east)s], [%(north)s, %(west)s]]);

        </script>

        </body>
        </html>

        """ % args    # noqa

        return s

    def generate_openlayers(self):
        """
        Template for openlayers.html implementing overlay of available Spherical Mercator layers.

        It returns filled string. Expected variables:
        title, bingkey, north, south, east, west, minzoom, maxzoom, tilesize, tileformat, publishurl
        """

        args = {}
        args['title'] = self.options.title
        args['bingkey'] = self.options.bingkey
        args['south'], args['west'], args['north'], args['east'] = self.swne
        args['minzoom'] = self.tminz
        args['maxzoom'] = self.tmaxz
        args['tilesize'] = self.tilesize
        args['tileformat'] = self.tileext
        args['publishurl'] = self.options.url
        args['copyright'] = self.options.copyright
        if self.options.tmscompatible:
            args['tmsoffset'] = "-1"
        else:
            args['tmsoffset'] = ""
        if self.options.profile == 'raster':
            args['rasterzoomlevels'] = self.tmaxz+1
            args['rastermaxresolution'] = 2**(self.nativezoom) * self.out_gt[1]

        s = r"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml"
          <head>
            <title>%(title)s</title>
            <meta http-equiv='imagetoolbar' content='no'/>
            <style type="text/css"> v\:* {behavior:url(#default#VML);}
                html, body { overflow: hidden; padding: 0; height: 100%%; width: 100%%; font-family: 'Lucida Grande',Geneva,Arial,Verdana,sans-serif; }
                body { margin: 10px; background: #fff; }
                h1 { margin: 0; padding: 6px; border:0; font-size: 20pt; }
            #header { height: 43px; padding: 0; background-color: #eee; border: 1px solid #888; }
            #subheader { height: 12px; text-align: right; font-size: 10px; color: #555;}
            #map { height: 95%%; border: 1px solid #888; }
            .olImageLoadError { display: none; }
            .olControlLayerSwitcher .layersDiv { border-radius: 10px 0 0 10px; }
        </style>""" % args    # noqa

        if self.options.profile == 'mercator':
            s += """
            <script src='http://maps.google.com/maps/api/js?sensor=false&v=3.7'></script>
            """ % args

        s += """
            <script src="http://www.openlayers.org/api/2.12/OpenLayers.js"></script>
            <script>
              var map;
              var mapBounds = new OpenLayers.Bounds( %(west)s, %(south)s, %(east)s, %(north)s);
              var mapMinZoom = %(minzoom)s;
              var mapMaxZoom = %(maxzoom)s;
              var emptyTileURL = "http://www.maptiler.org/img/none.png";
              OpenLayers.IMAGE_RELOAD_ATTEMPTS = 3;

              function init(){""" % args

        if self.options.profile == 'mercator':
            s += """
                  var options = {
                      div: "map",
                      controls: [],
                      projection: "EPSG:3857",
                      displayProjection: new OpenLayers.Projection("EPSG:4326"),
                      numZoomLevels: 20
                  };
                  map = new OpenLayers.Map(options);

                  // Create Google Mercator layers
                  var gmap = new OpenLayers.Layer.Google("Google Streets",
                  {
                      type: google.maps.MapTypeId.ROADMAP,
                      sphericalMercator: true
                  });
                  var gsat = new OpenLayers.Layer.Google("Google Satellite",
                  {
                      type: google.maps.MapTypeId.SATELLITE,
                      sphericalMercator: true
                  });
                  var ghyb = new OpenLayers.Layer.Google("Google Hybrid",
                  {
                      type: google.maps.MapTypeId.HYBRID,
                      sphericalMercator: true
                  });
                  var gter = new OpenLayers.Layer.Google("Google Terrain",
                  {
                      type: google.maps.MapTypeId.TERRAIN,
                      sphericalMercator: true
                  });

                  // Create Bing layers
                  var broad = new OpenLayers.Layer.Bing({
                      name: "Bing Roads",
                      key: "%(bingkey)s",
                      type: "Road",
                      sphericalMercator: true
                  });
                  var baer = new OpenLayers.Layer.Bing({
                      name: "Bing Aerial",
                      key: "%(bingkey)s",
                      type: "Aerial",
                      sphericalMercator: true
                  });
                  var bhyb = new OpenLayers.Layer.Bing({
                      name: "Bing Hybrid",
                      key: "%(bingkey)s",
                      type: "AerialWithLabels",
                      sphericalMercator: true
                  });

                  // Create OSM layer
                  var osm = new OpenLayers.Layer.OSM("OpenStreetMap");

          """ % args    # noqa
		  
            if self.options.xyz:
                s += """		  
                  // create TMS Overlay layer
                   var tmsoverlay = new OpenLayers.Layer.XYZ("XYZ Overlay",
                      "${z}/${x}/${y}.png", {
                      transitionEffect: 'resize',
                      isBaseLayer: false
                  });
				  
		        """ % args    # noqa
            else:
                s += """		  
                  // create TMS Overlay layer
                   var tmsoverlay = new OpenLayers.Layer.TMS("TMS Overlay", "",
                  {
                      serviceVersion: '.',
                      layername: '.',
                      alpha: true,
                      type: '%(tileformat)s',
                      isBaseLayer: false,
                      getURL: getURL
                  });
				  
		        """ % args    # noqa		  
		  
            s += """  
                  if (OpenLayers.Util.alphaHack() == false) {
                      tmsoverlay.setOpacity(0.7);
                  }

                  map.addLayers([gmap, gsat, ghyb, gter,
                                 broad, baer, bhyb,
                                 osm, tmsoverlay]);

                  var switcherControl = new OpenLayers.Control.LayerSwitcher();
                  map.addControl(switcherControl);
                  switcherControl.maximizeControl();

                  map.zoomToExtent(mapBounds.transform(map.displayProjection, map.projection));
          """ % args    # noqa

        elif self.options.profile == 'geodetic':
            s += """
                  var options = {
                      div: "map",
                      controls: [],
                      projection: "EPSG:4326"
                  };
                  map = new OpenLayers.Map(options);

                  var wms = new OpenLayers.Layer.WMS("VMap0",
                      "http://tilecache.osgeo.org/wms-c/Basic.py?",
                      {
                          layers: 'basic',
                          format: 'image/png'
                      }
                  );
                  var tmsoverlay = new OpenLayers.Layer.TMS("TMS Overlay", "",
                  {
                      serviceVersion: '.',
                      layername: '.',
                      alpha: true,
                      type: '%(tileformat)s',
                      isBaseLayer: false,
                      getURL: getURL
                  });
                  if (OpenLayers.Util.alphaHack() == false) {
                      tmsoverlay.setOpacity(0.7);
                  }

                  map.addLayers([wms,tmsoverlay]);

                  var switcherControl = new OpenLayers.Control.LayerSwitcher();
                  map.addControl(switcherControl);
                  switcherControl.maximizeControl();

                  map.zoomToExtent(mapBounds);
           """ % args   # noqa

        elif self.options.profile == 'raster':
            s += """
                  var options = {
                      div: "map",
                      controls: [],
                      maxExtent: new OpenLayers.Bounds(%(west)s, %(south)s, %(east)s, %(north)s),
                      maxResolution: %(rastermaxresolution)f,
                      numZoomLevels: %(rasterzoomlevels)d
                  };
                  map = new OpenLayers.Map(options);

                  var layer = new OpenLayers.Layer.TMS("TMS Layer", "",
                  {
                      serviceVersion: '.',
                      layername: '.',
                      alpha: true,
                      type: '%(tileformat)s',
                      getURL: getURL
                  });

                  map.addLayer(layer);
                  map.zoomToExtent(mapBounds);
        """ % args    # noqa

        s += """
                  map.addControls([new OpenLayers.Control.PanZoomBar(),
                                   new OpenLayers.Control.Navigation(),
                                   new OpenLayers.Control.MousePosition(),
                                   new OpenLayers.Control.ArgParser(),
                                   new OpenLayers.Control.Attribution()]);
              }
        """ % args

        if self.options.profile == 'mercator' and self.options.xyz is None:
            s += """
              function getURL(bounds) {
                  bounds = this.adjustBounds(bounds);
                  var res = this.getServerResolution();
                  var x = Math.round((bounds.left - this.tileOrigin.lon) / (res * this.tileSize.w));
                  var y = Math.round((bounds.bottom - this.tileOrigin.lat) / (res * this.tileSize.h));
                  var z = this.getServerZoom();
                  if (this.map.baseLayer.CLASS_NAME === 'OpenLayers.Layer.Bing') {
                      z+=1;
                  }
                  var path = this.serviceVersion + "/" + this.layername + "/" + z + "/" + x + "/" + y + "." + this.type;
                  var url = this.url;
                  if (OpenLayers.Util.isArray(url)) {
                      url = this.selectUrl(path, url);
                  }
                  if (mapBounds.intersectsBounds(bounds) && (z >= mapMinZoom) && (z <= mapMaxZoom)) {
                      return url + path;
                  } else {
                      return emptyTileURL;
                  }
              }
            """ % args    # noqa

        elif self.options.profile == 'geodetic':
            s += """
              function getURL(bounds) {
                  bounds = this.adjustBounds(bounds);
                  var res = this.getServerResolution();
                  var x = Math.round((bounds.left - this.tileOrigin.lon) / (res * this.tileSize.w));
                  var y = Math.round((bounds.bottom - this.tileOrigin.lat) / (res * this.tileSize.h));
                  var z = this.getServerZoom()%(tmsoffset)s;
                  var path = this.serviceVersion + "/" + this.layername + "/" + z + "/" + x + "/" + y + "." + this.type;
                  var url = this.url;
                  if (OpenLayers.Util.isArray(url)) {
                      url = this.selectUrl(path, url);
                  }
                  if (mapBounds.intersectsBounds(bounds) && (z >= mapMinZoom) && (z <= mapMaxZoom)) {
                      return url + path;
                  } else {
                      return emptyTileURL;
                  }
              }
            """ % args    # noqa

        elif self.options.profile == 'raster':
            s += """
              function getURL(bounds) {
                  bounds = this.adjustBounds(bounds);
                  var res = this.getServerResolution();
                  var x = Math.round((bounds.left - this.tileOrigin.lon) / (res * this.tileSize.w));
                  var y = Math.round((bounds.bottom - this.tileOrigin.lat) / (res * this.tileSize.h));
                  var z = this.getServerZoom();
                  var path = this.serviceVersion + "/" + this.layername + "/" + z + "/" + x + "/" + y + "." + this.type;
                  var url = this.url;
                  if (OpenLayers.Util.isArray(url)) {
                      url = this.selectUrl(path, url);
                  }
                  if (mapBounds.intersectsBounds(bounds) && (z >= mapMinZoom) && (z <= mapMaxZoom)) {
                      return url + path;
                  } else {
                      return emptyTileURL;
                  }
              }
            """ % args    # noqa

        s += """
           function getWindowHeight() {
                if (self.innerHeight) return self.innerHeight;
                    if (document.documentElement && document.documentElement.clientHeight)
                        return document.documentElement.clientHeight;
                    if (document.body) return document.body.clientHeight;
                        return 0;
                }

                function getWindowWidth() {
                    if (self.innerWidth) return self.innerWidth;
                    if (document.documentElement && document.documentElement.clientWidth)
                        return document.documentElement.clientWidth;
                    if (document.body) return document.body.clientWidth;
                        return 0;
                }

                function resize() {
                    var map = document.getElementById("map");
                    var header = document.getElementById("header");
                    var subheader = document.getElementById("subheader");
                    map.style.height = (getWindowHeight()-80) + "px";
                    map.style.width = (getWindowWidth()-20) + "px";
                    header.style.width = (getWindowWidth()-20) + "px";
                    subheader.style.width = (getWindowWidth()-20) + "px";
                    if (map.updateSize) { map.updateSize(); };
                }

                onresize=function(){ resize(); };

                </script>
              </head>
              <body onload="init()">
                <div id="header"><h1>%(title)s</h1></div>
                <div id="subheader">Generated by <a href="http://www.klokan.cz/projects/gdal2tiles/">GDAL2Tiles</a>, Copyright &copy; 2008 <a href="http://www.klokan.cz/">Klokan Petr Pridal</a>,  <a href="http://www.gdal.org/">GDAL</a> &amp; <a href="http://www.osgeo.org/">OSGeo</a> <a href="http://code.google.com/soc/">GSoC</a>
                <!-- PLEASE, LET THIS NOTE ABOUT AUTHOR AND PROJECT SOMEWHERE ON YOUR WEBSITE, OR AT LEAST IN THE COMMENT IN HTML. THANK YOU -->
                </div>
                <div id="map"></div>
                <script type="text/javascript" >resize()</script>
              </body>
            </html>""" % args   # noqa

        return s

    @staticmethod
    def getYtile(ty, tz, options):
        """
        Calculates the y-tile number based on whether XYZ or TMS (default) system is used
        :param ty: The y-tile number
        :return: The transformed tile number
        """
        if options.xyz:
            return (2**tz - 1) - ty  # Convert from TMS to XYZ numbering system
        else:
            return ty


def worker_tile_details(input_file, output_folder, options, send_pipe=None):
    try:
        gdal2tiles = GDAL2Tiles(input_file, output_folder, options)
        gdal2tiles.open_input()
        gdal2tiles.generate_metadata()
        tile_job_info, tile_details = gdal2tiles.generate_base_tiles()
        return_data = (tile_job_info, tile_details)
        if send_pipe:
            send_pipe.send(return_data)

        return return_data
    except Exception as e:
        print("worker_tile_details failed ", str(e))


def progress_printer_thread(queue, nb_jobs):
    pb = ProgressBar(nb_jobs)
    pb.start()
    for _ in range(nb_jobs):
        queue.get()
        pb.log_progress()
        queue.task_done()


class ProgressBar(object):

    def __init__(self, total_items):
        self.total_items = total_items
        self.nb_items_done = 0
        self.current_progress = 0
        self.STEP = 2.5

    def start(self):
        sys.stdout.write("0")

    def log_progress(self, nb_items=1):
        self.nb_items_done += nb_items
        progress = float(self.nb_items_done) / self.total_items * 100
        if progress >= self.current_progress + self.STEP:
            done = False
            while not done:
                if self.current_progress + self.STEP <= progress:
                    self.current_progress += self.STEP
                    if self.current_progress % 10 == 0:
                        sys.stdout.write(str(int(self.current_progress)))
                        if self.current_progress == 100:
                            sys.stdout.write("\n")
                    else:
                        sys.stdout.write(".")
                else:
                    done = True
        sys.stdout.flush()


def get_tile_swne(tile_job_info, options):
    if options.profile == 'mercator':
        mercator = GlobalMercator()
        tile_swne = mercator.TileLatLonBounds
    elif options.profile == 'geodetic':
        geodetic = GlobalGeodetic(options.tmscompatible)
        tile_swne = geodetic.TileLatLonBounds
    elif options.profile == 'raster':
        srs4326 = osr.SpatialReference()
        srs4326.ImportFromEPSG(4326)
        if tile_job_info.kml and tile_job_info.in_srs_wkt:
            in_srs = osr.SpatialReference()
            in_srs.ImportFromWkt(tile_job_info.in_srs_wkt)
            ct = osr.CoordinateTransformation(in_srs, srs4326)

            def rastertileswne(x, y, z):
                pixelsizex = (2 ** (tile_job_info.tmaxz - z) * tile_job_info.out_geo_trans[1])
                west = tile_job_info.out_geo_trans[0] + x * tile_job_info.tilesize * pixelsizex
                east = west + tile_job_info.tilesize * pixelsizex
                south = tile_job_info.ominy + y * tile_job_info.tilesize * pixelsizex
                north = south + tile_job_info.tilesize * pixelsizex
                if not tile_job_info.is_epsg_4326:
                    # Transformation to EPSG:4326 (WGS84 datum)
                    west, south = ct.TransformPoint(west, south)[:2]
                    east, north = ct.TransformPoint(east, north)[:2]
                return south, west, north, east

            tile_swne = rastertileswne
        else:
            tile_swne = lambda x, y, z: (0, 0, 0, 0)   # noqa
    else:
        tile_swne = lambda x, y, z: (0, 0, 0, 0)   # noqa

    return tile_swne


def single_threaded_tiling(input_file, output_folder, options):
    """
    Keep a single threaded version that stays clear of multiprocessing, for platforms that would not
    support it
    """
    if options.verbose:
        print("Begin tiles details calc")
    conf, tile_details = worker_tile_details(input_file, output_folder, options)

    if options.verbose:
        print("Tiles details calc complete.")

    if not options.verbose and not options.quiet:
        progress_bar = ProgressBar(len(tile_details))
        progress_bar.start()

    for tile_detail in tile_details:
        create_base_tile(conf, tile_detail, options)

        if not options.verbose and not options.quiet:
            progress_bar.log_progress()

    create_overview_tiles(conf, output_folder, options)

    shutil.rmtree(os.path.dirname(conf.src_file))


def multi_threaded_tiling(input_file, output_folder, options):
    nb_processes = options.nb_processes or 1
    (conf_receiver, conf_sender) = Pipe(False)

    if options.verbose:
        print("Begin tiles details calc")
    p = Process(target=worker_tile_details,
                args=[input_file, output_folder, options],
                kwargs={"send_pipe": conf_sender})
    p.start()
    # Make sure to consume the queue before joining. If the payload is too big, it won't be put in
    # one go in the queue and therefore the sending process will never finish, waiting for space in
    # the queue to send data
    conf, tile_details = conf_receiver.recv()
    p.join()
    if options.verbose:
        print("Tiles details calc complete.")
    # Have to create the Queue through a multiprocessing.Manager to get a Queue Proxy,
    # otherwise you can't pass it as a param in the method invoked by the pool...
    manager = Manager()
    queue = manager.Queue()
    pool = Pool(processes=nb_processes)
    # TODO: gbataille - check the confs for which each element is an array... one useless level?
    # TODO: gbataille - assign an ID to each job for print in verbose mode "ReadRaster Extent ..."
    # TODO: gbataille - check memory footprint and time on big image. are they opened x times
    for tile_detail in tile_details:
        pool.apply_async(create_base_tile, (conf, tile_detail, options), {"queue": queue})

    if not options.verbose and not options.quiet:
        p = Process(target=progress_printer_thread, args=[queue, len(tile_details)])
        p.start()

    pool.close()
    pool.join()     # Jobs finished
    if not options.verbose and not options.quiet:
        p.join()        # Traces done

    create_overview_tiles(conf, output_folder, options)

    shutil.rmtree(os.path.dirname(conf.src_file))


# def main():
#     # TODO: gbataille - use mkdtemp to work in a temp directory
#     # TODO: gbataille - debug intermediate tiles.vrt not produced anymore?
#     # TODO: gbataille - Refactor generate overview tiles to not depend on self variables
#     argv = gdal.GeneralCmdLineProcessor(sys.argv)
#     input_file, output_folder, options = process_args(argv[1:])
#     nb_processes = options.nb_processes or 1
#
#     if nb_processes == 1:
#         single_threaded_tiling(input_file, output_folder, options)
#     else:
#         multi_threaded_tiling(input_file, output_folder, options)
#
# if __name__ == '__main__':
#     # start_time = time.time()
#     main()
#     # print("--- %s seconds ---" % (time.time() - start_time))

#gdal_translate -of vrt -expand rgba F:\Danilo\Trampo\data_dir\data\remanescentes_florestais_desmatamento\brasil\prodes\prodes.tif prodes.vrt
# input_file = "F:\\Danilo\\Trampo\\data_dir\\data\\remanescentes_florestais_desmatamento\\brasil\\prodes\\prodes.vrt" #"F:\\Danilo\\Trampo\\data_dir\\data\\remanescentes_florestais_desmatamento\\brasil\\perda_cobertura_vegetal_ano_hansen\\lossyear.tif"
# output_folder = "F:\\Danilo\\Temp\\result\\prodes_publish\\"
#generateTileForMap(input_file, output_folder)

class Options:
    profile = "mercator"
    resampling = 'near'
    s_srs = None
    zoom= '0-2'
    resume = False
    srcnodata = ''
    tmscompatible = False
    xyz = True
    verbose = False
    quiet = True
    nb_processes = 1
    kml = False
    url = ''
    webviewer ='none'
    title = ''
    copyright = ''
    googlekey = ''
    bingkey = ''
    legendObj = None
    generatedFiles = []

def generateTileForMap(input_file, output_folder, maxZoom, resume, legendObj):
    options = Options()
    options.verbose = False
    options.resampling = 'near'
    options.zoom = '0-' + str(maxZoom)
    options.resume = resume
    options.legendObj = legendObj
    single_threaded_tiling(input_file, output_folder, options)
    for filename in options.generatedFiles:
        applyLegend(filename, options.legendObj)
    #multi_threaded_tiling(input_file, output_folder, options)


try:
    from WMSCapabilities import WMSCapabilities
    from WMSCapabilities import WMSBBox
except:
    pass #Not in Dinamica Code

#!/usr/bin/env python
# -*- coding: utf-8 -*-


isDinamica = False
try:
    dinamica.package("os")
    isDinamica = True
except:
    isDinamica = False

if not isDinamica:
    try:
        from .UTILS import UTILS
        from . import xmltodict
    except:
        pass #Not in QGIS

    try:
        from UTILS import UTILS
        from xmltodict import xmltodict
    except:
        pass #Not in Dinamica Code

from collections import OrderedDict
import collections
from pathlib import Path
import json
import os
import io
import csv
import re

# try:
#     from qgis.core import (QgsCoordinateReferenceSystem, QgsProject, QgsPointXY, QgsCoordinateTransform, QgsVectorLayer)
# except:
#     pass

class WMSCapabilities:

    @staticmethod
    def getDefaultCapabilities():
        return '''<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE WMT_MS_Capabilities SYSTEM "http://maps.csr.ufmg.br:80/geoserver/schemas/wms/1.1.1/WMS_MS_Capabilities.dtd"[
    <!ELEMENT VendorSpecificCapabilities (TileSet*) >
    <!ELEMENT TileSet (SRS, BoundingBox?, Resolutions, Width, Height, Format, Layers*, Styles*) >
    <!ELEMENT Resolutions (#PCDATA) >
    <!ELEMENT Width (#PCDATA) >
    <!ELEMENT Height (#PCDATA) >
    <!ELEMENT Layers (#PCDATA) >
    <!ELEMENT Styles (#PCDATA) >
    ]>
    <WMT_MS_Capabilities version="1.1.1" updateSequence="63258">
      <Service>
        <Name>OGC:WMS</Name>
        <Title>CSR Web Map Service</Title>
        <Abstract>Compliant WMS Response</Abstract>
        <KeywordList>
          <Keyword>WFS</Keyword>
          <Keyword>WMS</Keyword>
          <Keyword>GEOSERVER</Keyword>
        </KeywordList>
        <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="http://geoserver.sourceforge.net/html/index.php"/>
        <ContactInformation>
          <ContactPersonPrimary>
            <ContactPerson>GITHUB owner</ContactPerson>
            <ContactOrganization>GITHUB owner</ContactOrganization>
          </ContactPersonPrimary>
          <ContactPosition>Chief geographer</ContactPosition>
          <ContactAddress>
            <AddressType>Work</AddressType>
            <Address/>
            <City>Alexandria</City>
            <StateOrProvince/>
            <PostCode/>
            <Country>Egypt</Country>
          </ContactAddress>
          <ContactVoiceTelephone/>
          <ContactFacsimileTelephone/>
          <ContactElectronicMailAddress>claudius.ptolomaeus@gmail.com</ContactElectronicMailAddress>
        </ContactInformation>
        <Fees>NONE</Fees>
        <AccessConstraints>NONE</AccessConstraints>
      </Service>
      <Capability>
        <Request>
          <GetCapabilities>
            <Format>application/vnd.ogc.wms_xml</Format>
            <DCPType>
              <HTTP>
                <Get>
                  <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="http://maps.csr.ufmg.br:80/geoserver/wms?SERVICE=WMS&amp;"/>
                </Get>
                <Post>
                  <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="http://maps.csr.ufmg.br:80/geoserver/wms?SERVICE=WMS&amp;"/>
                </Post>
              </HTTP>
            </DCPType>
          </GetCapabilities>
          <GetMap>
            <Format>image/png</Format>
            <DCPType>
              <HTTP>
                <Get>
                  <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="http://maps.csr.ufmg.br:80/geoserver/wms?SERVICE=WMS&amp;"/>
                </Get>
              </HTTP>
            </DCPType>
          </GetMap>
          <GetFeatureInfo>
            <Format>text/plain</Format>
            <Format>application/vnd.ogc.gml</Format>
            <Format>application/vnd.ogc.gml/3.1.1</Format>
            <Format>text/html</Format>
            <Format>application/json</Format>
            <DCPType>
              <HTTP>
                <Get>
                  <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="http://maps.csr.ufmg.br:80/geoserver/wms?SERVICE=WMS&amp;"/>
                </Get>
                <Post>
                  <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="http://maps.csr.ufmg.br:80/geoserver/wms?SERVICE=WMS&amp;"/>
                </Post>
              </HTTP>
            </DCPType>
          </GetFeatureInfo>
          <DescribeLayer>
            <Format>application/vnd.ogc.wms_xml</Format>
            <DCPType>
              <HTTP>
                <Get>
                  <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="http://maps.csr.ufmg.br:80/geoserver/wms?SERVICE=WMS&amp;"/>
                </Get>
              </HTTP>
            </DCPType>
          </DescribeLayer>
          <GetLegendGraphic>
            <Format>image/png</Format>
            <DCPType>
              <HTTP>
                <Get>
                  <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="http://maps.csr.ufmg.br:80/geoserver/wms?SERVICE=WMS&amp;"/>
                </Get>
              </HTTP>
            </DCPType>
          </GetLegendGraphic>
          <GetStyles>
            <Format>application/vnd.ogc.sld+xml</Format>
            <DCPType>
              <HTTP>
                <Get>
                  <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="http://maps.csr.ufmg.br:80/geoserver/wms?SERVICE=WMS&amp;"/>
                </Get>
              </HTTP>
            </DCPType>
          </GetStyles>
        </Request>
        <Exception>
          <Format>application/vnd.ogc.se_xml</Format>
          <Format>application/vnd.ogc.se_inimage</Format>
        </Exception>
        <VendorSpecificCapabilities>
          <notempty></notempty>
        </VendorSpecificCapabilities>
        <UserDefinedSymbolization SupportSLD="1" UserLayer="1" UserStyle="1" RemoteWFS="1"/>
        <Layer queryable="0" opaque="0" noSubsets="0">
          <Title>MapServer via GItHub</Title>
          <Abstract>GitHub WMS</Abstract>
          <!--All supported EPSG projections:-->
          <SRS>EPSG:3857</SRS>
          <SRS>EPSG:4326</SRS>
          <SRS>EPSG:900913</SRS>
          <SRS>EPSG:42303</SRS>
          <LatLonBoundingBox minx="-180.00004074199998" miny="-90.0" maxx="180.0000000000001" maxy="90.0"/>
        </Layer>
      </Capability>
    </WMT_MS_Capabilities>'''

    # @staticmethod
    # def convertCoordinateProj(crsProj, fromX, fromY, outputProjected):
    #
    #     regex = r"^[ ]*PROJCS"
    #     isProjected = re.match(regex, crsProj)
    #
    #     if (isProjected and outputProjected) or ( not isProjected and  not outputProjected):
    #         return (fromX, fromY)
    #     else:
    #         fProj = QgsCoordinateReferenceSystem()
    #         fProj.createFromWkt(crsProj)
    #         tProj = QgsCoordinateReferenceSystem()
    #         tProj.createFromProj4("+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs" if outputProjected else "+proj=longlat +datum=WGS84 +no_defs ")
    #         newCoord = QgsCoordinateTransform(fProj, tProj, QgsProject.instance()).transform(QgsPointXY(fromX, fromY), True)
    #     return (newCoord.x, newCoord.y)

    @staticmethod
    def getMapKeyword(isShapefile, maxZoom, dlLink=None):
        if dlLink is None or len(dlLink) == 0:
            dlLink = 'disabledownload'
        elif ':' in dlLink:
            dlLink = dlLink[(dlLink.index(':') + 1):]
        elif '˸' in dlLink:
            dlLink = dlLink[(dlLink.index('˸') + 1):]
        return "group˸" + ('shp' if isShapefile else 'tif') + "˸˸˸" + dlLink + "˸notListing˸˸maxZoom˸" + str(maxZoom)

    @staticmethod
    def getMapDescription(layerNameID, layerAttr, latMinX, latMinY, latMaxX, latMaxY, projMinX, projMinY, projMaxX, projMaxY, maxZoom, isShapefile, dLink):
        layerAttr = UTILS.normalizeName(layerAttr)
        layerNameID = UTILS.normalizeName(layerNameID)
        # Inverti o minx/miny e maxX/maxY do epsg 4326 pq estava trocando no geoserver, mas n sei pq isso acontece.
        return """<CONTENT>
          <Layer queryable="1" opaque="0">
          <Name>GH:""" + layerNameID + """</Name>
          <Title>""" + layerNameID + """</Title>
          <Abstract>GH:""" + layerNameID + """ ABSTRACT</Abstract>
          <KeywordList>
            <Keyword>""" + WMSCapabilities.getMapKeyword(isShapefile, maxZoom, dLink) + """</Keyword>
          </KeywordList>
          <SRS>EPSG:4326</SRS>
          <LatLonBoundingBox minx=\"""" + str(latMinX) + """\" miny=\"""" + str(latMinY) + """\" maxx=\"""" + str(
            latMaxX) + """\" maxy=\"""" + str(latMaxY) + """\"/>
          <BoundingBox SRS="EPSG:4326" minx=\"""" + str(projMinX) + """\" miny=\"""" + str(
            projMinY) + """\" maxx=\"""" + str(projMaxX) + """\" maxy=\"""" + str(projMaxY) + """\"/>
          <Style>
           <Name>""" + layerAttr + """</Name>
           <Title>""" + layerAttr + """</Title>
           <Abstract/>
           <LegendURL width="20" height="20">
           <Format>image/png</Format>
           <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="https://maps.csr.ufmg.br:443/geoserver/wms?request=GetLegendGraphic&amp;format=image%2Fpng&amp;width=20&amp;height=20&amp;layer=""" + layerNameID + """\"/>
           </LegendURL>
          </Style>
        </Layer>
        </CONTENT>
        """

    @staticmethod
    def getTileSetDescription(fileNameId, latMinX, latMinY, latMaxX, latMaxY, projMinX, projMinY, projMaxX, projMaxY):
        # <BoundingBox SRS="EPSG:4326" minx=\"""" + str(latMinX) + """\" miny=\"""" + str(latMinY) + """\" maxx=\"""" + str(latMaxX) + """\" maxy=\"""" + str(latMaxY) + """\"/>
        return """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
        <CONTENT>
          <TileSet>
            <SRS>EPSG:4326</SRS>
            <BoundingBox SRS="EPSG:4326" minx="-180.0" miny="-90.0" maxx="0.0" maxy="90.0"/>
        <Resolutions>0.703125 0.3515625 0.17578125 0.087890625 0.0439453125 0.02197265625 0.010986328125 0.0054931640625 0.00274658203125 0.001373291015625 6.866455078125E-4 3.4332275390625E-4 1.71661376953125E-4 8.58306884765625E-5 4.291534423828125E-5 2.1457672119140625E-5 1.0728836059570312E-5 5.364418029785156E-6 2.682209014892578E-6 1.341104507446289E-6 6.705522537231445E-7 3.3527612686157227E-7 </Resolutions>
            <Width>256</Width>
            <Height>256</Height>
            <Format>image/png</Format>
            <Layers>GH:""" + fileNameId + """</Layers>
            <Styles/>
          </TileSet>
          <TileSet>
            <SRS>EPSG:900913</SRS>
            <BoundingBox SRS="EPSG:900913" minx="-2.003750834E7" miny="-2.003750834E7" maxx="2.003750834E7" maxy="2.003750834E7"/>
        <Resolutions>156543.03390625 78271.516953125 39135.7584765625 19567.87923828125 9783.939619140625 4891.9698095703125 2445.9849047851562 1222.9924523925781 611.4962261962891 305.74811309814453 152.87405654907226 76.43702827453613 38.218514137268066 19.109257068634033 9.554628534317017 4.777314267158508 2.388657133579254 1.194328566789627 0.5971642833948135 0.29858214169740677 0.14929107084870338 0.07464553542435169 0.037322767712175846 0.018661383856087923 0.009330691928043961 0.004665345964021981 0.0023326729820109904 0.0011663364910054952 5.831682455027476E-4 2.915841227513738E-4 1.457920613756869E-4 </Resolutions>
            <Width>256</Width>
            <Height>256</Height>
            <Format>image/png</Format>
            <Layers>GH:""" + fileNameId + """</Layers>
            <Styles/>
          </TileSet>
          </CONTENT>
        """
        # <BoundingBox SRS="EPSG:900913" minx=\"""" + str(projMinX) + """\" miny=\"""" + str(projMinY) + """\" maxx=\"""" + str(projMaxX) + """\" maxy=\"""" + str(projMaxY) + """\"/>

    @staticmethod
    def getAllLayers(content, layerAttr='1'):
        #FIXME should use the style name to identify the layer attributes
        doc = xmltodict.parse(content)
        allLayers = []
        try:
            layerDefinitions = doc['WMT_MS_Capabilities']['Capability']['Layer']['Layer']
            if layerDefinitions is not None and isinstance(layerDefinitions, list) and len(layerDefinitions):
                allLayers = [curLayer["Name"] for curLayer in layerDefinitions]
            elif layerDefinitions is not None and isinstance(doc['WMT_MS_Capabilities']['Capability']['Layer']['Layer'], collections.OrderedDict) and len(layerDefinitions):
                allLayers = [layerDefinitions["Name"]]
        except KeyError as e:
            pass
        return allLayers

    @staticmethod
    def getOperationsListForCustomLayer(docLayer):
        #FIXME Não deveria modificar o input numa funcao de get
        #FIXME codigo duplicado
        if not "Operation" in docLayer:
            docLayer["Operation"] = []
        elif isinstance(docLayer["Operation"], collections.OrderedDict):
            docLayer["Operation"] = [docLayer["Operation"]]

        if len(docLayer["Operation"]) == 0:
            return []
        elif isinstance(docLayer["Operation"], str):
            raise Exception(json.dumps(docLayer))
        else:
            return [{'type': operation["@type"], 'attribute': operation["#text"]} for operation in docLayer['Operation']]


    @staticmethod
    def getAllCustomLayers(content, layerAttr='1'):
        doc = xmltodict.parse(content)
        allCustomLayers = []
        if 'CustomLayer'  in doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']:
            layerDefinitions = doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']['CustomLayer']

            if layerDefinitions is not None and isinstance(layerDefinitions, collections.OrderedDict):
                layerDefinitions = [layerDefinitions]
            if layerDefinitions is not None and isinstance(layerDefinitions, list) and len(layerDefinitions) > 0:
                for curLayer in layerDefinitions:
                    for operation in WMSCapabilities.getOperationsListForCustomLayer(curLayer):
                        allCustomLayers.append(curLayer["Name"] + ";" + operation['attribute'])
                        #allCustomLayers.append(curLayer["Name"] + ":" + operation['attribute'] + ":" + operation['type'])
        return allCustomLayers

    @staticmethod
    def getCurrentCapabilitiesDoc(directory):
        capabilitiesPath = os.path.join(directory, "getCapabilities.xml")
        if os.path.isfile(capabilitiesPath):
            with io.open(capabilitiesPath, mode="r", encoding="utf-8") as capabilitiesFile:
                capabilitiesContent = capabilitiesFile.read()
        else:
            capabilitiesContent = WMSCapabilities.getDefaultCapabilities()
        doc = xmltodict.parse(capabilitiesContent)
        return doc

    @staticmethod
    def saveCurrentCapabilities(directory, doc):
        capabilitiesPath = os.path.join(directory, "getCapabilities.xml")
        with io.open(capabilitiesPath, mode="w", encoding="utf-8") as capabilitiesFile:
            capabilitiesFile.write(xmltodict.unparse(doc, pretty=True))

    @staticmethod
    def getCustomLayerDefaultDefinition(layerName):
        layerName = UTILS.normalizeName(layerName)
        return xmltodict.parse("""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
            <CONTENT>
                <Name>GH:""" + layerName + """</Name>
                <Title>"""+layerName +"""</Title>
            </CONTENT>""")["CONTENT"]

    #customDoc é um Dict vindo do xmltodict. layerAttr e operation são strings
    @staticmethod
    def addOperation(customDoc, layerAttr, operation):
        layerAttr = UTILS.normalizeName(layerAttr)
        if not "Operation" in customDoc:
            customDoc["Operation"] = list()
        if isinstance(customDoc["Operation"], collections.OrderedDict):
            customDoc["Operation"] = [customDoc["Operation"]]

        found = False
        for curOperationDict in customDoc["Operation"]:
            if not found and '@type' in curOperationDict and curOperationDict['@type'] == operation and curOperationDict['#text'] == layerAttr:
                found = True
        if not found:
            customDoc['Operation'].append(xmltodict.parse("""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
                            <CONTENT>
                            <Operation type=\"""" + operation + """\">""" + layerAttr + """</Operation>
                            </CONTENT>""")["CONTENT"]["Operation"])
        return customDoc


    @staticmethod
    def updateCustomXML(directory, layerTitle, layerAttr, operation):
        doc = WMSCapabilities.getCurrentCapabilitiesDoc(directory)
        filename = UTILS.normalizeName(layerTitle)  # layer Name no qgis

        if 'CustomLayer' in doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']:
            if type(doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']["CustomLayer"]) is collections.OrderedDict:
                curLayer = doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']["CustomLayer"]
                doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']["CustomLayer"] = [curLayer]
        else:
            doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']['CustomLayer'] = []

        curLayerDefinition = None
        if 'CustomLayer' in doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']:
            for iLayer in range(len(doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']["CustomLayer"]) - 1, -1, -1):
                curLayer = doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']["CustomLayer"][iLayer]
                if "Name" in curLayer and filename in curLayer["Name"]:
                    doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']["CustomLayer"].pop(iLayer)
                    curLayerDefinition = curLayer
                    #TODO verificar se não restaram outros com mesmo nome.
        if curLayerDefinition is None:
            curLayerDefinition = WMSCapabilities.getCustomLayerDefaultDefinition(filename)
        WMSCapabilities.addOperation(curLayerDefinition, layerAttr, operation)
        doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']["CustomLayer"].append(curLayerDefinition)
        WMSCapabilities.saveCurrentCapabilities(directory, doc)

    @staticmethod
    def setCapabilitiesDefaultMaxZoom(directory):
        doc = WMSCapabilities.getCurrentCapabilitiesDoc(directory)

        if 'Layer' in doc['WMT_MS_Capabilities']['Capability']['Layer']:
            if type(doc['WMT_MS_Capabilities']['Capability']['Layer']['Layer']) is collections.OrderedDict:
                curLayer = doc['WMT_MS_Capabilities']['Capability']['Layer']['Layer']
                doc['WMT_MS_Capabilities']['Capability']['Layer']['Layer'] = [curLayer]

        if 'Layer' in doc['WMT_MS_Capabilities']['Capability']['Layer']:
            for iLayer in range(len(doc['WMT_MS_Capabilities']['Capability']['Layer']['Layer']) - 1, -1, -1):
                curLayer = doc['WMT_MS_Capabilities']['Capability']['Layer']['Layer'][iLayer]
                if "KeywordList" in curLayer and type(curLayer['KeywordList']) is collections.OrderedDict and ("Keyword" in curLayer['KeywordList']) and curLayer['KeywordList']['Keyword'] == 'GITHUB':
                    curLayer['KeywordList']['Keyword'] = WMSCapabilities.getMapKeyword(False, 8)
        WMSCapabilities.saveCurrentCapabilities(directory, doc)

    @staticmethod
    def updateXML(directory, layerExtents, layerMercatorExtents, isShapefile, layerTitle, layerAttr, maxZoom, downloadLink):
        doc = WMSCapabilities.getCurrentCapabilitiesDoc(directory)

        filename = UTILS.normalizeName(layerTitle) #layer Name no qgis

        assert isinstance(layerExtents, WMSBBox) and isinstance(layerMercatorExtents, WMSBBox)

        # #extents, projection
        # projMaxX = layer.extent().xMaximum()
        projMaxX = layerExtents.xMaximum()
        # projMinX = layer.extent().xMinimum()
        projMinX = layerExtents.xMinimum()
        # projMaxY = layer.extent().yMaximum()
        projMaxY = layerExtents.yMaximum()
        # projMinY = layer.extent().yMinimum()
        projMinY = layerExtents.yMinimum()
        # llExtent = UTILS.getMapExtent(layer, QgsCoordinateReferenceSystem('EPSG:4326'))
        # latMaxX = llExtent.xMaximum()
        latMaxX = layerMercatorExtents.xMaximum()
        # latMinX = llExtent.xMinimum()
        latMinX = layerMercatorExtents.xMinimum()
        # latMaxY = llExtent.yMaximum()
        latMaxY = layerMercatorExtents.yMaximum()
        # latMinY = llExtent.yMinimum()
        latMinY = layerMercatorExtents.yMinimum()
        #isShapefile = (isinstance(layer, QgsVectorLayer))


        if 'Layer' in doc['WMT_MS_Capabilities']['Capability']['Layer']:
            if type(doc['WMT_MS_Capabilities']['Capability']['Layer']['Layer']) is collections.OrderedDict:
                curLayer = doc['WMT_MS_Capabilities']['Capability']['Layer']['Layer']
                doc['WMT_MS_Capabilities']['Capability']['Layer']['Layer'] = [curLayer]

        if 'Layer' in doc['WMT_MS_Capabilities']['Capability']['Layer']:
            for iLayer in range(len(doc['WMT_MS_Capabilities']['Capability']['Layer']['Layer']) - 1, -1, -1):
                curLayer = doc['WMT_MS_Capabilities']['Capability']['Layer']['Layer'][iLayer]
                if "Name" in curLayer and curLayer["Name"] == "GH:" + filename:
                    doc['WMT_MS_Capabilities']['Capability']['Layer']['Layer'].pop(iLayer)

        #FIXME One attribute only. (Is always overwriting)
        newLayerDescription = xmltodict.parse(
            WMSCapabilities.getMapDescription(filename, layerAttr, latMinX, latMinY, latMaxX, latMaxY,
                                              projMinX, projMinY, projMaxX, projMaxY, maxZoom, isShapefile, downloadLink))['CONTENT']
        if 'Layer' in doc['WMT_MS_Capabilities']['Capability']['Layer']:
            doc['WMT_MS_Capabilities']['Capability']['Layer']['Layer'].append(newLayerDescription['Layer'])
        else:
            doc['WMT_MS_Capabilities']['Capability']['Layer'] = newLayerDescription

        newTileSetDescription = xmltodict.parse(
            WMSCapabilities.getTileSetDescription(filename, latMinX, latMinY, latMaxX, latMaxY, projMinX, projMinY,
                                                  projMaxX, projMaxY))['CONTENT']

        if doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities'] is not None and 'TileSet' in \
                doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']:
            if type(doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities'][
                        'TileSet']) is collections.OrderedDict:
                curTileSet = doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']['TileSet']
                doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']['TileSet'] = [
                    curTileSet]  # Transforms into a list

        if doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities'] is not None and 'TileSet' in \
                doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']:
            for iTileSet in range(
                    len(doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']['TileSet']) - 1,
                    -1, -1):
                curTileSet = doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']['TileSet'][iTileSet]
                if "Layers" in curTileSet and curTileSet["Layers"] == "GH:" + filename:
                    doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']['TileSet'].pop(iTileSet)
            doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']['TileSet'] += newTileSetDescription[
                'TileSet']  # Dois elementos c mesma chave representa com lista
        else:
            doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities'] = newTileSetDescription
        WMSCapabilities.saveCurrentCapabilities(directory, doc)

    @staticmethod
    def write_description(directory, layerTitle, layerAttr, cellTypeName, nullValue, operation):
        layerTitle = UTILS.normalizeName(layerTitle)
        cellTypeName = UTILS.normalizeName(cellTypeName)
        filecsv = "description.csv"
        csvPath = os.path.join(directory, filecsv)
        jsonPath = os.path.join(directory, "description.json")
        if os.path.isfile(csvPath):
            csvFile = open(csvPath, "r", encoding="utf-8")
        else:
            csvFile = io.StringIO("Key*, cell, null, operation, attr,\n-9999, \"\", -1, \"\", nenhuma, ")

        csv_reader = csv.DictReader(csvFile, delimiter=',')
        line_count = 0
        elements = [cellTypeName, str(nullValue), operation, layerAttr]
        for row in csv_reader:
            curEntry = {
                'cellType': row[' cell'].strip(),
                'nullValue': row[' null'].strip(),
                'operation': row[' operation'].strip(),
                'attribute': row[' attr'].strip()
            }
            if line_count > 0 and curEntry['operation'] != operation and curEntry['attribute'] != layerAttr:
                # Key *, cell, null, operation, attr,
                elements.append(curEntry['cellType'])
                elements.append(curEntry['nullValue'])
                elements.append(curEntry['operation'])
                elements.append(curEntry['attribute'])
            line_count += 1
        with open(jsonPath, "w", encoding="utf-8") as jsonFile:
            jsonFile.write(json.dumps(elements))
        csvFile.close()

class WMSBBox():
    xMax = None
    def xMaximum(self):
        return self.xMax

    xMin = None
    def xMinimum(self):
        return self.xMin

    yMax = None
    def yMaximum(self):
        return self.yMax

    yMin = None
    def yMinimum(self):
        return self.yMin

    def __init__(self, xMax, xMin, yMax, yMin):
        self.xMax = xMax
        self.xMin = xMin
        self.yMax = yMax
        self.yMin = yMin



try:
    from GDAL_UTILS import GDAL_UTILS
except:
    pass #Not in Dinamica Code

from osgeo import gdal,ogr,osr

#Thanks to https://gis.stackexchange.com/questions/57834/how-to-get-raster-corner-coordinates-using-python-gdal-bindings
class GDAL_UTILS:

    #Danilo vai 4 pontos [Left Bottom,  Left Top, Right Bottom, Right Top]
    @staticmethod
    def _getExtent(gt,cols,rows):
        ''' Return list of corner coordinates from a geotransform

            @type gt:   C{tuple/list}
            @param gt: geotransform
            @type cols:   C{int}
            @param cols: number of columns in the dataset
            @type rows:   C{int}
            @param rows: number of rows in the dataset
            @rtype:    C{[float,...,float]}
            @return:   coordinates of each corner
        '''
        ext=[]
        xarr=[0,cols]
        yarr=[0,rows]

        for px in xarr:
            for py in yarr:
                x=gt[0]+(px*gt[1])+(py*gt[2])
                y=gt[3]+(px*gt[4])+(py*gt[5])
                ext.append([x,y])
                print(x,y)
            yarr.reverse()
        return ext

    @staticmethod
    def _reprojectCoords(coords,src_srs,tgt_srs):
        ''' Reproject a list of x,y coordinates.

            @type geom:     C{tuple/list}
            @param geom:    List of [[x,y],...[x,y]] coordinates
            @type src_srs:  C{osr.SpatialReference}
            @param src_srs: OSR SpatialReference object
            @type tgt_srs:  C{osr.SpatialReference}
            @param tgt_srs: OSR SpatialReference object
            @rtype:         C{tuple/list}
            @return:        List of transformed [[x,y],...[x,y]] coordinates
        '''
        trans_coords=[]
        transform = osr.CoordinateTransformation( src_srs, tgt_srs)
        for x,y in coords:
            x,y,z = transform.TransformPoint(x,y)
            trans_coords.append([x,y])
        return trans_coords

    #danilo se o epsgCode é None retorna o do próprio mapa sem alterar.
    @staticmethod
    def getExtent(rasterPath, epsgCode=None):
        ds = gdal.Open(rasterPath, gdal.GA_ReadOnly)
        try:
            gt = ds.GetGeoTransform()
            cols = ds.RasterXSize
            rows = ds.RasterYSize
            ext = GDAL_UTILS._getExtent(gt, cols, rows)
            if epsgCode is None:
                return GDAL_UTILS.getArrayFromExt(ext)
            else:
                src_srs=osr.SpatialReference()
                src_srs.ImportFromWkt(ds.GetProjection())
                tgt_srs = osr.SpatialReference()
                tgt_srs.ImportFromEPSG(epsgCode)
                return GDAL_UTILS.getArrayFromExt(GDAL_UTILS._reprojectCoords(ext,src_srs,tgt_srs))
        finally:
            ds = None

    #Retorna xMax, xMin, yMax, yMin do extents.
    @staticmethod
    def getArrayFromExt(ext):
        maxPoint = ext[3]
        minPoint = ext[1]
        return (maxPoint[0], minPoint[0], maxPoint[1], minPoint[1])

    # @staticmethod
    # #Pega as informacoes de celula direto do raster, usando o GDAL.
    # def getRasterCellInfo(mapDataPath):
    #     # cellInfo = dict()
    #     # # if Utils.isRasterFile(self.__mapDataPath) :
    #     # hDataset = gdal.Open(mapDataPath, gdal.GA_ReadOnly)
    #     # try:
    #     #     if hDataset is not None and hDataset.RasterCount > 0 :
    #     #         curBand = hDataset.GetRasterBand(1)
    #     #         unicode(gdal.GetDataTypeName(curBand.DataType))
    #     #         cellInfo[u"Null Cell Value"] = unicode(curBand.GetNoDataValue())
    #     #         cellInfo[u"Number of Lines"] = unicode(hDataset.RasterYSize)
    #     #         cellInfo[u"Number of Columns"] = unicode(hDataset.RasterXSize)
    #     #         adfGeoTransform = hDataset.GetGeoTransform(can_return_null = True)
    #     #         if adfGeoTransform is not None :
    #     #             cellInfo[u"Cell Width"] = unicode(adfGeoTransform[1])
    #     #             cellInfo[u"Cell Height"] = unicode(fabs(adfGeoTransform[5]))
    #     #         cellInfo[u"Number of Layers"] = unicode(hDataset.RasterCount)
    #     # finally:
    #     #     hDataset = None
    #     # return cellInfo
    #     return ""

    @staticmethod
    def getCellType(rasterPath):
        unicode(gdal.GetDataTypeName(curBand.DataType))





try:
    from WMSCapabilities import WMSCapabilities
except:
    pass

#!/usr/bin/env python
# -*- coding: utf-8 -*-


isDinamica = False
try:
    dinamica.package("os")
    isDinamica = True
except:
    isDinamica = False

if not isDinamica:
    try:
        from .UTILS import UTILS
        from . import xmltodict
    except:
        pass #Not in QGIS

    try:
        from UTILS import UTILS
        from xmltodict import xmltodict
    except:
        pass #Not in Dinamica Code

from collections import OrderedDict
import collections
from pathlib import Path
import json
import os
import io
import csv
import re

# try:
#     from qgis.core import (QgsCoordinateReferenceSystem, QgsProject, QgsPointXY, QgsCoordinateTransform, QgsVectorLayer)
# except:
#     pass

class WMSCapabilities:

    @staticmethod
    def getDefaultCapabilities():
        return '''<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE WMT_MS_Capabilities SYSTEM "http://maps.csr.ufmg.br:80/geoserver/schemas/wms/1.1.1/WMS_MS_Capabilities.dtd"[
    <!ELEMENT VendorSpecificCapabilities (TileSet*) >
    <!ELEMENT TileSet (SRS, BoundingBox?, Resolutions, Width, Height, Format, Layers*, Styles*) >
    <!ELEMENT Resolutions (#PCDATA) >
    <!ELEMENT Width (#PCDATA) >
    <!ELEMENT Height (#PCDATA) >
    <!ELEMENT Layers (#PCDATA) >
    <!ELEMENT Styles (#PCDATA) >
    ]>
    <WMT_MS_Capabilities version="1.1.1" updateSequence="63258">
      <Service>
        <Name>OGC:WMS</Name>
        <Title>CSR Web Map Service</Title>
        <Abstract>Compliant WMS Response</Abstract>
        <KeywordList>
          <Keyword>WFS</Keyword>
          <Keyword>WMS</Keyword>
          <Keyword>GEOSERVER</Keyword>
        </KeywordList>
        <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="http://geoserver.sourceforge.net/html/index.php"/>
        <ContactInformation>
          <ContactPersonPrimary>
            <ContactPerson>GITHUB owner</ContactPerson>
            <ContactOrganization>GITHUB owner</ContactOrganization>
          </ContactPersonPrimary>
          <ContactPosition>Chief geographer</ContactPosition>
          <ContactAddress>
            <AddressType>Work</AddressType>
            <Address/>
            <City>Alexandria</City>
            <StateOrProvince/>
            <PostCode/>
            <Country>Egypt</Country>
          </ContactAddress>
          <ContactVoiceTelephone/>
          <ContactFacsimileTelephone/>
          <ContactElectronicMailAddress>claudius.ptolomaeus@gmail.com</ContactElectronicMailAddress>
        </ContactInformation>
        <Fees>NONE</Fees>
        <AccessConstraints>NONE</AccessConstraints>
      </Service>
      <Capability>
        <Request>
          <GetCapabilities>
            <Format>application/vnd.ogc.wms_xml</Format>
            <DCPType>
              <HTTP>
                <Get>
                  <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="http://maps.csr.ufmg.br:80/geoserver/wms?SERVICE=WMS&amp;"/>
                </Get>
                <Post>
                  <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="http://maps.csr.ufmg.br:80/geoserver/wms?SERVICE=WMS&amp;"/>
                </Post>
              </HTTP>
            </DCPType>
          </GetCapabilities>
          <GetMap>
            <Format>image/png</Format>
            <DCPType>
              <HTTP>
                <Get>
                  <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="http://maps.csr.ufmg.br:80/geoserver/wms?SERVICE=WMS&amp;"/>
                </Get>
              </HTTP>
            </DCPType>
          </GetMap>
          <GetFeatureInfo>
            <Format>text/plain</Format>
            <Format>application/vnd.ogc.gml</Format>
            <Format>application/vnd.ogc.gml/3.1.1</Format>
            <Format>text/html</Format>
            <Format>application/json</Format>
            <DCPType>
              <HTTP>
                <Get>
                  <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="http://maps.csr.ufmg.br:80/geoserver/wms?SERVICE=WMS&amp;"/>
                </Get>
                <Post>
                  <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="http://maps.csr.ufmg.br:80/geoserver/wms?SERVICE=WMS&amp;"/>
                </Post>
              </HTTP>
            </DCPType>
          </GetFeatureInfo>
          <DescribeLayer>
            <Format>application/vnd.ogc.wms_xml</Format>
            <DCPType>
              <HTTP>
                <Get>
                  <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="http://maps.csr.ufmg.br:80/geoserver/wms?SERVICE=WMS&amp;"/>
                </Get>
              </HTTP>
            </DCPType>
          </DescribeLayer>
          <GetLegendGraphic>
            <Format>image/png</Format>
            <DCPType>
              <HTTP>
                <Get>
                  <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="http://maps.csr.ufmg.br:80/geoserver/wms?SERVICE=WMS&amp;"/>
                </Get>
              </HTTP>
            </DCPType>
          </GetLegendGraphic>
          <GetStyles>
            <Format>application/vnd.ogc.sld+xml</Format>
            <DCPType>
              <HTTP>
                <Get>
                  <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="http://maps.csr.ufmg.br:80/geoserver/wms?SERVICE=WMS&amp;"/>
                </Get>
              </HTTP>
            </DCPType>
          </GetStyles>
        </Request>
        <Exception>
          <Format>application/vnd.ogc.se_xml</Format>
          <Format>application/vnd.ogc.se_inimage</Format>
        </Exception>
        <VendorSpecificCapabilities>
          <notempty></notempty>
        </VendorSpecificCapabilities>
        <UserDefinedSymbolization SupportSLD="1" UserLayer="1" UserStyle="1" RemoteWFS="1"/>
        <Layer queryable="0" opaque="0" noSubsets="0">
          <Title>MapServer via GItHub</Title>
          <Abstract>GitHub WMS</Abstract>
          <!--All supported EPSG projections:-->
          <SRS>EPSG:3857</SRS>
          <SRS>EPSG:4326</SRS>
          <SRS>EPSG:900913</SRS>
          <SRS>EPSG:42303</SRS>
          <LatLonBoundingBox minx="-180.00004074199998" miny="-90.0" maxx="180.0000000000001" maxy="90.0"/>
        </Layer>
      </Capability>
    </WMT_MS_Capabilities>'''

    # @staticmethod
    # def convertCoordinateProj(crsProj, fromX, fromY, outputProjected):
    #
    #     regex = r"^[ ]*PROJCS"
    #     isProjected = re.match(regex, crsProj)
    #
    #     if (isProjected and outputProjected) or ( not isProjected and  not outputProjected):
    #         return (fromX, fromY)
    #     else:
    #         fProj = QgsCoordinateReferenceSystem()
    #         fProj.createFromWkt(crsProj)
    #         tProj = QgsCoordinateReferenceSystem()
    #         tProj.createFromProj4("+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs" if outputProjected else "+proj=longlat +datum=WGS84 +no_defs ")
    #         newCoord = QgsCoordinateTransform(fProj, tProj, QgsProject.instance()).transform(QgsPointXY(fromX, fromY), True)
    #     return (newCoord.x, newCoord.y)

    @staticmethod
    def getMapKeyword(isShapefile, maxZoom, dlLink=None):
        if dlLink is None or len(dlLink) == 0:
            dlLink = 'disabledownload'
        elif ':' in dlLink:
            dlLink = dlLink[(dlLink.index(':') + 1):]
        elif '˸' in dlLink:
            dlLink = dlLink[(dlLink.index('˸') + 1):]
        return "group˸" + ('shp' if isShapefile else 'tif') + "˸˸˸" + dlLink + "˸notListing˸˸maxZoom˸" + str(maxZoom)

    @staticmethod
    def getMapDescription(layerNameID, layerAttr, latMinX, latMinY, latMaxX, latMaxY, projMinX, projMinY, projMaxX, projMaxY, maxZoom, isShapefile, dLink):
        layerAttr = UTILS.normalizeName(layerAttr)
        layerNameID = UTILS.normalizeName(layerNameID)
        # Inverti o minx/miny e maxX/maxY do epsg 4326 pq estava trocando no geoserver, mas n sei pq isso acontece.
        return """<CONTENT>
          <Layer queryable="1" opaque="0">
          <Name>GH:""" + layerNameID + """</Name>
          <Title>""" + layerNameID + """</Title>
          <Abstract>GH:""" + layerNameID + """ ABSTRACT</Abstract>
          <KeywordList>
            <Keyword>""" + WMSCapabilities.getMapKeyword(isShapefile, maxZoom, dLink) + """</Keyword>
          </KeywordList>
          <SRS>EPSG:4326</SRS>
          <LatLonBoundingBox minx=\"""" + str(latMinX) + """\" miny=\"""" + str(latMinY) + """\" maxx=\"""" + str(
            latMaxX) + """\" maxy=\"""" + str(latMaxY) + """\"/>
          <BoundingBox SRS="EPSG:4326" minx=\"""" + str(projMinX) + """\" miny=\"""" + str(
            projMinY) + """\" maxx=\"""" + str(projMaxX) + """\" maxy=\"""" + str(projMaxY) + """\"/>
          <Style>
           <Name>""" + layerAttr + """</Name>
           <Title>""" + layerAttr + """</Title>
           <Abstract/>
           <LegendURL width="20" height="20">
           <Format>image/png</Format>
           <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="https://maps.csr.ufmg.br:443/geoserver/wms?request=GetLegendGraphic&amp;format=image%2Fpng&amp;width=20&amp;height=20&amp;layer=""" + layerNameID + """\"/>
           </LegendURL>
          </Style>
        </Layer>
        </CONTENT>
        """

    @staticmethod
    def getTileSetDescription(fileNameId, latMinX, latMinY, latMaxX, latMaxY, projMinX, projMinY, projMaxX, projMaxY):
        # <BoundingBox SRS="EPSG:4326" minx=\"""" + str(latMinX) + """\" miny=\"""" + str(latMinY) + """\" maxx=\"""" + str(latMaxX) + """\" maxy=\"""" + str(latMaxY) + """\"/>
        return """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
        <CONTENT>
          <TileSet>
            <SRS>EPSG:4326</SRS>
            <BoundingBox SRS="EPSG:4326" minx="-180.0" miny="-90.0" maxx="0.0" maxy="90.0"/>
        <Resolutions>0.703125 0.3515625 0.17578125 0.087890625 0.0439453125 0.02197265625 0.010986328125 0.0054931640625 0.00274658203125 0.001373291015625 6.866455078125E-4 3.4332275390625E-4 1.71661376953125E-4 8.58306884765625E-5 4.291534423828125E-5 2.1457672119140625E-5 1.0728836059570312E-5 5.364418029785156E-6 2.682209014892578E-6 1.341104507446289E-6 6.705522537231445E-7 3.3527612686157227E-7 </Resolutions>
            <Width>256</Width>
            <Height>256</Height>
            <Format>image/png</Format>
            <Layers>GH:""" + fileNameId + """</Layers>
            <Styles/>
          </TileSet>
          <TileSet>
            <SRS>EPSG:900913</SRS>
            <BoundingBox SRS="EPSG:900913" minx="-2.003750834E7" miny="-2.003750834E7" maxx="2.003750834E7" maxy="2.003750834E7"/>
        <Resolutions>156543.03390625 78271.516953125 39135.7584765625 19567.87923828125 9783.939619140625 4891.9698095703125 2445.9849047851562 1222.9924523925781 611.4962261962891 305.74811309814453 152.87405654907226 76.43702827453613 38.218514137268066 19.109257068634033 9.554628534317017 4.777314267158508 2.388657133579254 1.194328566789627 0.5971642833948135 0.29858214169740677 0.14929107084870338 0.07464553542435169 0.037322767712175846 0.018661383856087923 0.009330691928043961 0.004665345964021981 0.0023326729820109904 0.0011663364910054952 5.831682455027476E-4 2.915841227513738E-4 1.457920613756869E-4 </Resolutions>
            <Width>256</Width>
            <Height>256</Height>
            <Format>image/png</Format>
            <Layers>GH:""" + fileNameId + """</Layers>
            <Styles/>
          </TileSet>
          </CONTENT>
        """
        # <BoundingBox SRS="EPSG:900913" minx=\"""" + str(projMinX) + """\" miny=\"""" + str(projMinY) + """\" maxx=\"""" + str(projMaxX) + """\" maxy=\"""" + str(projMaxY) + """\"/>

    @staticmethod
    def getAllLayers(content, layerAttr='1'):
        #FIXME should use the style name to identify the layer attributes
        doc = xmltodict.parse(content)
        allLayers = []
        try:
            layerDefinitions = doc['WMT_MS_Capabilities']['Capability']['Layer']['Layer']
            if layerDefinitions is not None and isinstance(layerDefinitions, list) and len(layerDefinitions):
                allLayers = [curLayer["Name"] for curLayer in layerDefinitions]
            elif layerDefinitions is not None and isinstance(doc['WMT_MS_Capabilities']['Capability']['Layer']['Layer'], collections.OrderedDict) and len(layerDefinitions):
                allLayers = [layerDefinitions["Name"]]
        except KeyError as e:
            pass
        return allLayers

    @staticmethod
    def getOperationsListForCustomLayer(docLayer):
        #FIXME Não deveria modificar o input numa funcao de get
        #FIXME codigo duplicado
        if not "Operation" in docLayer:
            docLayer["Operation"] = []
        elif isinstance(docLayer["Operation"], collections.OrderedDict):
            docLayer["Operation"] = [docLayer["Operation"]]

        if len(docLayer["Operation"]) == 0:
            return []
        elif isinstance(docLayer["Operation"], str):
            raise Exception(json.dumps(docLayer))
        else:
            return [{'type': operation["@type"], 'attribute': operation["#text"]} for operation in docLayer['Operation']]


    @staticmethod
    def getAllCustomLayers(content, layerAttr='1'):
        doc = xmltodict.parse(content)
        allCustomLayers = []
        if 'CustomLayer'  in doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']:
            layerDefinitions = doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']['CustomLayer']

            if layerDefinitions is not None and isinstance(layerDefinitions, collections.OrderedDict):
                layerDefinitions = [layerDefinitions]
            if layerDefinitions is not None and isinstance(layerDefinitions, list) and len(layerDefinitions) > 0:
                for curLayer in layerDefinitions:
                    for operation in WMSCapabilities.getOperationsListForCustomLayer(curLayer):
                        allCustomLayers.append(curLayer["Name"] + ";" + operation['attribute'])
                        #allCustomLayers.append(curLayer["Name"] + ":" + operation['attribute'] + ":" + operation['type'])
        return allCustomLayers

    @staticmethod
    def getCurrentCapabilitiesDoc(directory):
        capabilitiesPath = os.path.join(directory, "getCapabilities.xml")
        if os.path.isfile(capabilitiesPath):
            with io.open(capabilitiesPath, mode="r", encoding="utf-8") as capabilitiesFile:
                capabilitiesContent = capabilitiesFile.read()
        else:
            capabilitiesContent = WMSCapabilities.getDefaultCapabilities()
        doc = xmltodict.parse(capabilitiesContent)
        return doc

    @staticmethod
    def saveCurrentCapabilities(directory, doc):
        capabilitiesPath = os.path.join(directory, "getCapabilities.xml")
        with io.open(capabilitiesPath, mode="w", encoding="utf-8") as capabilitiesFile:
            capabilitiesFile.write(xmltodict.unparse(doc, pretty=True))

    @staticmethod
    def getCustomLayerDefaultDefinition(layerName):
        layerName = UTILS.normalizeName(layerName)
        return xmltodict.parse("""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
            <CONTENT>
                <Name>GH:""" + layerName + """</Name>
                <Title>"""+layerName +"""</Title>
            </CONTENT>""")["CONTENT"]

    #customDoc é um Dict vindo do xmltodict. layerAttr e operation são strings
    @staticmethod
    def addOperation(customDoc, layerAttr, operation):
        layerAttr = UTILS.normalizeName(layerAttr)
        if not "Operation" in customDoc:
            customDoc["Operation"] = list()
        if isinstance(customDoc["Operation"], collections.OrderedDict):
            customDoc["Operation"] = [customDoc["Operation"]]

        found = False
        for curOperationDict in customDoc["Operation"]:
            if not found and '@type' in curOperationDict and curOperationDict['@type'] == operation and curOperationDict['#text'] == layerAttr:
                found = True
        if not found:
            customDoc['Operation'].append(xmltodict.parse("""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
                            <CONTENT>
                            <Operation type=\"""" + operation + """\">""" + layerAttr + """</Operation>
                            </CONTENT>""")["CONTENT"]["Operation"])
        return customDoc


    @staticmethod
    def updateCustomXML(directory, layerTitle, layerAttr, operation):
        doc = WMSCapabilities.getCurrentCapabilitiesDoc(directory)
        filename = UTILS.normalizeName(layerTitle)  # layer Name no qgis

        if 'CustomLayer' in doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']:
            if type(doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']["CustomLayer"]) is collections.OrderedDict:
                curLayer = doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']["CustomLayer"]
                doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']["CustomLayer"] = [curLayer]
        else:
            doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']['CustomLayer'] = []

        curLayerDefinition = None
        if 'CustomLayer' in doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']:
            for iLayer in range(len(doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']["CustomLayer"]) - 1, -1, -1):
                curLayer = doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']["CustomLayer"][iLayer]
                if "Name" in curLayer and filename in curLayer["Name"]:
                    doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']["CustomLayer"].pop(iLayer)
                    curLayerDefinition = curLayer
                    #TODO verificar se não restaram outros com mesmo nome.
        if curLayerDefinition is None:
            curLayerDefinition = WMSCapabilities.getCustomLayerDefaultDefinition(filename)
        WMSCapabilities.addOperation(curLayerDefinition, layerAttr, operation)
        doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']["CustomLayer"].append(curLayerDefinition)
        WMSCapabilities.saveCurrentCapabilities(directory, doc)

    @staticmethod
    def setCapabilitiesDefaultMaxZoom(directory):
        doc = WMSCapabilities.getCurrentCapabilitiesDoc(directory)

        if 'Layer' in doc['WMT_MS_Capabilities']['Capability']['Layer']:
            if type(doc['WMT_MS_Capabilities']['Capability']['Layer']['Layer']) is collections.OrderedDict:
                curLayer = doc['WMT_MS_Capabilities']['Capability']['Layer']['Layer']
                doc['WMT_MS_Capabilities']['Capability']['Layer']['Layer'] = [curLayer]

        if 'Layer' in doc['WMT_MS_Capabilities']['Capability']['Layer']:
            for iLayer in range(len(doc['WMT_MS_Capabilities']['Capability']['Layer']['Layer']) - 1, -1, -1):
                curLayer = doc['WMT_MS_Capabilities']['Capability']['Layer']['Layer'][iLayer]
                if "KeywordList" in curLayer and type(curLayer['KeywordList']) is collections.OrderedDict and ("Keyword" in curLayer['KeywordList']) and curLayer['KeywordList']['Keyword'] == 'GITHUB':
                    curLayer['KeywordList']['Keyword'] = WMSCapabilities.getMapKeyword(False, 8)
        WMSCapabilities.saveCurrentCapabilities(directory, doc)

    @staticmethod
    def updateXML(directory, layerExtents, layerMercatorExtents, isShapefile, layerTitle, layerAttr, maxZoom, downloadLink):
        doc = WMSCapabilities.getCurrentCapabilitiesDoc(directory)

        filename = UTILS.normalizeName(layerTitle) #layer Name no qgis

        assert isinstance(layerExtents, WMSBBox) and isinstance(layerMercatorExtents, WMSBBox)

        # #extents, projection
        # projMaxX = layer.extent().xMaximum()
        projMaxX = layerExtents.xMaximum()
        # projMinX = layer.extent().xMinimum()
        projMinX = layerExtents.xMinimum()
        # projMaxY = layer.extent().yMaximum()
        projMaxY = layerExtents.yMaximum()
        # projMinY = layer.extent().yMinimum()
        projMinY = layerExtents.yMinimum()
        # llExtent = UTILS.getMapExtent(layer, QgsCoordinateReferenceSystem('EPSG:4326'))
        # latMaxX = llExtent.xMaximum()
        latMaxX = layerMercatorExtents.xMaximum()
        # latMinX = llExtent.xMinimum()
        latMinX = layerMercatorExtents.xMinimum()
        # latMaxY = llExtent.yMaximum()
        latMaxY = layerMercatorExtents.yMaximum()
        # latMinY = llExtent.yMinimum()
        latMinY = layerMercatorExtents.yMinimum()
        #isShapefile = (isinstance(layer, QgsVectorLayer))


        if 'Layer' in doc['WMT_MS_Capabilities']['Capability']['Layer']:
            if type(doc['WMT_MS_Capabilities']['Capability']['Layer']['Layer']) is collections.OrderedDict:
                curLayer = doc['WMT_MS_Capabilities']['Capability']['Layer']['Layer']
                doc['WMT_MS_Capabilities']['Capability']['Layer']['Layer'] = [curLayer]

        if 'Layer' in doc['WMT_MS_Capabilities']['Capability']['Layer']:
            for iLayer in range(len(doc['WMT_MS_Capabilities']['Capability']['Layer']['Layer']) - 1, -1, -1):
                curLayer = doc['WMT_MS_Capabilities']['Capability']['Layer']['Layer'][iLayer]
                if "Name" in curLayer and curLayer["Name"] == "GH:" + filename:
                    doc['WMT_MS_Capabilities']['Capability']['Layer']['Layer'].pop(iLayer)

        #FIXME One attribute only. (Is always overwriting)
        newLayerDescription = xmltodict.parse(
            WMSCapabilities.getMapDescription(filename, layerAttr, latMinX, latMinY, latMaxX, latMaxY,
                                              projMinX, projMinY, projMaxX, projMaxY, maxZoom, isShapefile, downloadLink))['CONTENT']
        if 'Layer' in doc['WMT_MS_Capabilities']['Capability']['Layer']:
            doc['WMT_MS_Capabilities']['Capability']['Layer']['Layer'].append(newLayerDescription['Layer'])
        else:
            doc['WMT_MS_Capabilities']['Capability']['Layer'] = newLayerDescription

        newTileSetDescription = xmltodict.parse(
            WMSCapabilities.getTileSetDescription(filename, latMinX, latMinY, latMaxX, latMaxY, projMinX, projMinY,
                                                  projMaxX, projMaxY))['CONTENT']

        if doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities'] is not None and 'TileSet' in \
                doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']:
            if type(doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities'][
                        'TileSet']) is collections.OrderedDict:
                curTileSet = doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']['TileSet']
                doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']['TileSet'] = [
                    curTileSet]  # Transforms into a list

        if doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities'] is not None and 'TileSet' in \
                doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']:
            for iTileSet in range(
                    len(doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']['TileSet']) - 1,
                    -1, -1):
                curTileSet = doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']['TileSet'][iTileSet]
                if "Layers" in curTileSet and curTileSet["Layers"] == "GH:" + filename:
                    doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']['TileSet'].pop(iTileSet)
            doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities']['TileSet'] += newTileSetDescription[
                'TileSet']  # Dois elementos c mesma chave representa com lista
        else:
            doc['WMT_MS_Capabilities']['Capability']['VendorSpecificCapabilities'] = newTileSetDescription
        WMSCapabilities.saveCurrentCapabilities(directory, doc)

    @staticmethod
    def write_description(directory, layerTitle, layerAttr, cellTypeName, nullValue, operation):
        layerTitle = UTILS.normalizeName(layerTitle)
        cellTypeName = UTILS.normalizeName(cellTypeName)
        filecsv = "description.csv"
        csvPath = os.path.join(directory, filecsv)
        jsonPath = os.path.join(directory, "description.json")
        if os.path.isfile(csvPath):
            csvFile = open(csvPath, "r", encoding="utf-8")
        else:
            csvFile = io.StringIO("Key*, cell, null, operation, attr,\n-9999, \"\", -1, \"\", nenhuma, ")

        csv_reader = csv.DictReader(csvFile, delimiter=',')
        line_count = 0
        elements = [cellTypeName, str(nullValue), operation, layerAttr]
        for row in csv_reader:
            curEntry = {
                'cellType': row[' cell'].strip(),
                'nullValue': row[' null'].strip(),
                'operation': row[' operation'].strip(),
                'attribute': row[' attr'].strip()
            }
            if line_count > 0 and curEntry['operation'] != operation and curEntry['attribute'] != layerAttr:
                # Key *, cell, null, operation, attr,
                elements.append(curEntry['cellType'])
                elements.append(curEntry['nullValue'])
                elements.append(curEntry['operation'])
                elements.append(curEntry['attribute'])
            line_count += 1
        with open(jsonPath, "w", encoding="utf-8") as jsonFile:
            jsonFile.write(json.dumps(elements))
        csvFile.close()

class WMSBBox():
    xMax = None
    def xMaximum(self):
        return self.xMax

    xMin = None
    def xMinimum(self):
        return self.xMin

    yMax = None
    def yMaximum(self):
        return self.yMax

    yMin = None
    def yMinimum(self):
        return self.yMin

    def __init__(self, xMax, xMin, yMax, yMin):
        self.xMax = xMax
        self.xMin = xMin
        self.yMax = yMax
        self.yMin = yMin


def checkGitExecutable(gitExe):
    if not gitExe or not os.path.isfile(gitExe):
        QMessageBox.error("Select your git executable program.\n" + str(
            gitExe) + "\nIt can be downloadable at: https://git-scm.com/downloads")
        exit(1)

def writeLegendJson(mapDir, legendObj):
    content = []
    for legend in legendObj:
        content.append({"color": [legend.red, legend.green, legend.blue], "title": legend.categoryName})
    jsonFile = Path(os.path.join(mapDir, "legend.json"))
    jsonFile.write_text(json.dumps(content), encoding="utf-8")

def getLegendFromPath(sldPath):
    return readLegend(sldPath)

def publishMaps(gitExe, ghUser, ghPassword, mustAskUser, gitRepository, outputDir, input_file, layerAttr, operation, max_zoom, downloadLink, cellType, nullValue, openInBrowser, legendObj, filenameTitle):
    gitExe = gitExe if os.path.isfile(gitExe) else UTILS.which("git.exe")  # Danilo testar qnd não acha o git.exe
    foundGit = ''
    gitExe = GitHub.findGitExe(gitExe, foundGit, mustAskUser)
    checkGitExecutable(gitExe)
    Feedback.pushConsoleInfo("Git executable path found: " + gitExe)
    ghUser, ghPassword = GitHub.getGitCredentials(ghUser, ghPassword, mustAskUser)
    if ghUser is None or ghPassword is None:
        QMessageBox.error("Error: Github credentials failed to authenticate.")
        exit(1)
    Feedback.pushConsoleInfo("Authentication Confirmed: " + gitExe)

    GitHub.prepareEnvironment(gitExe)
    if not GitHub.existsRepository(ghUser, gitRepository) and not GitHub.createRepo(gitRepository, ghUser, ghPassword, outputDir, Feedback()):
        QMessageBox.error(
            "Error: Failed to create the repository " + gitRepository + ".\nPlease create a one at: https://github.com/new")
        exit(1)

    if not GitHub.isOptionsOk(outputDir, ghUser, gitRepository, Feedback(), ghPassword, mustAskUser):
        QMessageBox.error("Error: Canceling the execution, please select another output folder.")
        exit(1)

    # fileName = os.path.basename(input_file)
    # fileNameWithoutExt = os.path.splitext(fileName)[0]
    layerTitle = UTILS.normalizeName(filenameTitle)
    mapDir = os.path.join(outputDir, layerTitle, layerAttr, operation)
    descriptionDir = os.path.join(outputDir, layerTitle, layerAttr)

    generateTileForMap(input_file, mapDir, max_zoom, resume=False, legendObj=legendObj) #processar os tiles
    WMSCapabilities.write_description(descriptionDir, layerTitle, layerAttr, cellType, nullValue, operation)
    writeLegendJson(mapDir, legendObj)
    layerExtents = WMSBBox(*GDAL_UTILS.getExtent(input_file))
    layerMercatorExtents = WMSBBox(*GDAL_UTILS.getExtent(input_file, 4326))
    WMSCapabilities.updateXML(outputDir, layerExtents, layerMercatorExtents, False, layerTitle, layerAttr, max_zoom, downloadLink)
    GitHub.publishTilesToGitHub(outputDir, ghUser, gitRepository, Feedback(), version, ghPassword)
    if openInBrowser:
        storeUrl = GitHub.getGitUrl(ghUser, gitRepository)
        curMapsUrl = "https://maps.csr.ufmg.br/calculator/?queryid=152&storeurl=" + storeUrl + "/&remotemap=" + "GH:" + layerTitle + ";" + layerAttr
        webbrowser.open_new(curMapsUrl)
    # #Gera Thumbnail?

ghUser = None
ghPassword = None
mustAskUser = False
gitExe = ''
layerAttr = '1'
operation = 'rgba'
downloadLink = None
cellType = 'int32'
nullValue = -128
openInBrowser = True

class DinamicaClass:
    inputs = None
dinamica = DinamicaClass()
#isDinamica = True
dinamica.inputs = {"v1": 6.0, "s1": "C:/Users/Danilo/AppData/Local/Temp/EGO6B9.tmp_TEMP\\EGOTmp_29_.tif", "s2": "Mappia_Dinamica_tst", "s3": "G:\\Danilo\\Temp\\Dinamica_Example", "s4": "New Dinamica Online Example Map", "t1": [["Category", "From", "To", "Category_Name", "red", "green", "blue"], [1.0, "3", "5", "3 \u2013 5", 0.0, 0.0, 255.0], [2.0, "6", "7", "6 \u2013 7", 0.0, 107.0, 255.0], [3.0, "8", "9", "8 \u2013 9", 0.0, 218.0, 255.0], [4.0, "10", "11", "10 \u2013 11", 71.0, 255.0, 184.0], [5.0, "12", "13", "12 \u2013 13", 182.0, 255.0, 73.0], [6.0, "14", "15", "14 \u2013 15", 255.0, 220.0, 0.0], [7.0, "16", "16", "16", 255.0, 109.0, 0.0]]}


if isDinamica:
    print(json.dumps(dinamica.inputs))
    max_zoom = int(round(dinamica.inputs["v1"]))  # 7
    gitRepository = dinamica.inputs["s2"]  # 'Mappia_Example_p6'
    outputDir = dinamica.inputs["s3"] + "\\"  # 'C:\\Users\\Danilo\\AppData\\Local\\Temp\\outputDir\\'
    #sldPath = dinamica.inputs["s4"]  # 'I:\\Danilo\\Trampo\\data_dir\\data\\laurel\\land_use_1992_2015\\land_use_1992_2015_7.sld'
    realFileName = dinamica.inputs["s4"]
    input_file = dinamica.inputs["s1"]  # "F:\\Danilo\\Trampo\\data_dir\\data\\teste\\iyield_rubber2.tif" #iyield_rubber.tif" #"F:\\Danilo\\Trampo\\data_dir\\data\\teste\\byield_rubber.tif" #"F:\\Danilo\\Trampo\\data_dir\\data\\remanescentes_florestais_desmatamento\\brasil\\perda_cobertura_vegetal_ano_hansen\\lossyear.vrt"#"F:\\Danilo\\Trampo\\data_dir\\data\\remanescentes_florestais_desmatamento\\brasil\\perda_cobertura_vegetal_ano_hansen\\lossyear.tif" #"F:\\Danilo\\Trampo\\data_dir\\data\\remanescentes_florestais_desmatamento\\brasil\\prodes\\prodes.vrt" #"F:\\Danilo\\Trampo\\data_dir\\data\\remanescentes_florestais_desmatamento\\brasil\\perda_cobertura_vegetal_ano_hansen\\lossyear.tif"
    csvInput = dinamica.inputs['t1']
    legendObj = prepareLegend(csvInput)
    print("isDinamica")
else:
    gitRepository = 'Mappia_Example_p6'
    gitExe = 'C:\\Users\\Danilo\\AppData\\Local\\Temp\\tmpp5uzno5_\\portablegit\\mingw64\\bin\\git.exe'
    max_zoom = 6
    outputDir = 'C:\\Users\\Danilo\\AppData\\Local\\Temp\\outputDir\\'
    input_file = "E:\\Danilo\\Trampo\\data_dir\\data\\teste\\iyield_rubber2.tif"  # iyield_rubber.tif" #"F:\\Danilo\\Trampo\\data_dir\\data\\teste\\byield_rubber.tif" #"F:\\Danilo\\Trampo\\data_dir\\data\\remanescentes_florestais_desmatamento\\brasil\\perda_cobertura_vegetal_ano_hansen\\lossyear.vrt"#"F:\\Danilo\\Trampo\\data_dir\\data\\remanescentes_florestais_desmatamento\\brasil\\perda_cobertura_vegetal_ano_hansen\\lossyear.tif" #"F:\\Danilo\\Trampo\\data_dir\\data\\remanescentes_florestais_desmatamento\\brasil\\prodes\\prodes.vrt" #"F:\\Danilo\\Trampo\\data_dir\\data\\remanescentes_florestais_desmatamento\\brasil\\perda_cobertura_vegetal_ano_hansen\\lossyear.tif"
    sldPath = 'E:\\Danilo\\Trampo\\data_dir\\data\\laurel\\land_use_1992_2015\\land_use_1992_2015_7.sld'
    legendObj = getLegendFromPath(sldPath)
    realFileName = 'land_use_1992_2015_7'
    print("isNotDinamica")

# if __name__ == '__main__':
# realFileName
publishMaps(gitExe, ghUser, ghPassword, mustAskUser, gitRepository, outputDir, input_file, layerAttr, operation, max_zoom, downloadLink, cellType, nullValue, openInBrowser, legendObj, realFileName)

try:
    dinamica.outputs['out'] = 1
except:
    pass