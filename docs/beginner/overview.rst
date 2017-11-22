==========================
Setting up the environment
==========================

The first step towards developing is setting up your local environment.

------------
Download Git
------------
In order to download the code locally, you need to use `Git`_.  `Git`_ is a
source control management system which helps version and revise code. For more
information and usage, please view the :ref:`Git tutorial <tutorial-git>`. 

Additional Resource:
    1. https://www.atlassian.com/git/tutorials/install-git
    2. https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

Windows
=======
Command-line
------------
If you're comfortable with the command line, `Git`_ has a command-line version
called ``Git Bash``. ``Git Bash`` is a BASH "emulator" that allows you to run
`Git`_ commands just like on a UNIX computer terminal (think of the commands you
would run over PuTTy in CS 1570). 

There are two main ways you can install `Git`_ for command line:

1. `Official Git`_
2. `Git for Windows`_

.. note::
    In the installation settings for `Official Git`_, you need to explicitly
    include Git Bash. Otherwise, it will not be installed.

Click on the link in the list above and follow the installation instructions for 
the Window's executable.

.. _Official Git: https://git-scm.com/downloads
.. _Git for Windows: https://git-for-windows.github.io

GUI Client
----------
Some common `Git`_ GUI clients include:

1. `GitKraken`_
2. `Github Desktop`_
3. `TortoiseGit`_

There are pros and cons for each option, but overall I recommend using
`GitKraken`_.

To install any of these options, click on the link to their website and download
the Window's executable.

.. _GitKraken: https://www.gitkraken.com/
.. _Github Desktop: https://desktop.github.com/
.. _TortoiseGit: https://tortoisegit.org/

.. _overview-ssh-key:

---------------------------
Adding SSH Key (Optional)
---------------------------
.. note::
    TODO

--------------------
Clone the repository
--------------------
Now that you have `Git`_ installed, clone the `acm.mst.edu repository
<https://github.com/sigdotcom/acm.mst.edu>`_ from `GitHub`_. Cloning in `Git`_ is
just a special term for downloading all of the files saved on the remote
repository. In this case, the repository is located on `GitHub`_. 

Command-line
============
Open ``Git Bash``, ``cmd``, or any terminal and type::

    git clone https://github.com/sigdotcom/acm.mst.edu.git

If you :ref:`added your ssh key <overview-ssh-key>`, you can use the following
command::

    git clone git@github.com:sigdotcom/acm.mst.edu.git

.. _Git: https://git-scm.com
.. _GitHub: https://github.com/

GUI
===
.. note::
    TODO
