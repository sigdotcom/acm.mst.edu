# ACM-General Django Project

Welcome to the ACM-General Django Project!

## Installation
In any directory of the users chosing, please execute the following commands:
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3 python3-pip postgresql libpq-dev
git clone GITHUB_REPOSITORY_LINK
cd ACM_General/
sudo su - postgres
psql
> # CREATE DATABASE django_acmgeneral;
> # CREATE USER djangouser WITH PASSWORD 'djangoUserPassword';
> # GRANT ALL PRIVILEGES ON django_acmgeneral TO djangouser;
> # \q
exit
sudo nano ACM_General/settings.py             # Change ALLOWED_HOSTS to current IP
sudo cp ACM_General/settings_local.template ACM_Website/settings_local.py
sudo nano ACM_General/settings_local.py       # Add values as necessary
sudo python3 manage.py makemigrations accounts home #... any other apps
sudo python3 manage.py migrate
```

Note: `makemigrations` ***with*** application names should only be necessary if this is the first time building the project.

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
  
## Vagrant
Vagrant is a development tool we use to help ease the burden of configuring the different components of the project.  

### Requirements
1. [Virtualbox](https://virtualbox.org)
  + Or another virtualization tool, but `virtualbox` works nicely with vagrant.
2. [Vagrant](https://vagrantup.com)
  + Download the version compatible with your host operating system.
  
After satisfying those requirements it should be possible to run
```bash
$ vagrant up
```
from within the project root directory to initialize and provision the vagrant box. (This may take some time)  

After that you can run  
```bash
vagrant reload --provision # this will restart and reprovision the vm

vagrant halt # this will shutdown the vm

vagrant status # this will report the current status of the vm

vagrant destroy # this will delete the vm

vagrant up # this will, of course, build the vm if it has been destroyed
```

## Contributing
Please contact [acm@mst.edu](acm@mst.edu) if you wish to contribute to this project.
