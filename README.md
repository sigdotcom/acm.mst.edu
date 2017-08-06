# ACM-General Django Project

Welcome to the ACM-General Django Project!

## Setting Up Your Environment 
In order to set up a production-like environment, we have two main options:
1. Develop using [Vagrant](https://www.vagrantup.com/).
2. Use a linux computer or virtual machine.

For some more information about each of these options, refer to the sections
below.

### Vagrant
Vagrant provides a very simple and high fidelity way of interacting with the
codebase in a standardized way. The goal of Vagrant is to make development
easier by automatically provisioning a production like environment within a
virtual machine. 

In order to use Vagrant you must download the following tools:
1. [Vagrant](https://www.vagrantup.com/downloads.html)
2. [VirtualBox](https://www.virtualbox.org/wiki/Downloads). 

Note: while you do not need VirtualBox specifically, only certain virtualization
providers are supported by Vagrant (like VMWare).

In order to use Vagrant, open the terminal in any OS, navigate to the root GIT
directory (you should see the `Vagrantfile` file) and type `vagrant up`.
`vagrant up` will start the VM, provision it, and then run the setup script
within the VM. Open your web browser and put `http://localhost:8000` as the URL.
If you see a site which looks like [http://acm.mst.edu](http://acm.mst.edu),
everything went correctly. One of the great features about Vagrant is that now
you can edit the file locally and the changes will be reflected in the
virtual machine. For example, if you edit the `view.py` of any app within the
project, those edits will be transferred to the VM. When you refresh the
webpage should reflect those changes.

For changes that cannot be auto refreshed by Django (changes to the static
files, app migrations, etc.), you can do these changes manually (in the future,
we hope to make a command to do this). To refresh the app, do the following
commands in the folder where you can see the `Vagrantfile`:

```bash
vagrant ssh # This allows you to directly access the VM through ssh
sudo su # This changes you to the root user
tmux attach # This attaches you to the tmux session which is running the Django server
<C-c> # Hit control-C to kill the server, don't type <C-c>
... # Run whatever command you need to affect the server ./manage.py collectstatic./manage.py migrate, etc.
./manage.py runserver 0.0.0.0:8000
```
