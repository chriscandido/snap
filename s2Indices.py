## Import Python Modules
import os
import sys
import time
import numpy
import snappy
import datetime

from snappy import Band, GPF
from snappy import HashMap
from snappy import Product
from snappy import ProductUtils
from snappy import ProductIO

from zipfile import ZipFile
from numpy.core.fromnumeric import product

jpy = snappy.jpy

## Extract file from zip
def do_extract_file(source, filename, outDir):
    print ('\tExtracting files in ZIP to %s'%outDir)
    with ZipFile(source, 'r') as zipObj:
        zipObj.extractall(outDir)

## Convert to DIM
def do_convert_to_dim(source, name):
    print ('\tConverting to DIM')
    product = ProductIO.readProduct(source)
    HashMap = jpy.get_type('java.util.HashMap')
    parameters = HashMap()
    GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
    parameters.put('file', name)
    parameters.put('fileFormat', 'BEAM-DIMAP')
    
    output = GPF.createProduct('Write', parameters, product)
    return output

## Resampling 
def do_resampling(source):
    print ('\tResampling ...')
    product = ProductIO.readProduct(source)
    HashMap = jpy.get_type('java.util.HashMap')
    parameters = HashMap()
    GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
    parameters.put('targetResolution', 10)

    output = GPF.createProduct('Resample', parameters, product)
    return output

## Biophysical Parameters
def do_biophysical_parameter(source):
    print ('\tBiophysical Parameters ...')
    HashMap = jpy.get_type('java.util.HashMap')
    parameters = HashMap()
    GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
    parameters.put('computeLAI', True)
    ##parameters.put('computeFcover', True)

    output = GPF.createProduct('BiophysicalOp', parameters, source)
    return output

def do_band_maths(source):
    ## Input product, dimensions, and properties
    print ('\tBand Indices ...')
    product = source
    ## product = ProductIO.readProduct(source)
    width = product.getSceneRasterWidth()
    height = product.getSceneRasterHeight()
    name = product.getName()
    description = product.getDescription()
    bandNames = product.getBandNames()

    print ("Product: %s, %d x %d pixels, %s" % (name, width, height, description))
    print ("Bands: %s", (list(bandNames)))

    GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
    BandDescriptor = jpy.get_type('org.esa.snap.core.gpf.common.BandMathsOp$BandDescriptor')

    ## NDVI
    targetBand1 = BandDescriptor()
    targetBand1.name = 'ndvi'
    targetBand1.type = 'float32'
    targetBand1.expression = '(B8 - B4) / (B4 + B8)'

    ## SAVI
    targetBand2 = BandDescriptor()
    targetBand2.name = 'savi'
    targetBand2.type = 'float32'
    targetBand2.expression = '(B8 - B4) / ((B8 + B4 + 0.5)*1.5)'

    ## NDWI
    targetBand3 = BandDescriptor()
    targetBand3.name = 'ndwi'
    targetBand3.type = 'float32'
    targetBand3.expression = '(B3 - B8) / (B3 + B8)'

    ## MNDWI
    targetBand4 = BandDescriptor()
    targetBand4.name = 'mndwi'
    targetBand4.type = 'float32'
    targetBand4.expression = '(B3 - B11) / (B3 + B11)'

    ## NDBI
    targetBand5 = BandDescriptor()
    targetBand5.name = 'ndbi'
    targetBand5.type = 'float32'
    targetBand5.expression = '(B11 - B8) / (B11 + B8)'

    ## BAEI
    targetBand6 = BandDescriptor()
    targetBand6.name = 'baei'
    targetBand6.type = 'float32'
    targetBand6.expression = '(B4 + 0.3) / (B3 + B11)'

    ## NBI
    targetBand7 = BandDescriptor()
    targetBand7.name = 'nbi'
    targetBand7.type = 'float32'
    targetBand7.expression = '(B11*B4) / (B8)'

    ## UI
    targetBand8 = BandDescriptor()
    targetBand8.name = 'ui'
    targetBand8.type = 'float32'
    targetBand8.expression = '(B11 - B8) / (((B11 + B8) + 1.0)*100)'

    ## BSI
    targetBand9 = BandDescriptor()
    targetBand9.name = 'bsi'
    targetBand9.type = 'float32'
    targetBand9.expression = '((B11 + B4) - (B8 + B2)) / ((B11 + B4) + (B8 + B2))'

    targetBands = jpy.array('org.esa.snap.core.gpf.common.BandMathsOp$BandDescriptor', 9)
    targetBands[0] = targetBand1
    targetBands[1] = targetBand2
    targetBands[2] = targetBand3
    targetBands[3] = targetBand4
    targetBands[4] = targetBand5
    targetBands[5] = targetBand6
    targetBands[6] = targetBand7
    targetBands[7] = targetBand8
    targetBands[8] = targetBand9

    HashMap = jpy.get_type('java.util.HashMap')
    parameters = HashMap()
    parameters.put('targetBands', targetBands)

    result = GPF.createProduct('BandMaths', parameters, product)
    print ('Writing ...')

    return result

def main():
    ## All Sentinel-2 data subfolders are located within a super folder (make sure data is already unzipped and each sub folder name ends with .SAFE)
    zipDir = r'D:\Misc\S2_Images'
    raw = r'D:\Misc\Raw'
    path = r'D:\Misc\Test'
    outpath = r'D:\Misc\Out'

    if not os.path.exists(outpath):
        os.makedirs(outpath)
    
    ## Extraction of ZIP file
    for files in os.listdir(zipDir):
        s2File = zipDir + "\\" + files
        print ('Filename: ', s2File)
        result = do_extract_file(s2File, files, raw)
        print ('\t\tExtracting ...')
    
    print ('Done.')
    
    ## Copnverting .SAFE to .dim
    for files in os.listdir(raw): 
        safe = raw + "\\" + files + "\\MTD_MSIL2A.xml"
        print ('Filename: ', safe)

        loopstarttime = str(datetime.datetime.now())
        print ("Start time: ", loopstarttime)
        startTime = time.time()

        print ("Start Converting ...")
        result = do_convert_to_dim(safe, files.split('.SAFE')[0])
        ProductIO.writeProduct(result, path + "\\" + files.split('.SAFE')[0] + '.dim', 'BEAM-DIMAP')
        
        print ("Done.")       
        print("--- %s seconds ---" % (time.time() - startTime))

    ## Processing of Vegetation Indices
    print ('Start Processing Indices ...')
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith((".dim")) and not name.startswith('.'):
                ## Image Filename
                imgFile = path + "/" + name
                print ("Filename: ", imgFile)

                loopstarttime = str(datetime.datetime.now())
                print ("Start time: ", loopstarttime)
                startTime = time.time()

                ## Start processing
                print ("Processing ...")
                resample = do_resampling(imgFile)
                result = do_band_maths(resample)
                outFileName = outpath + "/" + name.split(".dim")[0] + "_indices.dim"
                ProductIO.writeProduct(result, outFileName, 'BEAM-DIMAP')
                print ("Done.")       
                print("--- %s seconds ---" % (time.time() - startTime))

if __name__=="__main__":
    main()