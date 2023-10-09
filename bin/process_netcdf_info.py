#----------------------------------------------------------------------------------------------------------------------
# Component of: ghub_exercise1 (github.com)
# Called from: Invoked as a thread from ghub_exercise1.ipynb
# Purpose: Run a Pegasus workflow via the HUBzero hublib.cmd interface
# Author: Renette Jones-Ivey
# Date: July 2023
#---------------------------------------------------------------------------------------------------------------------

import ast
import datetime
import json
import numpy as np
import os
import pandas as pd
import sys
import time

sys.path.append ('./packages')
print("sys.path: ", sys.path)

import xarray as xr
print (xr.__file__)
print (xr.__version__)

# check motonocity of a list (used to check time serie) 

def strictly_increasing(L):
    return all(x<y for x, y in zip(L, L[1:]))

def main(argv):
    
    print ('get_netcdf_info...')
    print ('argv: ', argv)
    
    start_time = time.time()

    # Process files in ISMIP6 directories
    region_path = argv[1]
    print ('region_path: ', region_path)
    # TODO 10/09/2023: list does not evaluate properly when passed in via the Pagasus workflow
    #modeling_group_list = ast.literal_eval(argv[2])
    modeling_group_list = ['AWI', 'ILTS_PIK']
    print ('type(modeling_group_list): ', type(modeling_group_list))
    print ('len(modeling_group_list): ', len(modeling_group_list))
    print ('modeling_group_list: ', modeling_group_list)
    
    FH1 = open('processed_netcdf_info.txt', 'w')
    FH1.write('\nUnique start exp, end exp and duration years combinations: \n')
    
    for i in range(len(modeling_group_list)):
    
        start_exps = []
        end_exps = []
        
        modeling_group_path = os.path.join(region_path, modeling_group_list[i])
        print ('Modeling Group: ', modeling_group_path)
        FH1.write('\nModeling Group {0}: \n'.format(modeling_group_path))
        modeling_group_path_split = modeling_group_path.split('/')
        print ('modeling_group_path_split: ', modeling_group_path_split)
        file_basename = '_'.join(modeling_group_path.split('/')[-2:])
        print ('file_basename: ', file_basename)
        FH2 = open ('%s.json' %file_basename , 'r')
        netcdf_dict = json.loads(FH2.read())
        #print ('type(netcdf_dict): ', type(netcdf_dict))
        #print ('netcdf_dict: ', netcdf_dict)

        models = [value["model"] for value in netcdf_dict.values()]
        #print (type(models))
        #print (models)
        models = np.unique(np.array(models))
        #print (type(models))
        #print (models)
        #print (type(models[0]))
        #print (models[0])

        # key: <class 'str'>
        # value: <class 'dict'>
        #for key, value in netcdf_dict.items():
           #print ('type(key): ', type(key), 'key: ', key)
           #print ('type(value): ', type(value), 'value: ', value, 'value.items(): ', value.items())
           #break;
           
        for model in models:
        
            start_exps = [value['start exp'] for key, value in netcdf_dict.items() if value['model'] == model]
            start_exps = np.array(start_exps)
            end_exps = [value['end exp'] for key, value in netcdf_dict.items() if value['model'] == model]
            end_exps = np.array(end_exps)
            duration_years = [value['duration years'] for key, value in netcdf_dict.items() if value['model'] == model]
            duration_years = np.array(duration_years)
            combined = np.column_stack([start_exps, end_exps, duration_years])
            unique_combined = np.unique(combined, axis=0)
            #print ('unique_combined.shape: ', unique_combined.shape)
            #print ('unique_combined: ', unique_combined)
            unique_combined_string = ''
            for i in range(unique_combined.shape[0]):
                unique_combined_string = unique_combined_string + str(unique_combined[i,:])
            #print ('unique_combined_string: ', unique_combined_string)
            FH1.write('\nmodel: {0: <14}: {1}'.format(model, unique_combined_string))
        FH1.write('\n')

    FH1.close()
    
    elapsed_time = time.time() - start_time
    print ('elapsed time: ', np.round(elapsed_time/60.0, 2), ' [min]')

if __name__ == "__main__":

    print ('sys.argv: ', sys.argv)
    main(sys.argv)
