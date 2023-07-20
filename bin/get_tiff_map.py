#----------------------------------------------------------------------------------------------------------------------
# Class: DEM
# Component of: ghub_vhub_exercise1 (github.com)
# Called from: Invoked as a thread from ghub_exercise1.ipynb
# Purpose: Run a Pegasus workflow via the HUBzero hublib.cmd interface
# Author: Renette Jones-Ivey
# Date: July 2023
#---------------------------------------------------------------------------------------------------------------------
import sys
import numpy as np
import os
import time
import matplotlib.pyplot as plt
from matplotlib import colors, cm

# References:
# https://pypi.org/project/elevation/
# https://grasswiki.osgeo.org/wiki/GRASS_Python_Scripting_Library
# https://baharmon.github.io/python-in-grass

sys.path.append ('./packages')
#print("sys.path: ", sys.path)

import rasterio
from rasterio.plot import show
import elevation

def main(argv):
    
    print ('get_tiff_map...')
    print ('argv: ', argv)
    
    print ('os.path.expanduser("~"): ', os.path.expanduser('~'))
    workingdir = os.getcwd()
    print ('workingdir: ', workingdir)

    center_lat = float(argv[1])
    center_lon = float(argv[2])
    lat_south = float(argv[3])
    lat_north = float(argv[4])
    lon_west = float(argv[5])
    lon_east = float(argv[6])
    
    #'''
    print('center_lat: ', center_lat)
    print('center_lon: ', center_lon)
    print('lat_south: ', lat_south)
    print('lat_north : ', lat_north)
    print('lon_west: ', lon_west)
    print('lon_east: ', lon_east)
    #'''
    
    start_time = time.time()
    
    # Geotiff has only 1 band
    geotiff = os.path.join(workingdir, 'elevation.tif')
    print ('geotiff: ', geotiff)
    
    #'''
    # clip the SRTM1 30m DEM and save it to elevation1.tif.
        
    # Bounding box: left bottom right top
    elevation.clip(bounds=(lon_west, lat_south, lon_east, lat_north), output=geotiff)
    # clean up stale temporary files and fix the cache in the event of a server error
    elevation.clean()
    #'''
    
    #https://rasterio.readthedocs.io/en/stable/topics/plotting.html
    #https://towardsdatascience.com/accessing-and-visualizing-digital-elevation-models-with-python-f4fd7f595d46
    #https://github.com/GlacioHack/GeoUtils/issues/93
    
    dem = rasterio.open(geotiff)
    data=dem.read()
    cmap = plt.get_cmap('pink')
    
    # transform the georeference
    
    fig,ax1 = plt.subplots(1, 1, figsize=(10, 10))
    show(data, transform=dem.transform, contour=False, ax=ax1, cmap=cmap)
    fig.colorbar(cm.ScalarMappable(norm=colors.Normalize(vmin=np.nanmin(data), vmax=np.nanmax(data)), cmap=cmap), ax=ax1, fraction=.0305)
    #plt.show()
    fig.savefig('elevation1.png')
    plt.close()

    fig,ax2 = plt.subplots(1, 1, figsize=(10, 10))
    show(data, transform=dem.transform, contour=True, ax=ax2, cmap=cmap)
    #plt.show()
    fig.savefig('elevation2.png')
    plt.close()
            
    elapsed_time = time.time() - start_time
    print ('elapsed time: ', np.round(elapsed_time/60.0, 2), ' [min]')

if __name__ == "__main__":

    print ('sys.argv: ', sys.argv)
    main([sys.argv, 42.28, -78.67, 42.26, 42.3, -78.7, -78.64])
