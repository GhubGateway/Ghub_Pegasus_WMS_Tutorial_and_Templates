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

tool_alias_name=ghubex1
build_version=v1

# Activate the Python environment

module load ccrsoft/2023.01
module load gcccore/11.2.0
module load python/3.9.6
source /projects/grid/ghub/Tools/${tool_alias_name}/${build_version}/software/2023.01/python/venv/bin/activate
which python

python "$@"

deactivate
exit 0
