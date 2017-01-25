# ACM-General Django Project

Welcome to the ACM-General Django Project!

## Installation
In any directory of the users chosing, please execute the following commands:
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3 python3-pip postgresql libpq-dev
sudo pip3 install -r requirements.txt 
git init
git remote add origin THIS_REPOS_CLONE_LINK
git pull origin master
cd ACM_Website/
sudo su - postgres
psql
> # CREATE DATABASE django_acmgeneral;
> # CREATE USER djangouser WITH PASSWORD 'djangoUserPassword';
> # GRANT ALL PRIVILEGES ON django_acmgeneral TO djangouser;
> # \q
exit
sudo nano ACM_Website/settings.py [CHANGE ALLOWED_HOST TO CURRENT IP]
sudo python3 manage.py makemigrations
sudo python3 manage.py migrate
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
