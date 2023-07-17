#----------------------------------------------------------------------------------------------------------------------
# Class: Wrapper
# Component of: ghub_exercise1 (github.com)
# Called from: Invoked as a thread from ghub_exercise1.ipynb
# Purpose: Run a Pegasus workflow via the HUBzero hublib.cmd interface
# Author: Renette Jones-Ivey
# Date: Feb 2023
#---------------------------------------------------------------------------------------------------------------------
import sys
import os

#import Rappture
#from Rappture.tools import executeCommand as RapptureExec
# Modified for Python 2 to 3
import hublib.cmd
#help (hublib.cmd.command.executeCommand)

# API for generating Pegasus DAXes
import DAX3 as DAX3
#help (DAX3)

'''
import signal

from newthreading import Thread

def sig_handler(self, signal, frame):
    print ("\nWrapper.py thread: sig_handler signal: ", signal, "\n")
    if Thread.rapptureCommandPid < 0:
        print ("In sig_handler - Thread.rapptureCommandPid < 0\n")
    else:
        if Thread.rapptureCommandPid == 0:
            print ("In sig_handler - Thread.rapptureCommandPid == 0 (child process)\n")
        else:
            print ("In sig_handler - Thread.rapptureCommandPid > 0 (parent process)\n")
            print ("Terminating the workflow\n")
            os.kill(Thread.rapptureCommandPid, signal)
    print ("Wrapper.py thread about to sys.exit(1)")
    sys.exit(1)

# When multiprocessing is used vice threading GUI t.terminate issues a SIGTERM for this process.
signal.signal(signal.SIGHUP, sig_handler)
signal.signal(signal.SIGINT, sig_handler)
signal.signal(signal.SIGQUIT, sig_handler)
signal.signal(signal.SIGTERM, sig_handler)
'''

