#----------------------------------------------------------------------------------------------------------------------
# Class: Wrapper_5.0.1
# Component of: ghub_exercise1 (github.com)
# Called from: ghub_exercise1.ipynb
# Purpose: Run a Pegasus WMS 5.0.1 workflow via the HUBzero hublib.cmd interface
# Author: Renette Jones-Ivey
# Date: Sept 2023
#---------------------------------------------------------------------------------------------------------------------

import ast
import os
import sys

#import Rappture
#from Rappture.tools import executeCommand as RapptureExec
# Modified for Python 2 to 3
import hublib.cmd
#help (hublib.cmd.command.executeCommand)

# API for generating Pegasus YML files
from Pegasus.api import *

# Wrapper class
# Called from ghub_exercise1.ipynb
class Wrapper():
    

    def __init__(self, parent, tooldir, bindir, datadir, workingdir, rundir, ice_sheet_folder, ice_sheet_description, modeling_groups, maxwalltime):

        self.parent = parent
        self.tooldir = tooldir
        self.bindir = bindir
        self.datadir = datadir
        self.workingdir = workingdir
        self.rundir = rundir
        self.ice_sheet_folder = ice_sheet_folder
        self.ice_sheet = ice_sheet_folder.split('/')[-1]
        self.ice_sheet_description = ice_sheet_description
        self.modeling_groups = modeling_groups
        self.maxwalltime = maxwalltime

        #'''
        print('self.parent: ', self.parent)
        print('self.tooldir: ', self.tooldir)
        print('self.bindir: ', self.bindir)
        print('self.datadir: ', self.datadir)
        print('self.workingdir: ', self.workingdir)
        print('self.rundir: ', self.rundir)
        print('self.ice_sheet_folder: ', self.ice_sheet_folder)
        print('self.ice_sheet: ', self.ice_sheet)
        print('self.ice_sheet_description: ', self.ice_sheet_description)
        print('self.modeling_groups: ', self.modeling_groups)
        print('self.maxwalltime: ', self.maxwalltime)
        #'''
        
        self.run()

    def run(self):

        try:

            #########################################################
            # Create the Pegasus WMS workflow
            #########################################################
            print ('Wrapper_5_0_1...')
    
            wf = Workflow('ghub_exercise1-workflow')
            tc = TransformationCatalog()
            rc = ReplicaCatalog()

            # Add python launch script to the transformation catalog
                
            tooldir = os.path.dirname(os.path.dirname(os.path.realpath(os.path.abspath(__file__))))
            print ('tooldir: ', tooldir)
            python_launch_exec_path =  os.path.join(tooldir, 'remotebin', 'pythonLaunch.sh')
            print ("python_launch_exec_path: %s" %python_launch_exec_path)
            
            pythonlaunch = Transformation(
                'pythonlaunch',
                site='local',
                pfn=python_launch_exec_path,
                is_stageable = True, #Stageable or installed
                arch=Arch.X86_64,
                os_type=OS.LINUX,
                os_release="rhel")

            tc.add_transformations(pythonlaunch)
            wf.add_transformation_catalog(tc)

            # All files in a Pegasus workflow are referred to in the DAX using their Logical File Name (LFN).
            # These LFNs are mapped to Physical File Names (PFNs) when Pegasus plans the workflow.
            # Add input files to the DAX-level replica catalog
            
            rc.add_replica('local', File('get_netcdf_info.py'), os.path.join(self.bindir, 'get_netcdf_info.py'))
            rc.add_replica('local', File('process_netcdf_info.py'), os.path.join(self.bindir, 'process_netcdf_info.py'))
            wf.add_replica_catalog(rc)

            # Add job(s) to the workflow

            modeling_groups_list = list(self.modeling_groups.split(','))
            print ('modeling_groups_list: ', modeling_groups_list)
            #print ('type(self.modeling_groups_list): ', type(modeling_groups_list))
            #print('len(modeling_groups_list): ', len(modeling_groups_list))

            
            file_basename_list = []
            get_netcdf_info_job_list = []

            for i in range(len(modeling_groups_list)):
            
                modeling_group  = modeling_groups_list[i]
                #print ('modeling_group: ', modeling_group)
                modeling_group_path = os.path.join(self.ice_sheet_folder, modeling_group)
                #print ('modeling_group_path: ', modeling_group_path)
                file_basename = '_'.join(modeling_group_path.split('/')[-2:])
                #print ('file_basename: ', file_basename)
                file_basename_list.append(file_basename)

                # Note: on Ghub, .add_outputs register_replica must be set to False (the default is True) to prevent
                # Pegasus from returning with a post script failure.
                
                get_netcdf_info_job = Job(pythonlaunch)\
                    .add_args("""get_netcdf_info.py %s""" %(modeling_group_path))\
                    .add_inputs(File('get_netcdf_info.py'))\
                    .add_outputs(File('%s_netcdf_info.txt' %file_basename), stage_out=True, register_replica=False)\
                    .add_outputs(File('%s_netcdf_info.json' %file_basename), stage_out=False, register_replica=False)\
                    .add_metadata(time='%d' %self.maxwalltime)
                    
                wf.add_jobs(get_netcdf_info_job)
                get_netcdf_info_job_list.append (get_netcdf_info_job)

            process_netcdf_info_job = Job(pythonlaunch)\
                .add_args('''process_netcdf_info.py %s %s %s''' %(self.ice_sheet_folder, self.ice_sheet_description, self.modeling_groups))\
                .add_inputs(File('process_netcdf_info.py'))\
                .add_outputs(File('%s_processed_netcdf_info.txt' %self.ice_sheet), stage_out=True, register_replica=False)\
                .add_metadata(time='%d' %self.maxwalltime)
                
            for i in range(len(modeling_groups_list)):
                process_netcdf_info_job.add_inputs(File('%s_netcdf_info.json' %file_basename_list[i]), bypass_staging=True)
                
            wf.add_jobs(process_netcdf_info_job)
            
            # process_netcdf_info_job depends on all the get_netcdf_info_jobs completing
            
            wf.add_dependency(process_netcdf_info_job, parents=get_netcdf_info_job_list)

            #########################################################
            # Create the Pegasus Workflow YML file
            #########################################################
    
            # Create the YML file
            try:
                wf.write()
            except PegasusClientError as e:
                print(e)

            # Verify contents
            #fp = open('workflow.yml', 'r')
            #file_contents = fp.read()
            #print (file_contents)
            #fp.close()
            
            sys.stdout.flush()
            
            #########################################################
            # Submit the Pegasus Workflow Plan
            #########################################################
    
            #'''
            submitcmd = ['submit', '--venue', 'WF-ccr-ghub', 'pegasus-plan', '--dax', 'workflow.yml']
            #print ('submitcmd: ', submitcmd)

            # submit blocks.
            exitCode,pegasusStdout,pegasusStderr = hublib.cmd.command.executeCommand(submitcmd,streamOutput=True)

            if (exitCode == 0):

                return

            else:
            
                # In this case, look for .stderr and .stdout files in the work directory
                print ('Wrapper.py: hublib.cmd.command.executeCommand(%s) returned with a non zero exit code = %d\n' %(submitcmd, exitCode))
                files = os.listdir(self.workingdir)
                files.sort(key=lambda x: os.path.getmtime(x))
                for file in files:
                    # Get the numbered Pegasus work directory
                    #print ('type(file): ', type(file)) #<class 'str'>
                    if os.path.isfile(file) and file[0].isdigit() and file.endswith('.stderr'):
                        print ('stderr file: %s\n' %os.path.join(self.workingdir, file))
                        print ('For the ghubex1 tool, the following errors were returned while running a Pegasus workflow: ')
                        with open(file) as f:
                            lines = f.readlines()
                            for line in lines:
                                if 'WARNING' not in line:
                                    print (line)
                        # In case there is more than one stderr file in the working directory
                        break
                return
              #'''
             
        except Exception as e:
            
            print ('Wrapper.py Exception: %s\n' %str(e))
            
        return


#######################################################

if __name__ == '__main__':

    print ('sys.argv: ', sys.argv)

    parent = sys.argv[1]
    tooldir = sys.argv[2]
    bindir = sys.argv[3]
    datadir = sys.argv[4]
    workingdir = sys.argv[5]
    rundir = sys.argv[6]
    ice_sheet_folder = sys.argv[7]
    ice_sheet_description = sys.argv[8]
    modeling_groups = sys.argv[9]
    maxwalltime = sys.argv[10]
    
    Wrapper(parent, tooldir, bindir, datadir, workingdir, rundir, ice_sheet_folder, ice_sheet_description, modeling_groups, maxwalltime)
