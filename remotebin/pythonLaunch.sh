#!/bin/sh

commandError=0
ERROR_EXIT_CODE=1

# Verify the python files do not contain unallowed system calls
pyFiles=$(ls *.py 2> /dev/null)
#echo ${pyFiles}
for pyFile in ${pyFiles} ; do
   echo "Verifying pyFile: ${pyFile}"
   for command in system popen subprocess ; do
      commandCount=$(grep -c -E "${command}[[:space:]]*\(|${command}[[:space:]]*\.\.\." ${pyFile})
      if [ ${commandCount} -gt 0 ] ; then
         echo "The Python command ${command} is not allowed in file ${pyFile}"
         commandError=1
      fi
   done
done

if [ ${commandError} -eq 1 ] ; then
   exit ${ERROR_EXIT_CODE}
fi

# Load python module
. /util/common/Lmod/lmod/lmod/init/sh
# For initial testing only
# old CCR env:
module load python/py38-anaconda-2021.05
# new CCR env:
#module load anaconda3/2022.05
which python

rm -rf ./packages
# Note: pip dependency conflicts occur but the netcdf4 package successfully installs
python -m pip install --target=./packages netcdf4

python "$@"

exit 0
