**Detector** is a complete machine learning workflow commands to perform an ensemble anomaly detection methoology. It's has a command line tool that interacts with the associated Snowflake database and multiple scripts to estimate anomaly probabilities, ranging from data collection to updating outputs to snowflake, passing by the creation of client / ticket features and modeling.   

The key features are:

#. Interact with Snowflake databases and **collect data** according to the used defined date window and table name.

#. **Build features** by aggregating raw data by client or ticket.

#. **Train and optimize** different anomaaly detection models and using *bayesian* optimization routine.

#. Estimate **anomaly probabilities** using developed models and **push** result back to Snowflake.

**Detector** aims to automatically assign risk probabilites to client or ticket according certain period and push the results
to Snwoflake.

.. contents:: **Contents**
:backlinks: none

How Detector works
=============

Detector We encourage you to read our `Get Started <https://dvc.org/doc/get-started>`_ guide to better understand what DVC
is and how it can fit your scenarios.

The easiest (but not perfect!) *analogy* to describe it: DVC is Git (or Git-LFS to be precise) & Makefiles
made right and tailored specifically for ML and Data Science scenarios.

#. ``Git/Git-LFS`` part - DVC helps store and share data artifacts and models, connecting them with a Git repository.
#. ``Makefile``\ s part - DVC describes how one data or model artifact was built from other data and code.

DVC usually runs along with Git. Git is used as usual to store and version code (including DVC meta-files). DVC helps
to store data and model files seamlessly out of Git, while preserving almost the same user experience as if they
were stored in Git itself. To store and share the data cache, DVC supports multiple remotes - any cloud (S3, Azure,
Google Cloud, etc) or any on-premise network storage (via SSH, for example).

|Flowchart|

The DVC pipelines (computational graph) feature connects code and data together. It is possible to explicitly
specify all steps required to produce a model: input dependencies including data, commands to run,
and output information to be saved. See the quick start section below or
the `Get Started <https://dvc.org/doc/get-started>`_ tutorial to learn more.

```
Usage: stronghold.py [OPTIONS]

  Securely configure your Mac.
  Developed by Aaron Lichtman -> (Github: alichtman)


Options:
  -lockdown  Set secure configuration without user interaction.
  -v         Display version and author information and exit.
  -help, -h  Show this message and exit.
```




Usage
===========

Common workflow commands include:

+-----------------------------------+-------------------------------------------------------------------+
| Step                              | Command                                                           |
+===================================+===================================================================+
| Load data                         | | ``$ detector load --table-name --end-date --nmonth --storage``  |
|                                   | | ``$ detector load --help``                                      |
+-----------------------------------+-------------------------------------------------------------------+
| Build features                    | | ``$ detector build --table-name --end-date --nmonth --type-features --storage``|
|                                   | | ``$ detector build --help`` |
+-----------------------------------+-------------------------------------------------------------------+
| Train models                      | | ``$ detector train --table-name --end-date --nmonth --type-features --storage`` |
|                                   | | ``$ detector build --help``                                     |
+-----------------------------------+-------------------------------------------------------------------+
| Predict data                      | | ``$ detector predict --table-name --end-date --nmonth --type-features --storage``|
|                                   | | ``$ detector predict --help``                                   |
+-----------------------------------+-------------------------------------------------------------------+
| Push data                         | | ``$ dvc remote add myremote -d s3://mybucket/image_cnn``        |
|                                   | | ``$ dvc push``                                                  |
+-----------------------------------+-------------------------------------------------------------------+
| Run                               | | ``$ dvc remote add myremote -d s3://mybucket/image_cnn``        |
|                                   | | ``$ dvc push``                                                  |
+-----------------------------------+-------------------------------------------------------------------+

Installation
============

There are four options to install DVC: ``pip``, Homebrew, Conda (Anaconda) or an OS-specific package.
Full instructions are `available here <https://dvc.org/doc/get-started/install>`_.

pip (PyPI)
----------

|PyPI|

.. code-block:: bash

   pip install dvc

Depending on the remote storage type you plan to use to keep and share your data, you might need to specify
one of the optional dependencies: ``s3``, ``gs``, ``azure``, ``oss``, ``ssh``. Or ``all`` to include them all.
The command should look like this: ``pip install dvc[s3]`` (in this case AWS S3 dependencies such as ``boto3``
will be installed automatically).

To install the development version, run:

.. code-block:: bash

   pip install git+git://github.com/iterative/dvc

Package
-------

|Packages|

Self-contained packages for Linux, Windows, and Mac are available. The latest version of the packages
can be found on the GitHub `releases page <https://github.com/iterative/dvc/releases>`_.

Ubuntu / Debian (deb)
^^^^^^^^^^^^^^^^^^^^^
.. code-block:: bash

   sudo wget https://dvc.org/deb/dvc.list -O /etc/apt/sources.list.d/dvc.list
   sudo apt-get update
   sudo apt-get install dvc

Fedora / CentOS (rpm)
^^^^^^^^^^^^^^^^^^^^^
.. code-block:: bash

   sudo wget https://dvc.org/rpm/dvc.repo -O /etc/yum.repos.d/dvc.repo
   sudo yum update
   sudo yum install dvc

Disclaimer
============
Detector's suite of algorithms aims at identifying possible events that deviate significantly from global observed events.
In this sense, detector provides a level of risk of possible anomalies,
but does not detect anomalies or fraud events with certainty.

As specified in its general rules of intervention, KPMG cannot be held responsible for decisions made on the basis of proposals or predictions made by detector.
