#---------------------------------------------------------------------------------------------------
# launch_wrapper.py
# Component of:
#     https://github.com/GhubGateway/Ghub_Pegasus_WMS_Tutorial_and_Templates and
#     https://theghub.org/tools/ghubex1
# Called from: ghubex1.ipynb
# Also see Ghub, https://theghub.org/about
# Purpose: Plan and submit a Pegasus WMS workflow
# Author: Renette Jones-Ivey
# Date: July 2024
# Reference: https://pegasus.isi.edu/documentation
#---------------------------------------------------------------------------------------------------

import ast
import os
import sys
#from datetime import datetime

import hublib.cmd
#help (hublib.cmd.command.executeCommand)

# API for generating Pegasus YAML files
from Pegasus.api import *

# Configuration parameters
import configuration as cfg

class LaunchWrapper():
    
    def __init__(self, template_index, user, lunch_items):

        self.template_index = template_index
        self.user = user
        self.lunch_items = lunch_items
        self.maxwalltime = 30 # minutes

        #'''
        print('self.template_index: ', self.template_index)
        print('self.user: ', self.user)
        print('self.lunch_items: ', self.lunch_items)
        #'''

    def run_workflow(self):

        try:
        
            print ('LaunchWrapper.run_workflow...')
            
            template =  cfg.TEMPLATE_LIST[self.template_index]
            print ('template: %s' %template)

            jobs_dir = os.path.join(cfg.JOBS_DIR[self.template_index], template)
            print ('jobs_dir: %s' %jobs_dir)
            job1 = cfg.JOB1_LIST[self.template_index]
            print ('job1: %s' %job1)
            job2 = cfg.JOB2_LIST[self.template_index]
            print ('job2: %s' %job2)

            ########################################################################
            # Create and plan the Pegasus WMS workflow
            ########################################################################

            workflow_name = 'ghubex1_%s_launch_workflow_%s' %(template, self.user)
            print ('workflow_name: ', workflow_name)
            wf = Workflow(workflow_name)
            #print ('wf: ', wf)
    
            ########################################################################
            # Create and configure the Transformation Catalog
            ########################################################################

            tc = TransformationCatalog()
            wf.add_transformation_catalog(tc)
            
            # Add the launch script to the Transformation Catalog. The launch script is run on CCR via SLURM.
                
            tooldir = os.path.dirname(os.path.dirname(os.path.realpath(os.path.abspath(__file__))))
            print ('tooldir: ', tooldir)
            
            launch_exec_path =  os.path.join(tooldir, 'remotebin', template, '%s_Launch.sh' %template)
            print ("launch_exec_path: %s" %launch_exec_path)
            
            launch_exec = Transformation(
                '%sLaunch' %template,
                site='local',
                pfn=launch_exec_path,
                is_stageable = True, #Stageable or installed
                arch=Arch.X86_64,
                os_type=OS.LINUX,
                os_release="rhel")

            tc.add_transformations(launch_exec)
            
            ########################################################################
            # Create and configure the Replica Catalog
            ########################################################################

            # Create the f.a input file for the first workflow job
            
            fp = open('f.a','w')
            if fp:
               fp.write('{0}'.format(self.lunch_items.rstrip()))
               fp.close()
            else:
               print ("Could not create the f.a input file.\n")
               return

            rc = ReplicaCatalog()
            wf.add_replica_catalog(rc)

            # All files in a Pegasus workflow are referred to in the DAX using their Logical File Name (LFN).
            # These LFNs are mapped to Physical File Names (PFNs) when Pegasus plans the workflow.
            # Add input files to the DAX-level replica catalog
            
            rc.add_replica('local', File(job1), os.path.join(tooldir, jobs_dir, job1))
            rc.add_replica('local', File(job2), os.path.join(tooldir, jobs_dir, job2))
            rc.add_replica('local', File('f.a'), os.path.join(tooldir, 'f.a'))

            ########################################################################
            # Add jobs to the workflow
            ########################################################################

            # On Ghub, .add_outputs register_replica must be set to False (the default is True) to prevent
            # Pegasus from returning with a post script failure.
            
            workflow_job1 = Job(launch_exec)\
                .add_args("""%s %s""" %(job1, self.user))\
                .add_inputs(File(job1))\
                .add_inputs(File('f.a'))\
                .add_outputs(File('f.b'), stage_out=False, register_replica=False)\
                .add_metadata(time='%d' %self.maxwalltime)
                
            wf.add_jobs(workflow_job1)

            workflow_job2 = Job(launch_exec)\
                .add_args("""%s""" %job2)\
                .add_inputs(File(job2))\
                .add_inputs(File('f.b'))\
                .add_outputs(File('f.c'), stage_out=True, register_replica=False)\
                .add_metadata(time='%d' %self.maxwalltime)
                
            wf.add_jobs(workflow_job2)
            
            # job2 depends on job1 completing
            
            wf.add_dependency(workflow_job2, parents=[workflow_job1])

            ########################################################################
            # Create the YAML (YAML Ain't Markup Language) file
            ########################################################################

            try:
                wf.write('launch_workflow.yml')
            except PegasusClientError as e:
                print(str(e))
                return 1

            # Verify contents
            #fp = open('workflow.yml', 'r')
            #file_contents = fp.read()
            #print (file_contents)
            #fp.close()
            
            sys.stdout.flush()
            
            ########################################################################
            # Submit the Pegasus Workflow plan
            ########################################################################

            #'''
            submitcmd = ['submit', '--venue', 'WF-vortex-ghub', 'pegasus-plan', '--dax', 'launch_workflow.yml']
            #print ('submitcmd: ', submitcmd)

            # submit blocks.
            exitCode,pegasusStdout,pegasusStderr = hublib.cmd.command.executeCommand(submitcmd,streamOutput=True)

            if (exitCode == 0):

                return 0

            else:
            
                # In this case, look for .stderr and .stdout files in the work directory
                print ('Wrapper.py: hublib.cmd.command.executeCommand(%s) returned with a non zero exit code = %d\n' %(submitcmd, exitCode))
                files = os.listdir(tooldir)
                files.sort(key=lambda x: os.path.getmtime(x))
                for file in files:
                    # Get the numbered Pegasus work directory
                    #print ('type(file): ', type(file)) #<class 'str'>
                    if os.path.isfile(file) and file[0].isdigit() and file.endswith('.stderr'):
                        print ('stderr file: %s\n' %os.path.join(tooldir, file))
                        print ('For the ghubex1 tool, the following errors were returned while running a Pegasus workflow: ')
                        with open(file) as f:
                            lines = f.readlines()
                            for line in lines:
                                if 'WARNING' not in line:
                                    print (line)
                        # In case there is more than one stderr file
                        break
                return exitCode
            #'''
             
        except Exception as e:
            
            print ('LaunchWrapper Exception: %s\n' %str(e))
            return 1
