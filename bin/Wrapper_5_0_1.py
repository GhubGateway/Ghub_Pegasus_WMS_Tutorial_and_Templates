#----------------------------------------------------------------------------------------------------------------------
# Class: Wrapper
# Component of: ghub_exercise1 (github.com)
# Called from: ghub_exercise1.ipynb
# Purpose: Run a Pegasus workflow via the HUBzero hublib.cmd interface
# Author: Renette Jones-Ivey
# Date: Sept 2023
#---------------------------------------------------------------------------------------------------------------------
import sys
import os

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
    

    def __init__(self, parent, tooldir, bindir, datadir, workingdir, rundir, modeling_group, maxwalltime):

        self.parent = parent
        self.tooldir = tooldir
        self.bindir = bindir
        self.datadir = datadir
        self.workingdir = workingdir
        self.rundir = rundir
        self.modeling_group = modeling_group
        self.maxwalltime = maxwalltime

        #'''
        print('self.parent: ', self.parent)
        print('self.tooldir: ', self.tooldir)
        print('self.bindir: ', self.bindir)
        print('self.datadir: ', self.datadir)
        print('self.workingdir: ', self.workingdir)
        print('self.rundir: ', self.rundir)
        print('self.modeling_group: ', self.modeling_group)
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
            python_launch_exec_path =  os.path.join(tooldir, 'remotebin', 'pythonLaunch.sh')
            print ("python_launch_exec_path: %s" %python_launch_exec_path)
            
            pythonlaunch = Transformation(
                'pythonlaunch',
                site='local',
                pfn=python_launch_exec_path,
                is_stageable = True, #Stageable or installed
                arch=Arch.X86_64,
                os_type=OS.LINUX)

            tc.add_transformations(pythonlaunch)
            wf.add_transformation_catalog(tc)

            # All files in a Pegasus workflow are referred to in the DAX using their Logical File Name (LFN).
            # These LFNs are mapped to Physical File Names (PFNs) when Pegasus plans the workflow.
            # Add input files to the DAX-level replica catalog
            
            rc.add_replica('local', File('get_netcdf_info.py'), os.path.join(self.bindir, 'get_netcdf_info.py'))
            wf.add_replica_catalog(rc)

            # Add job(s) to the workflow
            
            pythonjob  = Job(pythonlaunch)\
                .add_args("""get_netcdf_info.py %s""" %(self.modeling_group))\
                .add_inputs(File('get_netcdf_info.py'))\
                .add_outputs(File('get_netcdf_info.txt'))\
                .add_metadata(time='%d' %self.maxwalltime)
                
            wf.add_jobs(pythonjob)
            
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
    
            '''
            submitcmd = ['submit', '--venue', 'WF-ccr-ghub', 'pegasus-plan', '--dax', 'workflow.yml']
            #print ('submitcmd: ', submitcmd)

            # submit blocks.
            exitCode,pegasusStdout,pegasusStderr = hublib.cmd.command.executeCommand(submitcmd,streamOutput=True)

            if (exitCode == 0):

                return

            else:
            
                # In this case, look for .stderr and .stdout files in the work directory
                print ('Wrapper.py: hublib.cmd.command.executeCommand(%s) returned with a non zero exit code = %d\n' %(submitcmd, exitCode))
                #self.parent.handle_wrapper_error()
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
              '''
             
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
    modeling_group = sys.argv[7]
    maxwalltime = sys.argv[8]
    
    Wrapper(parent, tooldir, bindir, datadir, workingdir, rundir, modeling_group, maxwalltime)
