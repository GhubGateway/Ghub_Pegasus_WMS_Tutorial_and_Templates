#!/bin/sh

# Enter cat /etc/os-release to see the Linux operatibg system name and version.
# CentOS Linux
#
# Enter module avail python to see list of available python modules.
# Also see: https://ubccr.freshdesk.com/support/solutions/articles/5000686391-software-modules

#Load python module
module load python/py37-anaconda-2020.02
which python

# Install required python packages.
# Note: complaints about pytest-astropy but packages install
python -m pip install --target=./packages rasterio
python -m pip install --target=./packages elevation

# Set default center latitude and longitude coordinates to Ellicottville, NY.
# Set default half side in miles to 4.0 miles (2.29 kilometers)
python ./get_tiff_map.py 42.28 -78.67 42.26 42.3 -78.7 -78.64
