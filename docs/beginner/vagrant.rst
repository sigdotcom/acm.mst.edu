.. _tutorial-vagrant:

=======
Vagrant
=======

----------------
What is Vagrant?
----------------
`Vagrant`_ is a tool for building and distributing development environments.
This allows for similar development environments to be shared across developers
which model the production environment. Because of this parity, developers can
see how their code would run on a production server locally. Proper usage of
`Vagrant`_ can help minimize code integration problems and alert the developer
to potential problems in their code.

A concrete way to think about this is `Vagrant`_ provisions a machine (in this
case a Virtual Machine) according to a configuration file, a ``Vagrantfile``.
Then, `Vagrant`_ provides various interfaces for interacting with this machine
such as exposing ports on the virtual machine or sharing a local file with the
virtual machine.

-----------
Vagrantfile
-----------
A ``Vagrantfile`` is a file which describes the type of machine required for the
project and the configuration process for this machine. The ``Vagrantfile`` for
this project is located in the root git directory. 

Whenever you provision a machine such as when the ``--provision`` flag is
applied , the ``Vagrantfile`` is read by Vagrant and used to provision a machine
based on the configuration specified. Whenever you update the Vagrantfile, you
must re-provision the current machine in order to reapply the configuration.

For additional documentation about the ``Vagrantfile``, please see the official
documentation `here <https://www.vagrantup.com/docs/vagrantfile/>`_.

---------------
Common Commands
---------------
All commands referenced in this section must be run with a ``Vagrantfile`` in
the appropriate path. See the `Vagrantfile Lookup Path
<https://www.vagrantup.com/docs/vagrantfile/#lookup-path>`_ documentation for
more information.

In order to start the virtual machine, you must inform `Vagrant`_ to setup the
virtual machine and run it. To do this, run the following command::

    vagrant up

Please see `vagrant up documentation
<https://www.vagrantup.com/docs/cli/up.html>`_ for more information.


Whenever a migration needs to be performed or a change that requires the
provision script to be run again, run the following command::

    vagrant reload --provision

Please see `vagrant reload documentation
<https://www.vagrantup.com/docs/cli/reload.html>`_ for more information.

If there is a problem with the Vagrantbox or you wish to restore your computer
to a clean slate before the Vagrantbox, please run the following command::

    vagrant destroy

Please see `vagrant destroy documentation
<https://www.vagrantup.com/docs/cli/destroy.html>`_ for more information.

.. _Vagrant: https://www.vagrantup.com/
