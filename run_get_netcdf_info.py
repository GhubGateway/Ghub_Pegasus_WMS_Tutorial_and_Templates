#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 10:53:52 2023

@author: renettej
"""

import os
import sys

#create variables for general info
self_tooldir = os.path.realpath("")

self_bindir = os.path.join(self_tooldir,"bin")

# Add to PYTHONPATH
sys.path.insert (1, self_bindir)

self_datadir = os.path.join(self_tooldir,"data")

self_workingdir = os.getcwd()

from get_netcdf_info import main
        
# For unit testing with spyder on rlj's PC
main(['', '../../ismip6aissvn-models/AWI'])
main(['', '../../ismip6aissvn-models/DOE'])
main(['', '../../ismip6aissvn-models/ILTS_PIK'])