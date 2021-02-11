## Import Python Modules
import sentinelhub
import pandas 
import datetime

## Tile Spricification 
manilaBay_tile = ["T51PTS"]

## Start and End date 
startDate = "2020-01-01"
endDate = "2020-01-30"

dates = pandas.date_range(start=startDate, end=endDate)

for tile in manilaBay_tile:
    print ("Downloading tile: " + tile)
    for date in dates:
        print (str(date.date()) + " ...")
        try:
            sentinelhub.download_safe_format(tile=(tile, str(date.date())), entire_product=True)
        except Exception as ex:
            template = "No image for the specified tile / date combination could be found"
            message = template.format(type(ex).__name__)
            print (message)