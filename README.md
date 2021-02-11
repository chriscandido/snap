## This is a set of Python code used to automatized snap workflows

### c2rcc.py :: automatic processing of sentinel-3 images using c2rcc workflow

### s2Indices.py :: automatic processing of sentinel-2 images to generate biophysical parameter (LAI, FVC) and different indices
<br>    Index :: 
<br>&nbsp;&nbsp;a. VEGETATION
<br>&nbsp;&nbsp;&nbsp;NDTI = ((SWIR 1 - SWIR 2)/(SWIR 1 + SWIR 2)) 
<br>&nbsp;&nbsp;&nbsp;NDVIre = ((RE 1 - Red)/(RE 1 + Red))
<br>&nbsp;&nbsp;&nbsp;NDVI = ((NIR - Red)/(NIR + Red))
<br>&nbsp;&nbsp;&nbsp;SAVI = ((NIR - Red)/((NIR + Red + 0.5)*1.5))
<br>&nbsp;&nbsp;&nbsp;NDWI = ((Green - NIR)/(Green + NIR))
<br>&nbsp;&nbsp;&nbsp;MNDWI = ((Green - SWIR 1)/(Green + SWIR 1))
<br>&nbsp;&nbsp;b. BUILT-UP 
<br>&nbsp;&nbsp;&nbsp;NDBI = ((SWIR - NIR)/(SWIR + NIR))
<br>&nbsp;&nbsp;&nbsp;BUI = (NDBI - NDVI)
<br>&nbsp;&nbsp;&nbsp;BAEI = ((Red + 0.3)/(Green + SWIR))
<br>&nbsp;&nbsp;&nbsp;NBI = ((SWIR x Red)/NIR)
<br>&nbsp;&nbsp;&nbsp;VIBI = (NDVI/(NDVI + NDBI))
<br>&nbsp;&nbsp;&nbsp;IBI = ((NDBI - (SAVI + MNDWI))/2)/((NDBI + (SAVI + MNDWI))/2)
<br>&nbsp;&nbsp;&nbsp;UI = (((SWIR - NIR)/(SWIR + NIR)) + 1.0)*100
<br>&nbsp;&nbsp;&nbsp;BSI = ((SWIR + R) - (NIR + B))/((SWIR + R) + (NIR + B))