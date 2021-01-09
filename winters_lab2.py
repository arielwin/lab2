import pandas as pd
import geopandas as gpd
import fiona
import glob
import os
from shapely.geometry import Point, LineString, Polygon
from PIL import Image
import matplotlib.pyplot as plt
from rasterstats import zonal_stats

###
###
###
### Part 1

#Set File paths using glob
#files = ['./data/districts/district01.txt','./data/districts/district05.txt','./data/districts/district06.txt']
#creat an empty dictionary to populate with the following for loop

files = glob.glob(r'data/districts/*.txt', recursive = True)
districts  = {'district' : [], 'num_coords' : [], 'geometry':[]}

#run a for loop to read each file, extract coordinates and create polygons from coordinates
#add polygons, number of coordinates and distinct name to {distircts}

for file in files:
    
    x = pd.read_csv(file, delim_whitespace=True) #read file
    coords = list(zip(x['X'],x['Y']))            #make a list of pairs from 'X','Y' columns in txt file
    poly = Polygon(coords)                       #make a polygon from that coord list
    num_coords = (len(coords))                   #get total number of coords             
    district = file[-14:-4]                      #get unique ID
    
    districts['district'].append(district)       #append name to dictionary
    districts['num_coords'].append(num_coords)   #append num coords to dictionary 
    districts['geometry'].append(poly)           #append poly shape to dictionary
    
dist_df = pd.DataFrame.from_dict(districts)                                 #turn dictionary into df
districts_gdf = gpd.GeoDataFrame(dist_df, crs={'init': 'epsg:4326'})        #turn df into gdf, assign crs --- https://geopandas.org/projections.html#setting-a-projection
districts_gdf.to_file(driver = 'ESRI Shapefile', filename = 'districts.shp')#turn gdf into shapefile of 3 districts --- https://gis.stackexchange.com/questions/204201/geopandas-to-file-saves-geodataframe-without-coordinate-system

###
###
###
### Part 2

#use glob to look for images and assign them to a list
img_list = glob.glob(r'data/agriculture/*.tif', recursive = True)
final = {'district': [], 'year': [] , 'perc_cover':[]}

for img in img_list:
    x = pd.DataFrame(zonal_stats('districts.shp', img , stats = 'sum count')) #run zonal_stats on 2004/2009 and the three districts
    sums = list(x['sum']) #list of sums
    count = list(x['count']) #list of counts
    perc_cover = [i / j for i, j in zip(sums, count)] #devide each entry in sums by each in count #https://www.geeksforgeeks.org/python-dividing-two-lists/    
    
    #I dont think this is the right way to do this but I cant quite figure out the for loop.
    for event in perc_cover:
        final['perc_cover'].append(event)
    for file in files:
        final['district'].append(file[-14:-4])
        final['year'].append(img[-13:-9])
        

final
final_df = pd.DataFrame.from_dict(final)
final_df
