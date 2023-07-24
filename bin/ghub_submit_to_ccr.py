#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 10:04:26 2023

@author: renettej

"""

import getpass
import sys
import time
import os

# Current user
self_user = getpass.getuser()
# Path to current directory
self_workingdir = os.getcwd()

# Contains slurm job info
submit_info_filename = 'submit_term_out.txt'
self_log_filename = self_user + '_' + 'ismip6aissvn_log_file.txt'
self_log_filepath = os.path.join(self_workingdir, self_log_filename)
self_log_filename = self_user + '_' + 'ghub_submit_to_ccr_log_file.txt'
self_log_filepath = os.path.join(self_workingdir, self_log_filename)

estimated_time = 5

def retrieve_job_num():
    job_num = 0
    if os.path.exists(submit_info_filename):
        f = open(submit_info_filename,'r')
        for line in f:
            try:
                dets = line.split(' ')
                job_num = dets[1]
                ext = 8-len(job_num)
                for i in range(ext):
                    job_num = '0'+job_num
                return job_num
            except:
                return job_num
    return job_num

# Submit ./remotebin/pythonLaunch.sh
def submit ():
    
    if os.path.exists(submit_info_filename):
        os.remove(submit_info_filename)
    print ('\nSubmitting ../remotebin/pythonLaunch to CCR. ' +\
        'This should take approximately %d minutes...' %estimated_time)
    submit_cmd = r'submit -v ccr-ghub -w %d -i get_tiff_map.py ../remotebin/pythonLaunch.sh ./get_tiff_map.py 42.28 -78.67 42.26 42.3 -78.7 -78.64' %estimated_time + ' > ' + submit_info_filename
    print ('submit_cmd: ' + submit_cmd)
    # Submit blocks
    start_time = time.time()
    os.system(submit_cmd)
    elapsed_time = round((time.time() - start_time)/60.0, 2)
    print ('Done. Elapsed time: ' + str(elapsed_time) + ' [min]')
    job_num = retrieve_job_num()
    if job_num==0:
        print ('ERROR: job not submitted')
    else:
        #if os.path.exists(job_num + '.stdout'):        
            #os.remove(job_num + '.stdout')
        if os.path.exists(job_num + '.stderr'):
            print ('ERROR: job submitted. submit ' + job_num + '.stderr: ')
            f = open(job_num + '.stderr','r')
            for line in f:
                print (line)
            #os.remove(job_num + '.stderr')
            
def main(argv):
    
    print ('ghub_submit_to_ccr.py...')
    print ('argv: ', argv)
    
    submit()
    
if __name__ == "__main__":

    main(sys.argv)
 
           
            

