#!/bin/sh

# For interim testing on CCR.
# Also see ./remotebin/pythonLaunch.sh

# Enter cat /etc/os-release to see the Linux operating system name and version.
# old CCR env os-release and version on 09/18/2023:
# CentOS Linux 7 (based on Red Hat Enterprise Linux)
# new CCR env os-release and version on 09/18/2023:
# Ubuntu 22.04.3 LTS (based on Debian Linus)

# Load python module
# old CCR env:
module load python/py38-anaconda-2021.05
# new CCR env:
#module load anaconda3/2022.05
which python

python ./process_netcdf_info.py "/projects/grid/ghub/ISMIP6/Projections/Reprocessed/CMIP6_Archive_Final/AIS" "['AWI', 'ILTS_PIK']"