# Wrapper class
# Called from ghub_exercise1.ipynb
class Wrapper():
    

    def __init__(self, parent, tooldir, bindir, datadir, workingdir, rundir,
                 latitude, longitude, 
                 lat_south, lat_north, lat_west, lat_east, maxwalltime):

        self.parent = parent
        self.tooldir = tooldir
        self.bindir = bindir
        self.datadir = datadir
        self.workingdir = workingdir
        self.rundir = rundir
        self.latitude = latitude
        self.longitude = longitude
        self.lat_south = lat_south
        self.lat_north = lat_north
        self.lon_west = lon_west
        self.lon_east = lon_east
        self.maxwalltime = maxwalltime

        '''
        print('self.parent: ', self.parent)
        print('self.tooldir: ', self.tooldir)
        print('self.bindir: ', self.bindir)
        print('self.datadir: ', self.datadir)
        print('self.workingdir: ', self.workingdir)
        print('self.rundir: ', self.rundir)
        print('self.latitude: ', self.latitude)
        print('self.longitude: ', self.longitude)
        print('self.lat_south: ', self.lat_south)
        print('self.lat_north : ', self.lat_north)
        print('self.lon_west: ', self.lon_west)
        print('self.lon_east: ', self.lon_east)
        print('self.maxwalltime: ', self.maxwalltime)
        '''
        
        self.run()

    def run(self):

        try:
        
            #########################################################
            # Create the Pegasus WMS workflow
            #########################################################
    
            # Create the workflow as an abstract DAG.
    
            dax = DAX3.ADAG("ghub_exercise1-workflow")
            
            # Add MATLAB launch script to the workflow's transformation catalog.
            # Please see an example of a python launchscript in the /remotebin directory.
            
            python_launch_exec_path = os.path.join(self.tooldir, "remotebin", "pythonLaunch.sh")
            #print ("matlab_launch_exec_path : %s" %matlab_launch_exec_path)
    
            e_python_launch = DAX3.Executable(namespace="ghub_exercise1-workflow", name="python-launch", \
                os="linux", arch="x86_64", installed=False)
            e_python_launch.addPFN(DAX3.PFN("file://" + python_launch_exec_path , "local"))
            
            dax.addExecutable(e_python_launch)
            
            # Add input files to the workflow's replica catalog.
            
            # PFNs:
            # All files in a Pegasus workflow are referred to in the DAX using their Logical File Name (LFN). 
            # These LFNs are mapped to Physical File Names (PFNs) when Pegasus plans the workflow. 

            # Job 1 input, compiled matlab executable
            filename = "get_tiff_map.py"
            filepath = os.path.join(self.bindir, filename)
            get_tiff_map_py =  DAX3.File(filename)
            get_tiff_map_py.addPFN(DAX3.PFN("file://" + filepath, "local"))
            dax.addFile(get_tiff_map_py)
            
            # Job 1 output
            filename = "tiff_map_info.txt"
            filepath = os.path.join(self.workingdir, filename)
            tiff_map_info_txt =  DAX3.File(filename)
            tiff_map_info_txt.addPFN(DAX3.PFN("file://" + filepath, "local"))
            
            jobstep1 = DAX3.Job(namespace="ghub_exercise1-workflow", name="python-launch")
            jobstep1.addProfile(DAX3.Profile(DAX3.Namespace.GLOBUS,'maxwalltime', self.maxwalltime))
            jobstep1.addArguments("""./get_tiff_map %s %s %s %s""" %(self.lon_west, self.lat_south, self.lon_east, self.lat_north))
            jobstep1.uses(get_tiff_map_py, link=DAX3.Link.INPUT)
            jobstep1.uses(tiff_map_info_txt, link=DAX3.Link.OUTPUT, transfer=True)
            dax.addJob(jobstep1)
            
            #########################################################
            # Create the Pegasus Workflow DAX file
            #########################################################
    
            dax_filename = "ghub_exercise1-workflow.dax"
            dax_filepath = os.path.join(self.workingdir,dax_filename);
            fp = open(dax_filepath, "w")
            if fp:
                dax.writeXML(fp)
                fp.close()
                #print ("The daxfile %s created successfully\n" %dax_filepath)
            else:
                print ("Wrapper.py thread: Could not create the daxfile %s\n" %dax_filepath)
                #self.parent.handle_wrapper_error()
                return
    
            # Verify contents
            #fp = open("ghub_exercise1-workflow.dax", "r")
            #file_contents = fp.read()
            #print (file_contents)
            #fp.close()
            
            sys.stdout.flush()
            
            #########################################################
            # Submit the Pegasus Workflow Plan
            #########################################################
    
            #'''
            submitcmd = ["submit", "--venue", "WF-ccr-ghub", "pegasus-plan", "--dax", "ghub_exercise1-workflow.dax"]
            #print ("submitcmd: ", submitcmd)

            # submit blocks.
            exitCode,pegasusStdout,pegasusStderr = hublib.cmd.command.executeCommand(submitcmd,streamOutput=True)

            if (exitCode == 0):

                return

            else:
            
                # In this case, look for .stderr and .stdout files in the work directory
                print ("Wrapper.py: hublib.cmd.command.executeCommand(%s) returned with a non zero exit code = %d\n" %(submitcmd, exitCode))
                #self.parent.handle_wrapper_error()
                files = os.listdir(self.workingdir)
                files.sort(key=lambda x: os.path.getmtime(x))
                for file in files:
                    # Get the numbered Pegasus work directory
                    #print ('type(file): ', type(file)) #<class 'str'>
                    if os.path.isfile(file) and file[0].isdigit() and file.endswith('.stderr'):
                        print ("stderr file: %s\n" %os.path.join(self.workingdir, file))
                        print ("For the ghubex1 tool, the following errors were returned while running a Pegasus workflow: ")
                        with open(file) as f:
                            lines = f.readlines()
                            for line in lines:
                                if "WARNING" not in line:
                                    print (line)
                        # In case there is more than one stderr file in the working directory
                        break
                return

    
            #'''
            print (" ")
            
        except Exception as e:
            
            print ("Wrapper.py Exception: %s" %str(e))
            print (" ")
            
        return


#######################################################

if __name__ == "__main__":

    parent = sys.argv[1]
    tooldir = sys.argv[2]
    bindir = sys.argv[3]
    datadir = sys.argv[4]
    workingdir = sys.argv[5]
    rundir = sys.argv[6]
    latitude = sys.argv[7]
    longitude = sys.argv[8]
    lat_south = sys.argv[9]
    lat_north = sys.argv[10]
    lon_west = sys.argv[11]
    lon_east = sys.argv[12]
    maxwalltime = sys.argv[13]
    
    Wrapper(parent, tooldir, bindir, datadir, workingdir, rundir,
        latitude, longitude, 
        lat_south, lat_north, lon_west, lon_east, maxwalltime)
