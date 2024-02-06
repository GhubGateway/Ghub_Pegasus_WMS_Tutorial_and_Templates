#----------------------------------------------------------------------------------------------------------------------
# Component of: Ghub_Pegasus_WMS_Python_Example (github.com)
# Called from: pythonLaunch.sh
# Purpose: Run a Pegasus workflow via the HUBzero hublib.cmd interface
# Author: Renette Jones-Ivey
# Date: July 2023
#---------------------------------------------------------------------------------------------------------------------

import json
import numpy as np
import os
import sys
import time

from tabulate import tabulate

def main(argv):
    
    print ('process_netcdf_info...')
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
    
    table = [['Group', 'Experiment', 'Dims', 'Resolution', 'Units', 'Calendar', 'Start', 'End', 'Time Step', 'Years']]
    
    for i in range(len(modeling_groups_list)):

        new_group = True
        
        modeling_group_path = os.path.join(ice_sheet_folder, modeling_groups_list[i])
        print ('Modeling Group Path: ', modeling_group_path)
        FH1.write('Modeling Group Path: {0}\n'.format(modeling_group_path))
        #modeling_group_path_split = modeling_group_path.split('/')
        #print ('modeling_group_path_split: ', modeling_group_path_split)
        file_basename = '_'.join(modeling_group_path.split('/')[-2:])
        #print ('file_basename: ', file_basename)
        file_name = '%s_netcdf_info.json' %file_basename
        #print ('file_name: ', file_name)
       
        if os.path.exists(file_name):
            
            try:
            
                FH2 = open (file_name , 'r')
                netcdf_dict = json.loads(FH2.read())
                print ('type(netcdf_dict): ', type(netcdf_dict))
                #print ('netcdf_dict: ', netcdf_dict)
        
                experiments = [value["experiment"] for value in netcdf_dict.values()]
                #print (type(experiments))
                #print (experiments)
                experiments = np.unique(np.array(experiments))
                #print ('type(experiments): ', type(experiments)) #<class 'list'>
                #print ('experiments: ', experiments)
                #print (type(experiments[0]))
                #print (experiments[0])
        
                for j in range(len(experiments)):
                    
                    new_experiment = True
                    
                    experiment = experiments[j]
                    
                    # Reference: https://docs.xarray.dev/en/stable/user-guide/data-structures.html#dataset-contents
                    # dims is a list of dimension names, if omitted, dimension names are taken from coords.
                    
                    keys = [value['keys'] for key, value in netcdf_dict.items() if value['experiment'] == experiment]
                    #print ('type(keys): ', type(keys))
                    #print ('keys: ', keys)
                    keys = np.array(keys)
                    #print ('keys.shape: ', keys.shape)
                    dims = [value['dims'] for key, value in netcdf_dict.items() if value['experiment'] == experiment]
                    dims = np.array(dims)
                    coords = [value['coords'] for key, value in netcdf_dict.items() if value['experiment'] == experiment]
                    coords = np.array(coords)
                    if len(dims) == 0:
                        if len(coords) == 0:
                            dims = keys
                        else:
                            dims = coords
                    resolution = [value['resolution'] for key, value in netcdf_dict.items() if value['experiment'] == experiment]
                    resolution = np.array(resolution)
                    units = [value['units'] for key, value in netcdf_dict.items() if value['experiment'] == experiment]
                    units = np.array(units)
                    calendar = [value['calendar'] for key, value in netcdf_dict.items() if value['experiment'] == experiment]
                    calendar = np.array(calendar)
                    start_exps = [value['start exp'] for key, value in netcdf_dict.items() if value['experiment'] == experiment]
                    start_exps = np.array(start_exps)
                    end_exps = [value['end exp'] for key, value in netcdf_dict.items() if value['experiment'] == experiment]
                    end_exps = np.array(end_exps)
                    time_steps = [value['time step'] for key, value in netcdf_dict.items() if value['experiment'] == experiment]
                    time_steps = np.array(time_steps)
                    duration_years = [value['duration years'] for key, value in netcdf_dict.items() if value['experiment'] == experiment]
                    duration_years = np.array(duration_years)
                    
                    combined = np.column_stack([dims, resolution, units, calendar, start_exps, end_exps, time_steps, duration_years])
                    unique_combined = np.unique(combined, axis=0)
                    #print ('unique_combined.shape: ', unique_combined.shape)
                    #print ('unique_combined: ', unique_combined)
                    #table.append(' ')
                    
                    for k in range(unique_combined.shape[0]):
                        table_entry = []
                        if (new_group):
                            table_entry.append(file_basename)
                            new_group = False
                        else:
                            table_entry.append('')
                        if (new_experiment):
                            table_entry.append(experiment)
                            new_experiment = False
                        else:
                            table_entry.append('')
                        for l in range(unique_combined.shape[1]):
                            table_entry.append(unique_combined[k,l])
                        #print (table_entry)
                        table.append(table_entry)
                        #unique_combined_string = unique_combined_string + str(unique_combined[i,:])
                    #print ('type(unique_combined_string): ', type(unique_combined_string))
                    #print ('unique_combined_string: ', unique_combined_string)
                    #FH1.write('experiment: {0: <14}: {1}\n'.format(experiment, unique_combined_string))
                    
            except Exception as e:
                print ('WARNING %s: exception encountered: %s' %(file_name, str(e)))
                FH1.write ('WARNING {0}: exception encountered: {1}\n'.format(file_name, str(e)))

        else:
            FH1.write ('WARNING {0}: file not found\n'.format(file_name))
     
    FH1.write('\n')    
    tabulated_table = tabulate(table, headers='firstrow', tablefmt='grid')
    #print (tabulated_table)
    FH1.write(tabulated_table)
    FH1.write('\n')
        
    FH1.close()
    
    elapsed_time = time.time() - start_time
    print ('elapsed time: ', np.round(elapsed_time/60.0, 2), ' [min]')

if __name__ == "__main__":

    print ('sys.argv: ', sys.argv)
    main(sys.argv)
