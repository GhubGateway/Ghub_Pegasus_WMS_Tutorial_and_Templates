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
    ice_sheet_folder = argv[1]
    print ('ice_sheet_folder: ', ice_sheet_folder)
    #modeling_group_path_split = modeling_group_path.split('/')
    #print ('modeling_group_path_split: ', modeling_group_path_split)
    ice_sheet = ice_sheet_folder.split('/')[-1]
    print ('ice_sheet: ', ice_sheet)
    ice_sheet_description = argv[2]
    print ('ice_sheet_description: ', ice_sheet_description)
    modeling_groups = argv[3]
    modeling_groups_list = list(modeling_groups.split(','))
    print ('type(modeling_groups_list): ', type(modeling_groups_list))
    print ('len(modeling_groups_list): ', len(modeling_groups_list))
    print ('modeling_groups_list: ', modeling_groups_list)
    
    FH1 = open('%s_processed_netcdf_info.txt' %ice_sheet, 'w')
    FH1.write('Ice sheet folder: {0}\n'.format(ice_sheet_folder))
    FH1.write('Ice sheet description: {0}\n\n'.format(ice_sheet_description))
    FH1.write('Unique experiment, iterations, start exp, end exp, time_step and duration years combinations: \n')
    
    experiments_ = []
    iterations_ = []
    start_exps_ = []
    end_exps_ = []
    time_steps_ = []
    duration_years_ = []

    for i in range(len(modeling_groups_list)):
    
        modeling_group_path = os.path.join(ice_sheet_folder, modeling_groups_list[i])
        print ('Modeling Group Path: ', modeling_group_path)
        FH1.write('\nModeling Group Path {0}: \n\n'.format(modeling_group_path))
        #modeling_group_path_split = modeling_group_path.split('/')
        #print ('modeling_group_path_split: ', modeling_group_path_split)
        file_basename = '_'.join(modeling_group_path.split('/')[-2:])
        print ('file_basename: ', file_basename)
        FH2 = open ('%s.json' %file_basename , 'r')
        netcdf_dict = json.loads(FH2.read())
        #print ('type(netcdf_dict): ', type(netcdf_dict))
        #print ('netcdf_dict: ', netcdf_dict)

        experiments = [value["experiment"] for value in netcdf_dict.values()]
        #print (type(experiments))
        #print (experiments)
        experiments = np.unique(np.array(experiments))
        #print (type(experiments))
        print (experiments)
        #print (type(experiments[0]))
        #print (experiments[0])

        # key: <class 'str'>
        # value: <class 'dict'>
        #for key, value in netcdf_dict.items():
           #print ('type(key): ', type(key), 'key: ', key)
           #print ('type(value): ', type(value), 'value: ', value, 'value.items(): ', value.items())
           #break;
           
        for experiment in experiments:
        
            experiments__ = [value['experiment'] for key, value in netcdf_dict.items() if value['experiment'] == experiment]
            experiments_.extend(experiments__)
            iterations = [value['iterations'] for key, value in netcdf_dict.items() if value['experiment'] == experiment]
            iterations_.extend(iterations)
            start_exps = [value['start exp'] for key, value in netcdf_dict.items() if value['experiment'] == experiment]
            start_exps_.extend(start_exps)
            end_exps = [value['end exp'] for key, value in netcdf_dict.items() if value['experiment'] == experiment]
            end_exps_.extend(end_exps)
            time_steps= [value['time step'] for key, value in netcdf_dict.items() if value['experiment'] == experiment]
            time_steps_.extend(time_steps)
            duration_years = [value['duration years'] for key, value in netcdf_dict.items() if value['experiment'] == experiment]
            duration_years_.extend(duration_years)
            
            iterations = np.array(iterations)
            start_exps = np.array(start_exps)
            end_exps = np.array(end_exps)
            time_steps = np.array(time_steps)
            duration_years = np.array(duration_years)
            combined = np.column_stack([iterations, start_exps, end_exps, time_steps, duration_years])
            unique_combined = np.unique(combined, axis=0)
            #print ('unique_combined.shape: ', unique_combined.shape)
            #print ('unique_combined: ', unique_combined)
            unique_combined_string = ''
            for i in range(unique_combined.shape[0]):
                unique_combined_string = unique_combined_string + str(unique_combined[i,:])
            #print ('unique_combined_string: ', unique_combined_string)
            FH1.write('experiment: {0: <14}: {1}\n'.format(experiment, unique_combined_string))
            
        FH1.write('\n')
 
    FH1.write('Summary:\n\n')
    #print ('type(experiments_): ', type(experiments_))
    #print ('experiments_: ', experiments_)
    experiments_ = np.array(experiments_)
    #print ('experiments_.shape: ', experiments_.shape)
    iterations_ = np.array(iterations_)
    #print ('iterations_.shape: ', iterations_.shape)
    start_exps_ = np.array(start_exps_)
    #print ('start_exps_.shape: ', start_exps_.shape)
    end_exps_ = np.array(end_exps_)
    #print ('end_exps_.shape: ', end_exps_.shape)
    time_steps_ = np.array(time_steps_)
    #print ('time_steps_.shape: ',time_steps_.shape)
    duration_years_ = np.array(duration_years_)
    #print ('duration_years_.shape: ', duration_years_.shape)
    combined = np.column_stack([experiments_, iterations_, start_exps_, end_exps_, time_steps_, duration_years_])
    unique_combined = np.unique(combined, axis=0)
    #print ('unique_combined.shape: ', unique_combined.shape)
    #print ('unique_combined: ', unique_combined)
    unique_combined_string = ''
    for i in range(unique_combined.shape[0]):
        FH1.write('{0}\n'.format(str(unique_combined[i,:])))

    FH1.close()
    
    elapsed_time = time.time() - start_time
    print ('elapsed time: ', np.round(elapsed_time/60.0, 2), ' [min]')

if __name__ == "__main__":

    print ('sys.argv: ', sys.argv)
    main(sys.argv)
