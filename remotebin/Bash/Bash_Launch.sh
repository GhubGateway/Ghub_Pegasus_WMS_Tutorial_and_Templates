#!/bin/bash -l

#--------------------------------------------------------------------------------
# Bash_Launch.sh
# Component of:
#     https://github.com/GhubGateway/Ghub_Pegasus_WMS_Tutorial_and_Templates and
#     https://theghub.org/tools/ghubex1
# Called from: a SLURM script
# Also see Ghub, https://theghub.org/about
#--------------------------------------------------------------------------------

# Echo to stdout:
echo "Bash_Launch.sh: $@"

start=$(date +%s)

module load ccrsoft/2023.01

bash "$@"

end=$(date +%s)
echo "Elapsed Time: $(($end-$start)) seconds"

exit 0
