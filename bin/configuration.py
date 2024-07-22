#----------------------------------------------------------------------------------------------------------------------
# Configuration parameters
#----------------------------------------------------------------------------------------------------------------------

TEMPLATE_LIST = ['Bash', 'MATLAB', 'Python']

# Following lists are ordered by the TEMPLATE_LIST order:
SRC1_LIST = ['receive_lunch_items.sh', 'receive_lunch_items.m', 'receive_lunch_items.py']
SRC2_LIST = ['consume_lunch_items.sh', 'consume_lunch_items.m', 'consume_lunch_items.py']
BIN1_LIST = [None, 'receive_lunch_items', None]
BIN2_LIST = [None, 'consume_lunch_items', None]
JOBS_DIR = ['src', 'bin', 'src']
JOB1_LIST = [SRC1_LIST[0], BIN1_LIST[1], SRC1_LIST[2]]
JOB2_LIST = [SRC2_LIST[0], BIN2_LIST[1], SRC2_LIST[2]]

