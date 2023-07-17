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

. /util/common/Lmod/lmod/lmod/init/sh
module load grass/7.2.2
# Loads 

python "$@"

