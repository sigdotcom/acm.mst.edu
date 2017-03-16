# ACM-General Django Project

Welcome to the ACM-General Django Project!

## Installation
### Vagrant
Vagrant is a development tool we use to help ease the burden of configuring the different components of the project. With Vagrant, we don't have to worry about having various things installed such as Django, Python3, postgreSQL, etc. Although we do recommend installing Python and Django if you haven't already so that you can practice with them in case you aren't familiar with them. Using Vagrant simply makes it so that when testing the website, all required components will be installed on a virtual machine and the website will be locally hosted for further testing.

### Requirements
1. [Virtualbox](https://virtualbox.org)
  + Or another virtualization tool, but `virtualbox` works nicely with vagrant. (We suggest using VirtualBox unless you have previous experience with other virtualization tools).
2. [Vagrant](https://vagrantup.com)
  + Download the version compatible with your host operating system.

After satisfying these requirements, change to the directory in which the Vagrant file is located and run the following command:
```bash
$ vagrant up
```
This will initialize and provision the vagrant box. (This may take some time)  

After that you can run  
```bash
$ vagrant reload --provision # this will restart and reprovision the vm

$ vagrant halt # this will shutdown the vm

$ vagrant status # this will report the current status of the vm

$ vagrant destroy # this will delete the vm

$ vagrant up # this will, of course, build the vm if it has been destroyed
```

## Apps
In order to see detailed information about each of the apps, please see the read me in each of the app directories.
1. [Core](ACM_General/core/)
  + This app handles the core components of the ACM\_General project such as the base templates, global static css documents, and a variety of other generic needs which the project requires
2. [Accounts](ACM_General/accounts/)
  + This app handles the main components of the account features of the project such as login, logout, registering of a user, and authenticating users.
  + This is where the custom authentication backend and custom BaseUser are stored.
3. [Events](ACM_General/events/)
  + This app handles the main event components of the project such as registering an event and registering for an event.
4. [Home](ACM_General/home/)
  + This app handles the main index of the project and the homepage.

## Contributing
Please contact [acm@mst.edu](acm@mst.edu) if you wish to contribute to this project.
