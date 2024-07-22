#--------------------------------------------------------------------------------
# Component of:
#     https://github.com/GhubGateway/Ghub_Pegasus_WMS_Tutorial_and_Templates and
#     https://theghub.org/tools/ghubex1
# Called from: Python_Launch.sh
# Also see Ghub, https://theghub.org/about
#--------------------------------------------------------------------------------

# In the YAML file,
# this job is specified to have the f.b input file and the f.c output file

import sys

def main(argv):
    
    # f.b contains the served lunch items

    fp1 = open ('f.b', 'r');
    fp2 = open ('f.c', 'w');

    fp2.write('%sThank you for lunch. Yum Yum!!\n' %fp1.readline());
    
    fp1.close()
    fp2.close()

    # f.c contains the thank you note

if __name__ == "__main__":

    main(sys.argv)
