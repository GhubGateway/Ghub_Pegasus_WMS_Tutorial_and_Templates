## Pegasus WMS Workflow Python Example

- Demonstrates hosting a GitHub tool on the Ghub Science Gateway and running a Ghub Pegasus Workflow Management System (WMS) workflow, comprising Python scripts, on the University at Buffalo (UB)'s Center For Computational Research (CCR)'s generally accessible high performance compute cluster, UB-HPC.
- See https://theghub.org for more information on the Ghub Science Gateway.<br /> 
- See https://www.buffalo.edu/ccr.html for more information on CCR.<br />
- See https://pegasus.isi.edu/documentation/index.html for more information on the Pegasus WMS.<br /> 

### Requirements:

#### ghubex1.ipynb

This Jupyter Notebook provides the user interface for the Pegasus WMS workflow.

#### doc directory

This directory contains the PDF file, Ghub_Pegasus_WMS_Workflow_Python_Example.pdf.

#### bin directory

This directory contains the submit wrapper script, Wrapper_5_0_1.py, used to plan the Pegasus WMS workflow. This directory also contains the Python scripts to run on CCR's high performance compute cluster.

#### remotebin directory

This directory contains the bash script, pythonLaunch.sh, used by the Pegasus WMS to launch the python scripts contained in the bin directory. A Python virtual environment was created for this tool, see pythonLaunch.sh for details. If you need assistance creating a Python virtual environment for your tool, please open a Ghub support ticket.

#### middleware directory

This directory contains the invoke script which enables the ghubex1.ipynb Jupyter Notebook to be launched on Ghub.

Note: the invoke script must have the executable file permission bits set. For example, use chmod 755 invoke to set the executable file permission bits.

### Create New Tool on Ghub:

Note: created tools are launched from the Ghub Dashboard's My Tools component.

Note: when a new tool is created you will receive an email with a link to the tool's status page. The tool's status page will allow you to let the Ghub administrators know when you are ready to update, install, approve or publish your tool.

#### Host GIT repository on Github, Gitlab

Follow the instructions on the https://theghub.org/tools/create web page.  Enter the name of your tool, for this tool, ghubex1 was entered. Select the Repository Host, Host GIT repository on Github, Gitlab. Enter the Git Repository URL, for this tool, https://github.com/GhubGateway/Ghub_Pegasus_WMS_Python_Example was entered. Select the Publishing Option, Jupyter Notebook. 


### Run the Tool on Ghub for Testing after the Tool is installed:

#### Launch the Workspace 10 Tool from the Ghub Dashboard's My Tools component and in a xterm terminal window enter:<br />

```
git clone https://github.com/GhubGateway/Ghub_Pegasus_WMS_Python_Example ghubex1
```
#### Launch the Jupyter Notebooks (202210) Tool from the Ghub Dashboard's My Tools component:<br />

Open ghubex1/ghubex1.ipynb.<br />
Click the Appmode button.<br />

