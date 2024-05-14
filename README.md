## Pegasus WMS Workflow Python Example

This Jupyter Notebook tool provides a template for running a Ghub Science Gateway Pegasus Workflow Management System (WMS) workflow, comprising Python scripts, on the University at Buffalo (UB)'s Center For Computational Research (CCR)'s generally accessible high performance compute cluster, UB-HPC.

The Ghub tool name for this template is ghubex1. The files provided by this template are specific for the ghubex1 tool. You will need to replace the files with files specific for your tool as required.

- See https://theghub.org for more information on the Ghub Science Gateway.<br /> 
- See https://www.buffalo.edu/ccr.html for more information on CCR.<br />
- See https://pegasus.isi.edu/documentation/index.html for more information on the Pegasus WMS.<br /> 

### Description of files and directories provided by this template:

#### ghubex1.ipynb

This Jupyter Notebook provides the user interface for the Pegasus WMS workflow.

#### doc directory

This directory contains the PDF file, Ghub_Pegasus_WMS_Workflow_Python_Example.pdf.

#### bin directory

This directory contains the Python scripts to run on CCR. This directory also contains the submit wrapper script, launchWrapper.py, used to plan and run the Pegasus WMS workflow jobs on CCR.

#### remotebin directory

This directory contains the bash script, pythonLaunch.sh, used by the Pegasus WMS to launch the python scripts contained in the bin directory. A Python virtual environment was created for this tool, see pythonLaunch.sh for details. If you need assistance creating a Python virtual environment for your tool, please open a Ghub support ticket.

#### middleware directory

This directory contains the invoke script which enables the ghubex1.ipynb Jupyter Notebook to be launched on Ghub.

Note: the invoke script must have the executable file permission bits set. For example, use chmod 755 invoke to set the executable file permission bits.

### Create Your Tool on Ghub:

#### Host GIT repository on HUB

Follow the instructions on the https://theGhub.org/tools/create web page.  Enter a name for your tool, for this template, ghubex1 was entered. Select the Repository Host, Host GIT repository on HUB. Select the Publishing Option, Jupyter Notebook. 

Note: when a new tool is created you will receive an email with a link to the tool's status page. The tool's status page will allow you to let the Ghub administrators know when you are ready to update, install, approve or publish your tool.

Note: published tools are launched from the Ghub Dashboard's My Tools component.

### Update Your Tool:

1) Launch the Workspace 10 Tool from the Ghub Dashboard's My Tools component and in a xterm terminal window enter:

	git clone https://github.com/GhubGateway/Ghub_Pegasus_WMS_MATLAB_Example ghubex1

	git clone https://theghub.org/tools/\<your tool name\>/git/\<your tool name\> \<your tool name\>

2) Copy template files from the ghubex1 bin and remotebin directories to your tool's bin and remotebin directories.

3) Update the launchWrapper.py script in your tool's bin directory with the script required your your tool.

4) Compare the invoke script in your tool's middleware directory with the invoke script in the ghubex1 middleware directory and update as required.


### Launch the Python Scripts for Your Tool:

1) Launch the Jupyter Notebooks (202210) tool from the Ghub Dashboard's My Tools component tool and open the \<your tool name\>/\<your tool name\>.ipynb Jupyter Notebook.

2) Update \<your tool name\>/\<your tool name\>.ipynb with the user interface required for your tool.

3) Save the notebook updates.

4) Click the Appmode button.

5) Click the Run Workflow button to launch the Python Scripts.

### Commit Your Tool Updates:

1) Enter git add to add a new file or to update an existing file.

2) Enter git commit -m "commit message"  to describe your updates.

3) Enter git push origin master to push your updates to GIT repository on Ghub.

