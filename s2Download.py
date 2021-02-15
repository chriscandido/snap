## Import Python Modules
## Import Python Modules
import folium 
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt

from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt

## Connect to Copernicus Hub using Sentinel API
user = "chriscandido93"
password = "nvenesyn5868"

api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')

## Map of Manila bay Watershed
m = folium.Map([14.5995, 120.9842], zoom_start=8)
boundary = r'D:\\MapABLE\\Landcover Mapping\\Shapefile\\manilaBayWatershed_boundary.geojson'
folium.GeoJson(boundary).add_to(m)
m

## Search Imnage tile using Geojson Boundary
footprint = geojson_to_wkt(read_geojson(boundary))

products = api.query(footprint,
                     date = ('20200101', '20200131'),
                     platformname = 'Sentinel-2',
                     processinglevel = 'Level-2A',
                     cloudcoverpercentage = (0, 20))

## Convert to Geodataframe
api.to_geodataframe(products)
products_df = api.to_dataframe(products)

## Plot Areas of Image Tiles
areas = api.to_geodataframe(products)
ax = areas.plot(column='uuid', cmap=None, figsize=(20, 20))
areas.apply(lambda x: ax.annotate(s=x.uuid, xy=x.geometry.centroid.coords[0], ha='center'),axis=1)

gdf2 = gpd.read_file(boundary)
f, ax = plt.subplots(1)
areas.plot(ax=ax,column='uuid',cmap=None,)
gdf2.plot(ax=ax)
plt.show()

## Search by TileName
s2tiles = []
tileName = api.to_geodataframe(products)['title']

count = 0

for tile in tileName:
    if tile.split("_")[5] == "T51PUR":
        s2tiles.append(tileName.index[count])
    count += 1
s2tiles

## Download Sentinel Images
api.download_all(s2tiles, directory_path='D:\Misc\S2_Images')