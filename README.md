## https://github.com/rljbufny1/ghub_exercise1

- Demonstrates the procedure for hosting the Github tool, ghub_exercise1, on the Ghub Science Gateway.
- Demonstrates running a Ghub Pegasus Workflow Management System (WMS) Python script workflow on University at Buffalo (UB)'s Center For Computational Research (CCR)'s generally accessible high performance compute cluster, UB-HPC.
- See https://theghub.org for more information on the Ghub Science Gateway.<br /> 
- See https://www.buffalo.edu/ccr.html for more information on CCR.<br />
- See https://pegasus.isi.edu/documentation/index.html for more information on the Pegasus WMS.<br /> 

### Requirements:

#### ghub_exercise1.ipynb

#### bin directory

This directory contains the Python and shell scripts.

#### middleware directory

This directory contains the invoke script which enables the ghub_exercise1.ipynb Jupyter Notebook to be launched on Ghub.

Note: the invoke script must have the executable file permission bits set. For example, use chmod 755 invoke to set the executable file permission bits.

### Create New Tool on Ghub:

Note: created tools are launched from the Ghub Dashboard's My Tools component.

Note: when a new tool is created you will receive an email with a link to the tool's status page. The tool's status page will allow you to let the Ghub administrators know when you are ready to update, install, approve or publish your tool.

#### Host GIT repository on Github, Gitlab

Follow the instructions on the https://theghub.org/tools/create web page. Select the Repository Host, Host GIT repository on Github, Gitlab. Select the Publishing Option, Jupyter Notebook.   Enter the name of your tool, for example, ghubex1.

#### Host subversion repository on HUB

Alernately, follow the instructions on the https://theghub.org/tools/create web page to create a new tool and select the Repository Host: Host subversion repository on HUB. Select the Publishing Option, Jupyter Notebook, and enter the name of your tool, for example, ghubex1.

In this case, the middleware/invoke script will be created automatically and stored in the subversion repository (svn) on Ghub. You will need to add ghub_exercise1.ipynb and the src and bin directory files to the svn repository.

Example svn commands:

Enter svn checkout https://theghub.org/tools/ghubex1/svn/trunk ghubex1 to checkout files from the svn repository for your tool.<br />
Enter svn add <filename> to add files to the svn repository.<br />
Enter svn commit -m "commit message" to check updates into the svn repository.<br />

### Run the Tool on Ghub for Testing after the Tool is installed:

#### Launch the Workspace 10 Tool from the Ghub Dashboard's My Tools component and in a xterm terminal window enter:<br />

```
git clone https://github.com/rljbufny1/ghub_exercise1
```
#### Launch the Jupyter Notebooks (202210) Tool from the Ghub Dashboard's My Tools component:<br />

Open ghub_exercise1/ghub_exercise1.ipynb.<br />
Click the Appmode button.<br />

