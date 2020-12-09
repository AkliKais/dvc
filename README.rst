|Banner|

|Release| |CI| |Maintainability| |Coverage| |Donate| |DOI|

|PyPI| |Packages| |Brew| |Conda| |Choco| |Snap|

**Detector** is a complete machine learning workflow commands to perform an ensemble anomaly detection methoology. It's has a command line tool that interacts with the associated Snowflake database and multiple scripts to estimate anomaly probabilities, ranging from data collection to updating outputs to snowflake, passing by the creation of client / ticket features and modeling.   

The Key features are:

#. Interact with Snowflake databases and **Collect data** according to the used defined date window and table name.

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
| Load data                         | | ``$ detector load --help``                                      |
|                                   | | ``$ detector load --help``                                      |
+-----------------------------------+-------------------------------------------------------------------+
| Build features                    | | ``$ detector build --help``                                     |
|                                   | | ``$ dvc run -d images/ -d train.py -o model.p python train.py`` |
+-----------------------------------+-------------------------------------------------------------------+
| Train models                      | | ``$ vi train.py``                                               |
|                                   | | ``$ dvc repro model.p.dvc``                                     |
+-----------------------------------+-------------------------------------------------------------------+
| Predict data                      | | ``$ git add .``                                                 |
|                                   | | ``$ git commit -m 'The baseline model'``                        |
|                                   | | ``$ git push``                                                  |
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

Snap (Snapcraft/Linux)
----------------------

|Snap|

.. code-block:: bash

   snap install dvc --classic

This corresponds to the latest tagged release.
Add ``--beta`` for the latest tagged release candidate,
or ``--edge`` for the latest ``master`` version.

Choco (Chocolatey/Windows)
--------------------------

|Choco|

.. code-block:: bash

   choco install dvc

Brew (Homebrew/Mac OS)
----------------------

|Brew|

.. code-block:: bash

   brew install dvc

Conda (Anaconda)
----------------

|Conda|

.. code-block:: bash

   conda install -c conda-forge dvc

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

Comparison to related technologies
==================================

#. `Git-annex <https://git-annex.branchable.com/>`_ - DVC uses the idea of storing the content of large files (which should
   not be in a Git repository) in a local key-value store, and uses file hardlinks/symlinks instead of
   copying/duplicating files.

#. `Git-LFS <https://git-lfs.github.com/>`_ - DVC is compatible with any remote storage (S3, Google Cloud, Azure, SSH,
   etc). DVC also uses reflinks or hardlinks to avoid copy operations on checkouts; thus handling large data files
   much more efficiently.

#. *Makefile* (and analogues including ad-hoc scripts) - DVC tracks dependencies (in a directed acyclic graph).

#. `Workflow Management Systems <https://en.wikipedia.org/wiki/Workflow_management_system>`_ - DVC is a workflow
   management system designed specifically to manage machine learning experiments. DVC is built on top of Git.

#. `DAGsHub <https://dagshub.com/>`_ - This is a Github equivalent for DVC. Pushing Git+DVC based repositories to DAGsHub will produce in a high level project dashboard; including DVC pipelines and metrics visualizations, as well as links to any DVC-managed files present in cloud storage.

Disclaimer
============
Detector's suite of algorithms aims at identifying possible events that deviate significantly from global observed events.
In this sense, detector provides a level of risk of possible anomalies,
but does not detect anomalies or fraud events with certainty.

As specified in its general rules of intervention, KPMG cannot be held responsible for decisions made on the basis of proposals or predictions made by detector.

|Maintainability| |Donate|

Contributions are welcome! Please see our `Contributing Guide <https://dvc.org/doc/user-guide/contributing/core>`_ for more
details.

.. image:: https://sourcerer.io/fame/efiop/iterative/dvc/images/0
   :target: https://sourcerer.io/fame/efiop/iterative/dvc/links/0
   :alt: 0

.. image:: https://sourcerer.io/fame/efiop/iterative/dvc/images/1
   :target: https://sourcerer.io/fame/efiop/iterative/dvc/links/1
   :alt: 1

.. image:: https://sourcerer.io/fame/efiop/iterative/dvc/images/2
   :target: https://sourcerer.io/fame/efiop/iterative/dvc/links/2
   :alt: 2

