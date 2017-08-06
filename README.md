# ACM-General Django Project

Welcome to the ACM-General Django Project!

## Setting Up Your Environment 
In order to set up a production-like environment, we have two main options:
1. Develop using [Vagrant](https://www.vagrantup.com/).
2. Use a Linux computer or virtual machine.

For some more information about each of these options, refer to the sections
below.

### Vagrant
Vagrant provides a very simple and high fidelity way of interacting with the
codebase in a standardized way. The goal of Vagrant is to make development
easier by automatically provisioning a production like environment within a
virtual machine. 

#### Dependencies
In order to use Vagrant you must download the following tools:
1. [Vagrant](https://www.vagrantup.com/downloads.html)
2. [VirtualBox](https://www.virtualbox.org/wiki/Downloads). 

Note: while you do not need VirtualBox specifically, only certain virtualization 
providers are supported by Vagrant (like VMWare).

#### Running Vagrant

In order to use Vagrant, open the terminal in any OS, navigate to the root GIT
directory (you should see the `Vagrantfile` file), and type `vagrant up`.
`vagrant up` will start the VM, provision it, and then run the setup script
within the VM. Open your web browser and put `http://localhost:8000` as the URL.
If you see a site which looks like [https://acm.mst.edu](http://acm.mst.edu)
everything setup correctly. One of the great features about Vagrant is that now
you can edit the file locally and the changes will be reflected in the
virtual machine. For example, if you edit the `view.py` of any app within the
project, those edits will be transferred to the VM. When you refresh your
browser the webpage should reflect those changes.

For changes that cannot be auto refreshed by Django (changes to the static
files, app migrations, etc.), you can do these changes manually (in the future,
we hope to make a command to do this). To refresh the app, do the following
commands in the folder where you can see the `Vagrantfile`:

```bash
# This allows you to directly access the VM through ssh
# NOTE: If you do not have a CLI-interface (i.e. you are using windows cmd or
# powershell, read below in Windows Specific Problems)
vagrant ssh 
# This changes you to the root user
sudo su 
# This attaches you to the tmux session which is running the Django server
tmux attach 
# Hit control-C to kill the server, don't type <C-c>
<C-c> 
# Run whatever command you need to affect the server ./manage.py collectstatic./manage.py migrate, etc.
... 
# Start the server again
./manage.py runserver 0.0.0.0:8000
```

##### Windows Specific Problems
If you are not using a terminal which supports a CLI interface for ssh like
Windows PowerShell or cmd, there are two ways you can get around this. 

The easier way is to download [Git Bash](https://git-scm.com/downloads) and use
Git Bash as your terminal for vagrant. Git Bash is a terminal which works like a
pseudo-Linux terminal.

The way which requires a little more work is using PuTTY to ssh into the Vagrant
box. A good tutorial article on how to do these can be located
[here](http://tech.osteel.me/posts/2015/01/25/how-to-use-vagrant-on-windows.html)
. Browse to the `PuTTY` section for specific instructions. This article also
shows more information on Git Bash.

If you can successfully ssh into the box, continue running the commands listed
in the [Running Vagrant](#running-vagrant) section beneath the `vagrant ssh`
command.

### Native Linux
In order to run the environment on a native Linux machine, navigate to the root
directory of the git repository and run the following commands:

```
cp ./dependencies/settings_local.template ./ACM_General/ACM_General/settings_local.py
python3 ./ACM_General/manage.py runserver 0.0.0.0:8000
```
