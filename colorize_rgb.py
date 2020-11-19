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