## This is a set of Python code used to automatized snap workflows

### c2rcc.py :: automatic processing of sentinel-3 images using c2rcc workflow

### s2Indices.py :: automatic processing of sentinel-2 images to generate biophysical parameter (LAI, FVC) and different indices
<br><t>Index :: 
<br><t><t>a. VEGETATION
<br><t><t><t>NDTI = ((SWIR 1 - SWIR 2)/(SWIR 1 + SWIR 2)) 
<br><t><t><t>NDVIre = ((RE 1 - Red)/(RE 1 + Red))
<br><t><t><t>NDVI = ((NIR - Red)/(NIR + Red))
<br><t><t><t>SAVI = ((NIR - Red)/((NIR + Red + 0.5)*1.5))
<br><t><t><t>NDWI = ((Green - NIR)/(Green + NIR))
<br><t><t><t>MNDWI = ((Green - SWIR 1)/(Green + SWIR 1))
<br><t><t>b. BUILT-UP 
<br><t><t><t>NDBI = ((SWIR - NIR)/(SWIR + NIR))
<br><t><t><t>BUI = (NDBI - NDVI)
<br><t><t><t>BAEI = ((Red + 0.3)/(Green + SWIR))
<br><t><t><t>NBI = ((SWIR x Red)/NIR)
<br><t><t><t>VIBI = (NDVI/(NDVI + NDBI))
<br><t><t><t>IBI = ((NDBI - (SAVI + MNDWI))/2)/((NDBI + (SAVI + MNDWI))/2)
<br><t><t><t>UI = (((SWIR - NIR)/(SWIR + NIR)) + 1.0)*100
<br><t><t><t>BSI = ((SWIR + R) - (NIR + B))/((SWIR + R) + (NIR + B))