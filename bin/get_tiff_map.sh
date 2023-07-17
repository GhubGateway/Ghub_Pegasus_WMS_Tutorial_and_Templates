#!/bin/sh

#Load grass module
module load grass/7.2.2

#Load python module
which python
#module load python/py38-anaconda-2021.05
#which python

#Load gdal module
which gdalinfo
which gdal_translate
#module load gdal/2.4.0
#which gdalinfo


#Install the elevation package,
# requires gdal
#python -m pip install --target=./elevation elevation

#python ./DEM.py 0 2 -79 -77 grassdata AZUFRAL_VOLCAN_location AZUFRAL_VOLCAN_mapset AZUFRAL_VOLCAN_map
python ./get_tiff_map.py 0 2 -79 -77 grassdata AZUFRAL_VOLCAN_location PERMANENT AZUFRAL_VOLCAN_map
