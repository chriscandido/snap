###############################################################################################
# C2RCC                                                                                       #
# To automatically perform c2rcc on Sentinel-3 Images                                         #
###############################################################################################
import numpy
import shutil
import sys
import os

import snappy
from snappy import GPF
from snappy import HashMap
from snappy import ProductIO

import fileinput
import subprocess

path = r"D:/c2rcc"

jpy = snappy.jpy

dictionary = {}
for root, dirs, files in os.walk (path):
    for name in files:
        if name.endswith((".dim")) and not name.startswith('.'):
                print ('Filename', name)
                
                sal = 35.0
                temp = 15.0
                ozo = 330.0
                pres = 1000.0
                TSMfakBpart = 1.72
                TSMfakBwit = 3.1
                CHLexp = 1.04
                CHLfak = 21.0
                thresholdRtosaOOS=0.005
                thresholdAcReflecOos=0.1
                thresholdCloudTDown865=0.955
                outputAsRrs=False
                deriveRwFromPathAndTransmittance=False
                useEcmwfAuxData=True
                outputRtoa=True
                outputRtosaGc=False
                outputRtosaGcAann=False
                outputRpath=False
                outputTdown=False
                outputTup=False
                outputAcReflectance=True
                outputRhown=True
                outputOos=False
                outputKd=True
                outputUncertainties=True

                inFolder = str(path + '/' + name)
                OLI=ProductIO.readProduct(inFolder)
                print ('C2RCC')
                HashMap = jpy.get_type('java.util.HashMap')
                parameters = HashMap()
                parameters.put('validPixelExpression','(!quality_flags.invalid && (!quality_flags.land || quality_flags.fresh_inland_water))')
                parameters.put('temperature',temp)
                parameters.put('salinity',sal)
                parameters.put('ozone',ozo)
                parameters.put('press',pres)
                parameters.put('TSMfac',TSMfakBpart)
                parameters.put('TSMexp',TSMfakBwit)
                parameters.put('CHLexp',CHLexp)
                parameters.put('CHLfak',CHLfak)
                parameters.put('thresholdRtosaOOS',thresholdRtosaOOS)
                parameters.put('thresholdAcReflecOos',thresholdAcReflecOos)
                parameters.put('thresholdCloudTDown865',thresholdCloudTDown865)
                parameters.put('outputAsRrs',outputAsRrs)
                parameters.put('deriveRwFromPathAndTransmittance',deriveRwFromPathAndTransmittance)
                parameters.put('useEcmwfAuxData',useEcmwfAuxData)
                parameters.put('outputRtoa',outputRtoa)
                parameters.put('outputRtosaGc',outputRtosaGc)
                parameters.put('outputRtosaGcAann',outputRtosaGcAann)
                parameters.put('outputRpath',outputRpath)
                parameters.put('outputTdown',outputTdown)
                parameters.put('outputTup',outputTup)
                parameters.put('outputAcReflectance',outputAcReflectance)
                parameters.put('outputRhown',outputRhown)
                parameters.put('outputOos',outputOos)
                parameters.put('outputKd',outputKd)
                parameters.put('outputUncertainties',outputUncertainties)
                result = GPF.createProduct('c2rcc.olci', parameters, OLI)
                tmpName = path+"/" + name.split(".dim")[0]+"_c2rcc.dim"
                ProductIO.writeProduct(result,tmpName,"BEAM-DIMAP")
                print ("Product Writing .... ")
print ('DONE')
