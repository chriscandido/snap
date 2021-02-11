## Import Python Modules
import os
import sys
import time
import numpy
from numpy.core.fromnumeric import product
import snappy
import datetime

from snappy import Band, GPF
from snappy import HashMap
from snappy import Product
from snappy import ProductUtils
from snappy import ProductIO

jpy = snappy.jpy

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

    ## BSI
    targetBand2 = BandDescriptor()
    targetBand2.name = 'bsi'
    targetBand2.type = 'float32'
    targetBand2.expression = '((B11 + B4) - (B8 + B2)) / ((B11 + B4) + (B8 + B2))'

    targetBands = jpy.array('org.esa.snap.core.gpf.common.BandMathsOp$BandDescriptor', 2)
    targetBands[0] = targetBand1
    targetBands[1] = targetBand2

    HashMap = jpy.get_type('java.util.HashMap')
    parameters = HashMap()
    parameters.put('targetBands', targetBands)

    result = GPF.createProduct('BandMaths', parameters, product)
    print ('Writing ...')

    return result

def main():
    ## All Sentinel-2 data subfolders are located within a super folder (make sure data is already unzipped and each sub folder name ends with .SAFE)
    raw = r'D:\Misc\Raw'
    path = r'D:\Misc\Test'
    outpath = r'D:\Misc\Out'

    if not os.path.exists(outpath):
        os.makedirs(outpath)
    
    for files in os.listdir(raw): 
        safe = raw + "\\" + files + "\\MTD_MSIL2A.xml"
        print ('Filename: ', safe)
        result = do_convert_to_dim(safe, files.split('.SAFE')[0])
        ProductIO.writeProduct(result, path + "\\" + files.split('.SAFE')[0] + '.dim', 'BEAM-DIMAP')
        print ('Done.')
    print ('Start Processing ...')
    
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