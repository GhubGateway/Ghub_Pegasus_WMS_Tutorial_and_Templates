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

# References:
# https://pypi.org/project/elevation/
# https://grasswiki.osgeo.org/wiki/GRASS_Python_Scripting_Library
# https://baharmon.github.io/python-in-grass

sys.path.append ('./elevation')
#print("sys.path: ", sys.path)

import elevation
#help (elevation)

#CCR: /util/academic/grass7.2.2/anaconda2/lib/python2.7/site-packages/osgeo/gdal.py
from osgeo import gdal
#help(gdal)

def main(argv):
    
    print ('DEM.py...')
    #print (argv)
    
    print ('os.path.expanduser("~"): ', os.path.expanduser('~'))
    workingdir = os.getcwd()
    print ('workingdir: ', workingdir)

    lat_south = float(argv[1])
    lat_north = float(argv[2])
    lon_west = float(argv[3])
    lon_east = float(argv[4])
    
    #'''
    print('lat_south: ', lat_south)
    print('lat_north : ', lat_north)
    print('lon_west: ', lon_west)
    print('lon_east: ', lon_east)
    #'''
    
    # Set GISBASE environment variable
    gisbase = '/util/academic/grass7.2.2/grass-7.2.2'
    os.environ['GISBASE'] = gisbase
    print ("os.environ['GISBASE']: ", os.environ['GISBASE'])
    
    # Set GISLOCK environment variable
    os.environ['GISLOCK'] = '$$'
    
    # define GRASS-Python environment
    grass_python_dir = os.path.join(gisbase, "etc", "python")
    print ('grass_python_dir: ', grass_python_dir)
    sys.path.append(grass_python_dir)
    print ('sys.path: ', sys.path)
    
    #print ('Current GRASS 7 environment: ', grass_script.gisenv())
    
    start_time = time.time()
    
    print ('workingdir: ', workingdir)
    
    # Geotiff has only 1 band
    geotiff1 = os.path.join(workingdir, 'elevation1.tif')
    print ('geotiff1: ', geotiff1)
    geotiff2 = os.path.join(workingdir, 'elevation2.tif')
    print ('geotiff2: ', geotiff2)
    
    #'''
    # clip the SRTM1 30m DEM and save it to elevation1.tif.
        
    # Bounding box: left bottom right top
    elevation.clip(bounds=(lon_west, lat_south, lon_east, lat_north), output=geotiff1)
    # clean up stale temporary files and fix the cache in the event of a server error
    elevation.clean()
    #'''
    
    # elevation1.tif: Band 1 Block=256x256 Type=Int16, ColorInterp=Gray
    print (gdal.Info(geotiff1))
    
    # Translate to floating Point datas
    
    ds = gdal.Open(geotiff1)
    ds = gdal.Translate(geotiff2, ds, outputType=gdal.GDT_Float32)
    ds = None
    
    #Band 1 Block=7200x1 Type=Float32, ColorInterp=Gray    
    print (gdal.Info(geotiff2))
            
    elapsed_time = time.time() - start_time
    print ('elapsed time: ', np.round(elapsed_time/60.0, 2), ' [min]')

if __name__ == "__main__":

    main(sys.argv)


    
