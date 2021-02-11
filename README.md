**This is a set of Python code used to automate snap workflows**

A. c2rcc.py 
-
>  - *automatic processing of Sentinel-3 images using c2rcc algorithm in snap*

B. s2Indices.py 
-
> *automatic processing of sentinel-2 images to generate biophysical parameter (LAI, FVC) and different indices*
> 
> **List of Indices**
>  <br>A. Vegetation<br>
> `NDTI = ((SWIR 1 - SWIR 2)/(SWIR 1 + SWIR 2))`<br?
> `NDVIre = ((RE 1 - Red)/(RE 1 + Red))`<br>
> `NDVI = ((NIR - Red)/(NIR + Red))` <br>
> `SAVI = ((NIR - Red)/((NIR + Red + 0.5)*1.5))`<br>
> `NDWI = ((Green - NIR)/(Green + NIR))` <br>
> `MNDWI = ((Green - SWIR 1)/(Green + SWIR 1))` <br>
> B. Built-up <br>
> `NDBI = ((SWIR - NIR)/(SWIR + NIR))` <br>
> `BUI = (NDBI - NDVI)` <br>
> `BAEI = ((Red + 0.3)/(Green + SWIR))` <br>
> `NBI = ((SWIR x Red)/NIR)` <br>
> `VIBI = (NDVI/(NDVI + NDBI))` <br>
> `IBI = ((NDBI - (SAVI + MNDWI))/2)/((NDBI + (SAVI + MNDWI))/2)` <br>
> `UI = (((SWIR - NIR)/(SWIR + NIR)) + 1.0)*100` <br>
> `BSI = ((SWIR + R) - (NIR + B))/((SWIR + R) + (NIR + B))` <br>

	
