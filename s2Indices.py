import datetime
import time
import numpy 
import scipy 
import shutil
import sys
import os
import gc

import snappy
from snappy import GPF
from snappy import HashMap
from snappy import Product
from snappy import ProductUtils
from snappy import ProductIO

jpy = snappy.jpy

## Resampling 
def do_resampling (source):
    print ('\tResampling ...')
    HashMap = jpy.get_type('java.util.HashMap')
    parameters = HashMap()
    GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
    parameters.put('targetResolution', 10)

    output = GPF.createProduct('Resample', parameters, source)
    return output

## Biophysical Parameters
def do_biophysical_parameter (source):
    print ('\tBiophysical Parameters ...')
    HashMap = jpy.get_type('java.util.HashMap')
    parameters = HashMap()
    GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
    parameters.put('targetResolution', 10)
    parameters.put('computeLAI', True)
    ##parameters.put('computeFcover', True)

    output = GPF.createProduct('BiophysicalOp', parameters, source)
    return output

## Indices 
def do_vegetation_indices (source):
    print ('\tVegetation Indices ...')
    ## Input product and dimensions
    input_product = ProductIO.readProduct(source)
    width = input_product.getSceneRasterWidth()
    height = input_product.getSceneRasterHeight()
    product_name = input_product.getName()
    product_description = input_product.getDescription()
    product_band_names = input_product.getBandNames()

    GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()

    ## input product red and nir bands
    b4 = input_product.getBand('B4')
    b8 = input_product.getBand('B8')

    ## output product (ndvi) new band
    output_product = Product('NDVI', 'NDVI', width, height)
    ProductUtils.copyGeoCoding(input_product, output_product)
    output_band = output_product.addBand('ndvi', ProductData.TYPE_FLOAT32)

    ## output writer
    output_product_writer = ProductIO.getProductWriter('BEAM-DIMAP')
    output_product.setProductWriter(output_product_writer)
    output_product.writeHeader(product_name + '_ndvi.dim')

    ## compute & save ndvi line by line
    red_row = numpy.zeros(width, dtype=numpy.float32)
    nir_row = numpy.zeros(width, dtype=numpy.float32)

    for y in xrange (height):
        red_row = b4.readPixels(0, y, width, 1, red_row)
        nir_row = b8.readPixels(0, y, width, 1, nir_row)
        ndvi = (nir_row - red_row)/(nir_row + red_row)
        output = output_band.writePixels(0, y, width, 1, ndvi)

    output_product.CloseIO()
    return output

def main():
    ## All Sentinel-2 data subfolders are located within a super folder (make sure data is already unzipped and each sub folder name ends with .SAFE)
    path = r'D:\Sentinel\test'
    outpath = r'D:\Sentinel\out'
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    
    for folder in os.listdir(path):
        gc.enable()
        gc.collect()
        print ("Filname: ", path + "\\" + folder + "\\manifest.safe")
        ##sentinel2 = path + "\\" + folder + "\\MTD_MSIL1C.xml"
        sentinel2 = ProductIO.readProduct(path + "\\" + folder + "\\MTD_MSIL1C.xml")

        loopstarttime = str(datetime.datetime.now())
        print ('Start time: ', loopstarttime)
        start_time = time.time()

        ## Extract mode, product type
        modestamp = folder.split("_")[1]
        productstamp = folder.split("_")[2]
        
        ## Start preprocessing 
        resample = do_resampling(sentinel2)
        biOp = do_biophysical_parameter(resample)
        ##ndvi = do_vegetation_indices(sentinel2)
        print ("outFilename: ", outpath + "\\" + folder.split(".SAFE")[0] + '_biOp' + '.dim')
        ProductIO.writeProduct(biOp, outpath + "\\" + folder.split(".SAFE")[0] + '_biOp' + '.dim', "BEAM-DIMAP")
       

if __name__=="__main__":
    main()