.. image:: https://sourcerer.io/fame/efiop/iterative/dvc/images/3
   :target: https://sourcerer.io/fame/efiop/iterative/dvc/links/3
   :alt: 3

.. image:: https://sourcerer.io/fame/efiop/iterative/dvc/images/4
   :target: https://sourcerer.io/fame/efiop/iterative/dvc/links/4
   :alt: 4

.. image:: https://sourcerer.io/fame/efiop/iterative/dvc/images/5
   :target: https://sourcerer.io/fame/efiop/iterative/dvc/links/5
   :alt: 5

.. image:: https://sourcerer.io/fame/efiop/iterative/dvc/images/6
   :target: https://sourcerer.io/fame/efiop/iterative/dvc/links/6
   :alt: 6

.. image:: https://sourcerer.io/fame/efiop/iterative/dvc/images/7
   :target: https://sourcerer.io/fame/efiop/iterative/dvc/links/7
   :alt: 7

Mailing List
============

Want to stay up to date? Want to help improve DVC by participating in our occasional polls? Subscribe to our `mailing list <https://sweedom.us10.list-manage.com/subscribe/post?u=a08bf93caae4063c4e6a351f6&id=24c0ecc49a>`_. No spam, really low traffic.

Copyright
=========

This project is distributed under the Apache license version 2.0 (see the LICENSE file in the project root).

By submitting a pull request to this project, you agree to license your contribution under the Apache license version
2.0 to this project.

Citation
========

|DOI|

Iterative, *DVC: Data Version Control - Git for Data & Models* (2020)
`DOI:10.5281/zenodo.012345 <https://doi.org/10.5281/zenodo.3677553>`_.

.. |Banner| image:: https://dvc.org/img/logo-github-readme.png
   :target: https://dvc.org
   :alt: DVC logo

.. |Release| image:: https://img.shields.io/badge/release-ok-brightgreen
   :target: https://travis-ci.com/iterative/dvc/branches
   :alt: Release

.. |CI| image:: https://github.com/iterative/dvc/workflows/Tests/badge.svg?branch=master
   :target: https://github.com/iterative/dvc/actions
   :alt: GHA Tests

.. |Maintainability| image:: https://codeclimate.com/github/iterative/dvc/badges/gpa.svg
   :target: https://codeclimate.com/github/iterative/dvc
   :alt: Code Climate

.. |Coverage| image:: https://codecov.io/gh/iterative/dvc/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/iterative/dvc
   :alt: Codecov

.. |Donate| image:: https://img.shields.io/badge/patreon-donate-green.svg?logo=patreon
   :target: https://www.patreon.com/DVCorg/overview
   :alt: Donate

.. |Snap| image:: https://img.shields.io/badge/snap-install-82BEA0.svg?logo=snapcraft
   :target: https://snapcraft.io/dvc
   :alt: Snapcraft

.. |Choco| image:: https://img.shields.io/chocolatey/v/dvc?label=choco
   :target: https://chocolatey.org/packages/dvc
   :alt: Chocolatey

.. |Brew| image:: https://img.shields.io/homebrew/v/dvc?label=brew
   :target: https://formulae.brew.sh/formula/dvc
   :alt: Homebrew

.. |Conda| image:: https://img.shields.io/conda/v/conda-forge/dvc.svg?label=conda&logo=conda-forge
   :target: https://anaconda.org/conda-forge/dvc
   :alt: Conda-forge

.. |PyPI| image:: https://img.shields.io/pypi/v/dvc.svg?label=pip&logo=PyPI&logoColor=white
   :target: https://pypi.org/project/dvc
   :alt: PyPI

.. |Packages| image:: https://img.shields.io/github/v/release/iterative/dvc?label=deb|pkg|rpm|exe&logo=GitHub
   :target: https://github.com/iterative/dvc/releases/latest
   :alt: deb|pkg|rpm|exe

.. |DOI| image:: https://img.shields.io/badge/DOI-10.5281/zenodo.3677553-blue.svg
   :target: https://doi.org/10.5281/zenodo.3677553
   :alt: DOI

.. |Flowchart| image:: https://dvc.org/img/flow.gif
   :target: https://dvc.org/img/flow.gif
   :alt: how_dvc_works
