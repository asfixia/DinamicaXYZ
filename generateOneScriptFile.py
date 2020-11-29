import os
import io

def getSource(filePath):
    with io.open(filePath, mode="r", encoding="utf-8") as sourceFile:
        return sourceFile.read()

def write(filePath, content):
    with io.open(filePath, mode="w", encoding="utf-8") as destFile:
        destFile.write(content)

def generateOneFileScript(filePath, destPath):
    fileDir = os.path.dirname(filePath)
    mainContent = getSource(filePath)
    fileContents = mainContent.split("#include ")
    futures = []
    result = []
    for i in range(0, len(fileContents)):
        curContent = fileContents[i]
        possibleInclude = curContent.split(".")
        if len(possibleInclude) > 1 and possibleInclude[1].lower().startswith("py") and not '\n' in possibleInclude[0]:
            importContent = getSource(os.path.join(fileDir, possibleInclude[0].strip() + ".py"))
            for line in importContent.split("\n"):
                if line.strip().startswith("from __future__") and not line in result:
                    importContent = importContent.replace(line, "")
                    futures.append(line)
            result.append(importContent)
            result.append(curContent[len(possibleInclude[0]) + 3:])
        else:
            result.append(curContent)
    write(destPath, #'\n'.join(futures) + '\n' +
          '\n'.join(result))




filePath = 'E:\\Danilo\\Programacao\\python\\DinamicaXYZ\\publish_mappia.py'
destPath = 'E:\\Danilo\\Programacao\\python\\DinamicaXYZ\\publish_mappia_gen.py'

generateOneFileScript(filePath, destPath)