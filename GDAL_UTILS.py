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

