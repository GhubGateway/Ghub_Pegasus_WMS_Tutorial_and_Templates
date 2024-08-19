#!/bin/bash -l

#--------------------------------------------------------------------------------
# C++_Launch.sh
# Component of:
#     https://github.com/GhubGateway/Ghub_Pegasus_WMS_Tutorial_and_Templates and
#     https://theghub.org/tools/ghubex1
# Called from: a SLURM script
# Also see Ghub, https://theghub.org/about
#--------------------------------------------------------------------------------

# Echo to stdout:
echo "C++_Launch.sh: $@"

start=$(date +%s)

module load ccrsoft/2023.01
module load gcc/11.2.0

eval "$@"

end=$(date +%s)
echo "Elapsed Time: $(($end-$start)) seconds"

:
