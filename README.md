# Ghub Pegasus WMS Tutorial and Templates

This Jupyter Notebook tool provides an introductory tutorial and templates for running Pegasus WMS workflows on Ghub.

The [Pegasus Workflow Management System (WMS)](https://pegasus.isi.edu) comprises software that automates and manages the execution of computational workflow jobs, including staging the jobs, distributing the work, submitting the jobs for execution, as well as handling data flow dependencies and overcoming job failures. These workflow jobs are executed on the University at Buffalo (UB)'s [Center for Computational Research (CCR)](https://www.buffalo.edu/ccr.html) high-performance compute cluster, UB-HPC, using Pegasus and submit!

This tool provides Pegasus pipeline workflow templates which associates two simple workflow jobs to create a "Hello World" demonstration of Pegasus using an abstract YAML file and a cluster submission.

This tool provides templates for workflow jobs written in the `Bash`, `C`, `CPP`, `Fortran`, `MATLAB`, `Python` and `R` programming languages. Each programming language requires a different template because the scripts to launch the `Bash`, `Python`, and `R` scripts, and the scripts to build and launch the binary executables for the `C`, `CPP`, `Fortran`, and `MATLAB` source codes, are different for each programming language. The templates' scripts and source codes provide a guideline for you to create your Pegasus WMS workflow tool on Ghub.  

This tool is published on the [Ghub Science Gateway](https://theghub.org), see [Pegasus WMS Workflows Tutorial and Templates](https://theghub.org/tools/ghubex1). You must be logged in as a Ghub member to launch this tool, see [Join Ghub](https://theghub.org/about/joining) for more information.
