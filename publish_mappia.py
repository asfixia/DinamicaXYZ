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

try:
    import QMessageBox
except:
    pass
#include QMessageBox.py
#include Feedback.py

try:
    from colorize_rgb import applyLegendCsv, applyLegend, readLegend, prepareLegend
except:
    pass #Not in Dinamica Code
#include colorize_rgb.py

try:
    from UTILS import UTILS
except:
    pass #Not in Dinamica Code
#include UTILS.py

try:
    from GitHub import GitHub
except:
    pass #Not in Dinamica Code
#include GitHub.py

try:
    from Feedback import Feedback
except:
    pass #Not in Dinamica Code
#include Feedback.py


try:
    from gdal2tiles_local import generateTileForMap
except:
    pass #Not in Dinamica Code
#include gdal2tiles_local.py

try:
    from WMSCapabilities import WMSCapabilities
    from WMSCapabilities import WMSBBox
except:
    pass #Not in Dinamica Code
#include WMSCapabilities.py


try:
    from GDAL_UTILS import GDAL_UTILS
except:
    pass #Not in Dinamica Code
#include GDAL_UTILS.py


try:
    from WMSCapabilities import WMSCapabilities
except:
    pass
#include WMSCapabilities.py

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

def publishMaps(gitExe, ghUser, ghPassword, mustAskUser, ghRepository, outputDir, input_file, layerAttr, operation, max_zoom, downloadLink, cellType, nullValue, openInBrowser, legendObj, filenameTitle):
    gitExe = gitExe if os.path.isfile(gitExe) else UTILS.which("git.exe")  # Danilo testar qnd não acha o git.exe
    foundGit = ''
    feedback = Feedback()
    gitExe = GitHub.findGitExe(gitExe, foundGit, feedback, mustAskUser)
    checkGitExecutable(gitExe)
    if gitExe:
        GitHub.prepareEnvironment(gitExe)
    Feedback.pushConsoleInfo("Git executable path found: " + gitExe)
    ghUser, ghPassword = GitHub.getGitCredentials(ghUser, ghPassword, mustAskUser)
    if ghUser is None or ghPassword is None:
        QMessageBox.error("Error: Github credentials failed to authenticate.")
        exit(1)
    Feedback.pushConsoleInfo("Authentication Confirmed: " + gitExe)

    if ((not GitHub.existsRepository(ghUser, ghRepository, ghPassword) and not GitHub.createRepo(ghRepository, ghUser, ghPassword, outputDir, Feedback()))
            or (GitHub.existsRepository(ghUser, ghRepository, ghPassword) and not GitHub.isRepositoryInitialized(ghUser, ghRepository)
                and not GitHub.initializeRepository(outputDir, ghUser, ghRepository, ghPassword, feedback))):
        QMessageBox.error(
            "Error: Failed to create the repository " + ghRepository + ".\nPlease create a one at: https://github.com/new")
        exit(1)

    if not GitHub.isOptionsOk(outputDir, ghUser, ghRepository, Feedback(), ghPassword, mustAskUser):
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
    GitHub.publishTilesToGitHub(outputDir, ghUser, ghRepository, Feedback(), version, ghPassword)
    if openInBrowser:
        storeUrl = GitHub.getGitUrl(ghUser, ghRepository)
        curMapsUrl = "https://maps.csr.ufmg.br/calculator/?queryid=152&storeurl=" + storeUrl + "/&remotemap=" + "GH:" + layerTitle + ";" + layerAttr
        webbrowser.open_new(curMapsUrl)
    # #Gera Thumbnail?

curUser = None
ghPassword = None
mustAskUser = False
gitExe = ''
layerAttr = '1'
operation = 'rgba'
downloadLink = None
cellType = 'int32'
nullValue = -128
openInBrowser = True

# class DinamicaClass:
#     inputs = None
# dinamica = DinamicaClass()
# isDinamica = True
# dinamica.inputs = {"v1": 4.0, "s1": "C:/Users/Danilo/AppData/Local/Temp/EGO96D7.tmp_TEMP\\EGOTmp_36_.tif", "s2": "Mappia_Dinamica2", "s3": "C:/Users/Danilo/AppData/Local/Temp/teste2", "s4": "outro2", "t1": [["Category", "From", "To", "Category_Name", "red", "green", "blue"], [1.0, "0.1166", "0.3548", "0.1166 \u2013 0.3548", 0.0, 0.0, 255.0], [2.0, "0.3549", "0.5868", "0.3549 \u2013 0.5868", 0.0, 107.0, 255.0], [3.0, "0.5869", "0.7783", "0.5869 \u2013 0.7783", 0.0, 218.0, 255.0], [4.0, "0.7784", "0.9006", "0.7784 \u2013 0.9006", 71.0, 255.0, 184.0], [5.0, "0.9007", "0.9600", "0.9007 \u2013 0.9600", 182.0, 255.0, 73.0], [6.0, "0.9601", "0.9940", "0.9601 \u2013 0.9940", 255.0, 220.0, 0.0], [7.0, "0.9941", "1.0", "0.9941 \u2013 1.0", 255.0, 109.0, 0.0]]}


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
    gitRepository = 'Mappia_Example_p6asdaz'
    max_zoom = 6
    outputDir = 'C:\\Users\\Danilo\\AppData\\Local\\Temp\\outputDir\\'
    input_file = "E:\\Danilo\\Trampo\\data_dir\\data\\teste\\iyield_rubber2.tif"  # iyield_rubber.tif" #"F:\\Danilo\\Trampo\\data_dir\\data\\teste\\byield_rubber.tif" #"F:\\Danilo\\Trampo\\data_dir\\data\\remanescentes_florestais_desmatamento\\brasil\\perda_cobertura_vegetal_ano_hansen\\lossyear.vrt"#"F:\\Danilo\\Trampo\\data_dir\\data\\remanescentes_florestais_desmatamento\\brasil\\perda_cobertura_vegetal_ano_hansen\\lossyear.tif" #"F:\\Danilo\\Trampo\\data_dir\\data\\remanescentes_florestais_desmatamento\\brasil\\prodes\\prodes.vrt" #"F:\\Danilo\\Trampo\\data_dir\\data\\remanescentes_florestais_desmatamento\\brasil\\perda_cobertura_vegetal_ano_hansen\\lossyear.tif"
    sldPath = 'E:\\Danilo\\Trampo\\data_dir\\data\\laurel\\land_use_1992_2015\\land_use_1992_2015_7.sld'
    legendObj = getLegendFromPath(sldPath)
    realFileName = 'land_use_1992_2015_7'
    print("isNotDinamica")

# if __name__ == '__main__':
# realFileName

curUser = 'asfixia'
ghPassword = '9e9805573b5af294e24dd50caf6e1fda9ad56a92'
gitExe = 'C:\\Users\\Danilo\\AppData\\Local\\Temp\\tmpi3pm8k1v\\portablegit\\mingw64\\bin\\git.exe'
publishMaps(gitExe, curUser, ghPassword, mustAskUser, gitRepository, outputDir, input_file, layerAttr, operation, max_zoom, downloadLink, cellType, nullValue, openInBrowser, legendObj, realFileName)

try:
    dinamica.outputs['out'] = 1
except:
    pass