#----------------------------------------------------------------------------------------------------------------------
# Component of: Ghub_Pegasus_WMS_Python_Example (github.com)
# Called from: Invoked as a thread from ghub_exercise1.ipynb
# Purpose: Run a Pegasus WMS Python workflow via the HUBzero hublib.cmd interface
# Author: Renette Jones-Ivey
# Date: July 2023
#---------------------------------------------------------------------------------------------------------------------

import datetime
import json
import numpy as np
import os
import pandas as pd
import sys
import time

import xarray as xr
#print (xr.__file__)
#print (xr.__version__)

from tabulate import tabulate

# check motonocity of a list (used to check time serie) 
def strictly_increasing(L):
    return all(x<y for x, y in zip(L, L[1:]))

def main(argv):
    
    print ('get_netcdf_info...')
    print ('argv: ', argv)
    
    start_time = time.time()
    
    # Process files in ISMIP6 directories
    
    modeling_group_path = argv[1]
    print ('modeling_group_path: ', modeling_group_path)

    recognized_variables = ['acabf', 'libmassbffl', 'lithk', 'sftflf', 'sftgif', 'sftgrf', 'topg', 'xvelmean', 'xvelsurf', 'yvelmean', 'yvelsurf']
    print ('recognized_variables: ', recognized_variables)
    
    file_basename = '_'.join(modeling_group_path.split('/')[-2:])
    print ('file_basename: ', file_basename)
    
    FH1 = open('%s_netcdf_info.txt' %file_basename, 'w')
    
    print ('Modeling Group Path: ', modeling_group_path)
    FH1.write('\nModeling Group Path: {0}\n\n'.format(modeling_group_path))
    
    table = [['Group', 'Model', 'Experiment', 'Variable', 'Iterations', 'Units', 'Calendar', 'Avgyear', 'Start', 'End', 'Time Step', 'Duration Years']]

    netcdf_dict = {}
    netcdf_dict_json_file = '%s_netcdf_info.json' %file_basename
    
    def get_dir_ls(path):

        print ('Path: ', path)
        #FH1.write ('Path {0}:\n'.format(path))
        
        for file in sorted(os.listdir(path)):

            #print ('file: ', file)
            if os.path.isfile(os.path.join(path, file)):

                # Ignore hidden files
                if file.startswith('.') == False:
                
                    try:
                        
                        file_split = file.split('_')
                        path_split = path.split('/')
                        
                        variable = file_split[0]
                        
                        if variable in recognized_variables:

                            #print ('variable: ', variable)
                            ice_sheet = path_split[-4]
                            #print ('ice_sheet: ', ice_sheet)
                            modeling_group = path_split[-3]
                            #print ('modeling_group: ', modeling_group)
                            model  = path_split[-2]
                            #print('model: ', model)
                            experiment = path_split[-1]
                            #print ('experiment: ', experiment)
                            experiment_split = experiment.split('_')
                            if str.isnumeric(experiment_split[-1]):
                                # Remove the resolution from the model name
                                experiment = '_'.join(experiment_split[:-1])
                            #print ('experiment ', experiment)
                            ddi_name = '_'.join([ice_sheet, modeling_group, model, experiment, variable])
                            #print ('ddi_name: ', ddi_name)
    
                            #'''
                            # By default, xarray decodes the time values and in this case,
                            # the units and calendar attributes are consumed into the returned time values
                            ds = xr.open_dataset(os.path.join(path,file), decode_times=False)
                            
                            #print (type(ds)) #<class 'xarray.core.dataset.Dataset'>
                            #print ('type(ds.values()): ', type(ds.values())) #c<lass 'collections.abc.ValuesView'>
                            #print ('ds.values(): ', ds.values())
                            coords = list(ds.coords)
                            #print ('type(coords): ', type(coords))
                            #print ('coords: ', coords)
                            
                            if 'time' in coords:
                            
                                #print (list(ds.keys()))
                                #print (list(ds.coords))
                                #print ("ds['time'].attrs: ", ds['time'].attrs)
                                units = ds['time'].attrs['units']
                                #print ('units: ', units)
                                calendar = ds['time'].attrs['calendar']
                                #print ('calendar: ', calendar)

                                ds = xr.open_dataset(os.path.join(path,file))
                            
                                #print (type(ds)) #<class 'xarray.core.dataset.Dataset'>
                                #print ('type(ds.values()): ', type(ds.values())) #c<lass 'collections.abc.ValuesView'>
                                #print ('ds.values(): ', ds.values())
                                coords = list(ds.coords)
                                #print ('type(coords): ', type(coords))
                                #print ('coords: ', coords)

                                time = ds['time'].values
                                #print ('type(time): ', type(time))
                                #print ('type(time[0]): ', type(time[0]))
                                #print ('time[0]: ', time[0])
                                #print ("type (min(ds['time']).values): ", type (min(ds['time']).values))
                                #print ("min(ds['time']).values: ", min(ds['time']).values)
                                iterations = len(time)
                                #print ('iterations: ', iterations)
                            
                                mintime = min(ds['time']).values
                                #print ('type(mintime): ', type(mintime)) #<class 'numpy.ndarray'>
                                #print ('mintime.shape: ', mintime.shape) #()
                                #print ('mintime: ', mintime)
                                #print ('mintime: ', mintime.astype("datetime64[D]"))
                                maxtime = max(ds['time']).values
                                #print ('type(maxtime): ', type(maxtime)) #<class 'numpy.ndarray'>
                                #print ('maxtime.shape: ', maxtime.shape) #()
                                #print ('maxtime: ', maxtime)
                                #print ('maxtime: ', maxtime.astype("datetime64[D]"))
                                
                                #start_exp = min(ds['time']).values.astype("datetime64[D]")
                                start_exp = mintime.astype("datetime64[D]")
                                #end_exp  = max(ds['time']).values.astype("datetime64[D]")
                                end_exp  = maxtime.astype("datetime64[D]")
                                avgyear = 365        # pedants definition of a year length with leap years
                                calendar_split = calendar.split('_')
                                if len(calendar_split) == 2 and calendar_split[1] == 'day':
                                   avgyear = int(calendar_split[0])
                                #print ('avgyear: ', avgyear)
                                duration_days = (end_exp - start_exp)
                                duration_years =  duration_days.astype('timedelta64[Y]')/np.timedelta64(1,'Y')
                                #print ('duration days: ', duration_days)
                                #print ('duration years: ', duration_years)
        
                                if np.issubdtype(start_exp.dtype, np.datetime64) & np.issubdtype(start_exp.dtype, np.datetime64):
                                    
                                    if strictly_increasing(ds.coords['time']):
                                        
                                        if isinstance((ds['time'].values[1]-ds['time'].values[0]),datetime.timedelta):
                                            time_step = (ds['time'].values[1]-ds['time'].values[0]).days
                                        else:
                                            if isinstance((ds['time'].values[1]-ds['time'].values[0]),np.timedelta64):
                                                time_step = np.timedelta64(ds['time'].values[1]-ds['time'].values[0], 'D')/ np.timedelta64(1, 'D')
                                            else:
                                                time_step = ds['time'].values[1]-ds['time'].values[0]
                                        #if 360<=time_step<=367:
                                            #print(' - Time step: ' + str(time_step) + ' days' + '\n')
                                        #else:
                                            #print(' - ERROR: the time step(' + str(time_step) + ') should be comprised between [360,367].\n')
            
                                        # test duration  (iteration = length of the coords 'time')
                                        duration_days = pd.to_timedelta(time_step * iterations,'D')
                                        duration_years = round(pd.to_numeric(duration_days.days / avgyear))
                                        #print ('duration days: ', duration_days)
                                        #print ('duration years: ', duration_years)
                                        
                                        start_exp = np.datetime_as_string(start_exp)
                                        end_exp = np.datetime_as_string(end_exp)
                                        
                                        # Dictionary item
                                        table.append([modeling_group, model, experiment, variable, iterations, units, calendar, avgyear, start_exp, end_exp, time_step, duration_years])
                                        ddi = {'experiment': experiment, 'iterations': str(iterations), 'units': units, 'calendar': calendar, 'avgyear': avgyear, 'start exp': start_exp, 'end exp':  end_exp, 'time step': str(time_step), 'duration years': str(duration_years)}
                                        #print ('ddi: ', ddi)
                                        netcdf_dict[ddi_name] = ddi
                                    else:
                                        FH1.write ('WARNING {0}: time not strictly increasing\n'.format(file))
                                else:
                                    FH1.write ('WARNING {0}: time not in datetime64 format\n'.format(file))
                            else:
                                FH1.write ('WARNING {0} time coordinate not found\n'.format(file))
                        #endif
                    except Exception as e:
                         print ('WARNING %s: exception encountered: %s' %(file, str(e)))
                         FH1.write ('WARNING {0}: exception encountered: {1}\n'.format(file, str(e)))
  
            elif os.path.isdir(os.path.join(path, file)):

                #print ('%s is a dir' %file)
                get_dir_ls (os.path.join(path, file))
 
            else:

                print ('WARNING %s is not a dir or file' %file)
                break
                    
    get_dir_ls(modeling_group_path)
    
    tabulated_table = tabulate(table, headers='firstrow', tablefmt='grid')
    #print (tabulated_table)
    FH1.write(tabulated_table)
    FH1.write('\n')

    FH1.close()
    
    #print ('type(netcdf_dict): ', type(netcdf_dict))
    #print ('netcdf_dict: ', netcdf_dict)
    with open(netcdf_dict_json_file, 'w') as outfile:
        json.dump(netcdf_dict, outfile)
    
    elapsed_time = time.time() - start_time
    print ('elapsed time: ', np.round(elapsed_time/60.0, 2), ' [min]')

if __name__ == "__main__":

    print ('sys.argv: ', sys.argv)
    main(sys.argv)
