#!/bin/bash -l

#--------------------------------------------------------------------------------
# CPP_Build.sh
# Component of:
#     https://github.com/GhubGateway/Ghub_Pegasus_WMS_Tutorial_and_Templates and
#     https://theghub.org/tools/ghubex1
# Called from: a SLURM script
# Also see Ghub, https://theghub.org/about
#--------------------------------------------------------------------------------

# Echo to stdout:
echo "CPP_Build.sh"

start=$(date +%s)

module load ccrsoft/2023.01
module load gcc/11.2.0

# gcc creates C++ executables to run on a platform corresponding to the platform on which they are generated.

gcc=$(which gcc)
echo 'gcc: '${gcc}

# -v: verbose
# -o: output file

${gcc} -lstdc++ -v ./receive_lunch_items.cpp -o receive_lunch_items
${gcc} -lstdc++ -v ./consume_lunch_items.cpp -o consume_lunch_items

end=$(date +%s)
echo "Elapsed Time: $(($end-$start)) seconds"

:
