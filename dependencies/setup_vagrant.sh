#!/usr/bin/env bash

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root" 
    exit 1
fi

if [ "`basename $(pwd)`" != "dependencies" ]; then
    echo "setup.sh must be run in the dependencies folder."
    exit 1;
fi

###
# Installing all the necessary dependencies. 
###
apt update
apt upgrade -y
apt install python3 python3-pip postgresql nginx libpq-dev uwsgi uwsgi-plugin-python3 xvfb
pip3 install -r requirements.txt

###
# Preparing the database
###
sudo -u postgres psql -c "drop database django_acmgeneral"
sudo -u postgres psql -c "create database django_acmgeneral"
sudo -u postgres psql -c "create user djangouser with password 'djangoUserPassword'"
sudo -u postgres psql -c "grant all privileges on database django_acmgeneral to djangouser"
sudo -u postgres psql -c "alter user djangouser createdb"

###
# Moving he propeer configuration files into place.
###
# WARNING: This -n will not quash any existing files so if you're looking for a
#          complete overwrite remove these flags
rsync -auz settings_local.template ../ACM_General/ACM_General/settings_local.py

###
# Generating the django migrations from scratch.
###
find .. -name migrations -type d -exec rm -rf {} \;
for d in *; do
    if [ -d "$d" ]; then
        echo "Running $D"
        python3 manage.py makemigrations "$d"
    fi
done
python3 manage.py collectstatic --noinput
python3 manage.py migrate --noinput

###
# Creating the Sphinx documentation
###
cd ../docs/
make html
