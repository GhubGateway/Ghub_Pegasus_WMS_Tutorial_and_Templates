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
python -m pip install --target=./elevation elevation

# Default latitude and longitude to Buffalo, NY latitude and longitude coordinates.
python ./get_tiff_map.py 42 44 -80 -78
