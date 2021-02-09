## This is a set of Python code used to automatized snap workflows

## c2rcc.py - automatic processing of sentinel-3 images using c2rcc workflow

## s2Indices.py - automatic processing of sentinel-2 images to generate biophysical parameter (LAI, FVC) and different indices
##               Index :: NDTI = ((SWIR 1 - SWIR 2)/(SWIR 1 + SWIR 2)) 
##                        NDVIre = ((RE 1 - Red)/(RE 1 + Red))
##                        NDVI = ((NIR - Red)/(NIR + Red))
##                        SAVI = ((NIR - Red)/((NIR + Red + 0.5)*1.5))
##                        NDWI = ((Green - NIR)/(Green + NIR))
##                        MNDWI = ((Green - SWIR 1)/(Green + SWIR 1))