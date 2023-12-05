#!/bin/bash -l

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

# Activate the vortex venv
#module load python/py38-anaconda-2021.05
# Activate the vortex-future env
module load gcc/11.2.0 openmpi/4.1.1 scipy-bundle
source /projects/grid/ghub/Tools/software/2023.01/python/venvs/ghubex1/bin/activate
which python

python "$@"

deactivate
exit 0
