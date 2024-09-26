#----------------------------------------------------------------------------------------------------------------------
# Configuration parameters
#----------------------------------------------------------------------------------------------------------------------

TEMPLATE_LIST = ['Bash', 'C', 'CPP', 'Fortran', 'MATLAB', 'Python', 'R']

# Following lists are ordered by the TEMPLATE_LIST order.
# Scripts for the Bash, Python, and R templates, and source code and binary executables for the C, CPP, Fortran, and MATLAB templates,
# are stored in the tool's bin directory; for the installed and published versions of the tool, users not have read access to the tool's src directory.
SRC1_LIST = ['receive_lunch_items.sh', 'receive_lunch_items.c', 'receive_lunch_items.cpp', 'receive_lunch_items.f90', 'receive_lunch_items.m', 'receive_lunch_items.py', 'receive_lunch_items.r']
SRC2_LIST = ['consume_lunch_items.sh', 'consume_lunch_items.c', 'consume_lunch_items.cpp', 'consume_lunch_items.f90', 'consume_lunch_items.m', 'consume_lunch_items.py', 'consume_lunch_items.r']
BIN1_LIST = [None, 'receive_lunch_items', 'receive_lunch_items', 'receive_lunch_items', 'receive_lunch_items', None, None]
BIN2_LIST = [None, 'consume_lunch_items', 'consume_lunch_items', 'consume_lunch_items', 'consume_lunch_items', None, None]
JOB1_LIST = [SRC1_LIST[0], BIN1_LIST[1], BIN1_LIST[2], BIN1_LIST[3], BIN1_LIST[4], SRC1_LIST[5], SRC1_LIST[6]]
JOB2_LIST = [SRC2_LIST[0], BIN2_LIST[1], BIN2_LIST[2], BIN2_LIST[3], BIN2_LIST[4], SRC2_LIST[5], SRC2_LIST[6]]

