#----------------------------------------------------------------------------------------------------------------------
# Component of: ghub_exercise1 (github.com)
# Called from: Invoked as a thread from ghub_exercise1.ipynb
# Purpose: Run a Pegasus workflow via the HUBzero hublib.cmd interface
# Author: Renette Jones-Ivey
# Date: July 2023
#---------------------------------------------------------------------------------------------------------------------
import numpy as np
import os
import pandas as pd
import sys
import time

sys.path.append ('./packages')
#print("sys.path: ", sys.path)

import netCDF4

def main(argv):
    
    print ('get_netcdf_info...')
    print ('argv: ', argv)
    
    start_time = time.time()

    FH1 = open('get_netcdf_info.txt', 'w')

    # Process files in ISMIP6 directories
    modeling_group_path = argv[1]
    print ('modeling_group_path: ', modeling_group_path)

    FH1.write('\nModeling Group {0} netCDF4 time units: \n'.format(modeling_group_path))

    def get_dir_ls(path):

        #print ('path: ', path)
        FH1.write ('Path {0}:\n'.format(path))
        
        for file in os.listdir(path):

            #print ('file: ', file)
            if os.path.isfile(os.path.join(path, file)):

                #print ('%s is a file' %file)
                nc_dataset = netCDF4.Dataset(os.path.join(path, file), 'r')
                #print ('type(nc_dataset): ', type(nc_dataset))
                #print ('nc_dataset: ', nc_dataset)
                             
                # Extract the variables
                keys = list(nc_dataset.variables.keys())
                #print ('type(keys): ', type(keys))
                #print ('len(keys): ', len(keys))
                
                if 'time' in keys:
                    FH1.write ('{0} time units: {1}\n'.format(file, nc_dataset.variables['time'].units))
                else:
                    FH1.write ('WARNING {0} time variable not found\n'.format(file))
                               
            elif os.path.isdir(os.path.join(path, file)):

                #print ('%s is a dir' %file)
                get_dir_ls (os.path.join(path, file))
 
            else:

                print ('WARNING %s is not a dir or file' %file)
                break
                    
    get_dir_ls(modeling_group_path)    
    FH1.close()
    
    elapsed_time = time.time() - start_time
    print ('elapsed time: ', np.round(elapsed_time/60.0, 2), ' [min]')

if __name__ == "__main__":

    print ('sys.argv: ', sys.argv)
    main(sys.argv)
