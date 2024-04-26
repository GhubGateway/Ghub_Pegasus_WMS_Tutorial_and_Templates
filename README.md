## Pegasus WMS Workflow Python Example

This Jupyter Notebook tool privides a termplate for hosting a GitHub tool on the GHub Science Gateway and running a GHub Pegasus Workflow Management System (WMS) workflow, comprising Python scripts, on the University at Buffalo (UB)'s Center For Computational Research (CCR)'s generally accessible high performance compute cluster, UB-HPC.

The GHub tool name for this template is ghubex1. The files provided by this template are specific for the ghubex1 tool. You will need to replace the files with files specific for your tool as required.

- See https://theghub.org for more information on the GHub Science Gateway.<br /> 
- See https://www.buffalo.edu/ccr.html for more information on CCR.<br />
- See https://pegasus.isi.edu/documentation/index.html for more information on the Pegasus WMS.<br /> 

### Description of files and directories provided by this template:

#### ghubex1.ipynb

This Jupyter Notebook provides the user interface for the Pegasus WMS workflow.

#### doc directory

This directory contains the PDF file, Ghub_Pegasus_WMS_Workflow_Python_Example.pdf.

#### bin directory

This directory contains the Python scripts to run on CCR. This directory also contains the submit wrapper script, launchWrapper.py, used to plan run the Pegasus WMS workflow jobs on CCR.

#### remotebin directory

This directory contains the bash script, pythonLaunch.sh, used by the Pegasus WMS to launch the python scripts contained in the bin directory. A Python virtual environment was created for this tool, see pythonLaunch.sh for details. If you need assistance creating a Python virtual environment for your tool, please open a GHub support ticket.

#### middleware directory

This directory contains the invoke script which enables the ghubex1.ipynb Jupyter Notebook to be launched on GHub.

Note: the invoke script must have the executable file permission bits set. For example, use chmod 755 invoke to set the executable file permission bits.

### Create New Tool on GHub:

#### Host GIT repository on Github, Gitlab

Follow the instructions on the https://theghub.org/tools/create web page.  Enter the name of your tool, for this tool, ghubex1 was entered. Select the Repository Host, Host GIT repository on Github, Gitlab. Enter the Git Repository URL, for this tool, https://github.com/GhubGateway/Ghub_Pegasus_WMS_Python_Example was entered. Select the Publishing Option, Jupyter Notebook. 

Note: when a new tool is created you will receive an email with a link to the tool's status page. The tool's status page will allow you to let the GHub administrators know when you are ready to update, install, approve or publish your tool.

Note: published tools are launched from the GHub Dashboard's My Tools component.

### Update Your Tool:

1) Launch the Workspace 10 Tool from the GHub Dashboard's My Tools component and in a xterm terminal window enter:

	git clone https://github.com/GhubGateway/Ghub_Pegasus_WMS_Pytrhon_Example ghubex1

	git clone https://theghub.org/tools/\<your tool alias name\>/git/\<your tool alias name\> \<your tool alias name\>

2) Copy ghubex1 template files to your tool's src, bin and remotebin directories as required.

3) Update / replace the files in your tool's src, bin and remotebin directories with files specific for your tool as required.

#### Launch the Python scripts for Your Tool:

1) Update the launchWrapper.py in your tool's bin directory and the pythonLaunch.sh script in your tool's remotebin directory with the scripts required your your tool.
2) Launch the Jupyter Notebooks (202210) tool from the GHub Dashboard's My Tools component tool and open the \<your tool alias name\>/\<your tool alias name\>.ipynb Jupyter Notebook.
3) Update \<your tool alias name\>/\<your tool alias name\>.ipynb with the user interface required for your tool.
4) Save the notebook updates.
5) Click the Appmode button.
6) Click the Run Workflow button to launch the MATLAB executables.
