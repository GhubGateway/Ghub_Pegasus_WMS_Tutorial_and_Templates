#----------------------------------------------------------------------------------------------------------------------
# Component of: Ghub_Pegasus_WMS_Python_Example (github.com)
# Called from: pythonLaunch.sh
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

# check motonocity of a list (used to check time series)
def strictly_increasing(L):
    return all(x<y for x, y in zip(L, L[1:]))

def main(argv):
    
    print ('get_netcdf_info...')
    print ('argv: ', argv)
    
    start_time = time.time()
    
    # Process files in ISMIP6 directories
    
    modeling_group_path = argv[1]
    print ('modeling_group_path: ', modeling_group_path)

    # See the isschecker tool data/smip6_criteria.csv.
    recognized_variables = ['acabf', 'base', 'libmassbffl', 'libmassbfgr', 'lithk', 'orog', 'sftflf', 'sftgif', 'sftgrf', 'strbasemag', 'topg', 'xvelmean', 'yvelmean']
    #print ('recognized_variables: ', recognized_variables)
    
    file_basename = '_'.join(modeling_group_path.split('/')[-2:])
    print ('file_basename: ', file_basename)
    
    FH1 = open('%s_netcdf_info.txt' %file_basename, 'w')
    
    print ('Modeling Group Path: ', modeling_group_path)
    FH1.write('\nModeling Group Path: {0}\n\n'.format(modeling_group_path))
    
    table = [['Group', 'Model', 'Experiment', 'Variable', 'Keys', 'Dims', 'Coords', 'Resolution', 'Units', 'Calendar', 'Start', 'End', 'Time Step', 'Years']]

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
                            #if str.isnumeric(experiment_split[-1]):
                                # Remove the resolution from the model name
                                #experiment = '_'.join(experiment_split[:-1])
                            #print ('experiment ', experiment)
                            ddi_name = '_'.join([ice_sheet, modeling_group, model, experiment, variable])
                            #print ('ddi_name: ', ddi_name)
    
                            # Reference: https://docs.xarray.dev/en/stable/user-guide/data-structures.html#dataset-contents
                            #print (type(ds)) #<class 'xarray.core.dataset.Dataset'>
                            #print ('type(ds.values()): ', type(ds.values())) #<class 'collections.abc.ValuesView'>
                            #print ('ds.values(): ', ds.values())

                            # Get the undecoded times.
                            # By default, xarray decodes the time values and in this case,
                            # the units and calendar attributes are consumed into the returned time values
                            ds = xr.open_dataset(os.path.join(path,file), decode_times=False)
                            
                            #data_vars = list(ds.data_vars)
                            #print ('data_vars: ', data_vars)

                            # To str to account for any inhomogeneity
                            keys = str(list(ds.keys()))
                            #print ('keys: ', keys)
                            
                            # To str to account for any inhomogeneity
                            dims = str(list(ds.dims))
                            #print ('dims: ', dims)

                            # To str to account for any inhomogeneity
                            coords = str(list(ds.coords))
                            #print ('coords: ', coords)
                            
                            try:
                                x = ds['x'].values
                            except Exception as e:
                                try:
                                    x = ds['lon'].values
                                except Exception as e:
                                    x = []
                            if len(x) > 1:
                                xres = round(x[1] - x[0])
                            else:
                                xres = 'Unknown'
                            try:
                                y = ds['y'].values
                            except Exception as e:
                                try:
                                    y = ds['lat'].values
                                except Exception as e:
                                    y = []
                            if len(y) > 1:
                                yres = round(y[1] - y[0])
                            else:
                                yres = 'Unknown'
                            resolution = str(list((xres, yres)))
                            #print ('resolution: ', resolution)

                            try:
                                time = ds['time'].values
                            except Exception as e:
                                time = []
                            #print ("type(time): ", type(time))
                            #print ('len(time): ', len(time))
                            #print ('time: ', time)
                            
                            units = 'Unknown'
                            calendar = 'Unknown'
                            start_exp = 'Unknown'
                            end_exp = 'Unknown'
                            time_step = str(0)
                            duration_years = str(0)

                            if len(time) > 0:

                                if 'units' in ds['time'].attrs:
                                    units = ds['time'].attrs['units']
                                #print ('units: ', units)
                                
                                if 'calendar' in ds['time'].attrs:
                                    calendar = ds['time'].attrs['calendar']
                                #print ('calendar: ', calendar)
                                
                                # Get the decoded times:
                                ds = xr.open_dataset(os.path.join(path,file))
                            
                                time = ds['time'].values
                                #print ("type(time): ", type(time))
                                #print ('len(time): ', len(time))
                                #print ('time: ', time)

                                start_exp = min(ds['time']).values.astype('datetime64[D]')
                                #print ('type(start_exp): ', type(start_exp)) #<class 'numpy.ndarray'>
                                #print ('start_exp: ', start_exp)
                                end_exp  = max(ds['time']).values.astype('datetime64[D]')
                                #print ('type(end_exp): ', type(end_exp)) #<class 'numpy.ndarray'>
                                #print ('end_exp: ', end_exp)
                                avgyear = 365        # pedants definition of a year length with leap years
                                calendar_split = calendar.split('_')
                                if len(calendar_split) == 2 and calendar_split[1] == 'day':
                                   avgyear = int(calendar_split[0])
                                #print ('avgyear: ', avgyear)
                                duration_days = (end_exp - start_exp)
                                duration_years =  str(duration_days.astype('timedelta64[Y]')/np.timedelta64(1,'Y'))
                                #print ('duration days: ', duration_days)
                                #print ('duration years: ', duration_years)
                                
                                iterations = len(time)
                                #print ('iterations: ', iterations)

                                if iterations > 1:
                            
                                    if np.issubdtype(start_exp.dtype, np.datetime64) & np.issubdtype(end_exp.dtype, np.datetime64):
                                        
                                        start_exp = np.datetime_as_string(start_exp)
                                        #print ('type(start_exp): ', type(start_exp)) #<class 'numpy.str_'>
                                        #print ('start_exp: ', start_exp)
                                        end_exp = np.datetime_as_string(end_exp)
                                        #print ('type(end_exp): ', type(end_exp)) #<class 'numpy.str_'>
                                        #print ('end_exp: ', end_exp)

                                        if strictly_increasing(time):
                                            time_delta = time[1]-time[0]
                                            if isinstance(time_delta,datetime.timedelta):
                                                time_step = (time_delta.days)
                                            else:
                                                if isinstance(time_delta,np.timedelta64):
                                                    time_step = np.timedelta64(time_delta, 'D') / np.timedelta64(1, 'D')
                                                else:
                                                    time_step = time_delta

                                            #if 360<=time_step<=367:
                                                #print(' - Time step: ' + str(time_step) + ' days' + '\n')
                                            #else:
                                                #print(' - ERROR: the time step(' + str(time_step) + ') should be comprised between [360,367].\n')
                
                                            # test duration  (iteration = length of the coords 'time')
                                            duration_days = pd.to_timedelta(time_step * iterations,'D')
                                            duration_years = str(round(pd.to_numeric(duration_days.days / avgyear)))
                                            # To str to prevent object is not JSON serializable error
                                            time_step = str(time_step)
                                            #print ('duration days: ', duration_days)
                                            #print ('duration years: ', duration_years)
                                            
                                        else:
                                            FH1.write ('WARNING {0}: time not strictly increasing\n'.format(file))
                                    else:
                                        FH1.write ('WARNING {0}: time not in datetime64 format\n'.format(file))
                                        # To str to prevent object is not JSON serializable error
                                        start_exp = str(start_exp.tolist())
                                        end_exp = str(end_exp.tolist())
                                else:
                                    FH1.write ('WARNING {0}: contains {1} time value(s)\n'.format(file, iterations))
                                    # To str to prevent object is not JSON serializable error
                                    start_exp = str(start_exp.tolist())
                                    end_exp = str(end_exp.tolist())
                                    
                            else:
                                FH1.write ('WARNING {0} time not found\n'.format(file))
                                
                            # Dictionary item
                            #print ('ddi_name: ', ddi_name)
                            table.append([modeling_group, model, experiment, variable, keys, dims, coords, resolution, units, calendar, start_exp, end_exp, time_step, duration_years])
                            #ddi = {'experiment': experiment, 'keys': keys, 'dims': dims, 'coords': coords, 'resolution': resolution, 'units': units, 'calendar': calendar, \
                                #'start exp': start_exp, 'end exp':  end_exp, 'time step': time_step, 'duration years': duration_years}
                            ddi = {'experiment': experiment, 'keys': keys, 'dims': dims, 'coords': coords, 'resolution': resolution, \
                                'units': units, 'calendar': calendar, 'start exp': start_exp, 'end exp':  end_exp, 'time step': time_step, 'duration years': duration_years}
                            #print ('ddi: ', ddi)
                            netcdf_dict[ddi_name] = ddi
                                
                        #endif variable in recognized_variables
                        
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
