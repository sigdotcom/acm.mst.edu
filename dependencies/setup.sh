#!/usr/bin/env bash

# Colors
GREEN="\e[92m"
RED="\e[91m"
RESET="\e[0m"

if [[ $EUID -ne 0 ]]; then
    echo -e "[${RED}ERROR${RESET}] This script must be run as root" 
    exit 1
fi

if [ "`basename $(pwd)`" != "dependencies" ]; then
    echo -e "[${RED}ERROR${RESET}] setup.sh must be run in the dependencies folder."
    exit 1;
fi

if [[ $# -ne 1 ]]; then
    echo -e "usage: setup.sh {dev, live}"
    exit 1;
fi

INSTALLATION_DIR="/var/django"
ROOT_DIR="../../"

if [[ $1 == "dev" ]]; then
    BUILD_URL="dev.kevinschoonover.me"
elif [[ $1 == "live" ]]; then
    BUILD_URL="acm.mst.edu"
else
    echo -e "usage: setup.sh {dev, live, vagrant}"
    exit 1;
fi

###
# Installing all the necessary dependencies. 
###
apt update
apt upgrade -y
apt install python3 python3-pip postgresql nginx libpq-dev uwsgi uwsgi-plugin-python3 xvfb ruby-compass -y
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
# Putting the main repository in /var/django/
###
mkdir -p $INSTALLATION_DIR
cd $ROOT_DIR
echo "Current Directory = `pwd`"
rsync -av --delete acm.mst.edu/ $INSTALLATION_DIR/$BUILD_URL/

cd $INSTALLATION_DIR/$BUILD_URL/dependencies

###
# Moving the proper configuration files into place.
###
# WARNING: This -n will not quash any existing files so if you're looking for a
#          complete overwrite remove these flags
rsync -auz settings_local.template ../ACM_General/ACM_General/settings_local.py
rsync -auz ACMGeneral_uwsgi.ini /etc/uwsgi/apps-available/ACMGeneral_uwsgi.ini
rsync -auz env_vars.template /etc/uwsgi/apps-available/env_vars.txt
rsync -auz ssl-acm.mst.edu /etc/nginx/sites-available/ssl-acm.mst.edu
sed -i "s#{{ BUILD_URL }}#'"$BUILD_URL"'#g" /etc/nginx/sites-available/ssl-acm.mst.edu
sed -i "s#{{ INSTALLATION_DIR }}#'"$INSTALLATION_DIR"'#g" /etc/nginx/sites-available/ssl-acm.mst.edu
sed -i "s#{{ BUILD_URL }}#$BUILD_URL#g" /etc/uwsgi/apps-available/ACMGeneral_uwsgi.ini
sed -i "s#{{ INSTALLATION_DIR }}#$INSTALLATION_DIR#g" /etc/uwsgi/apps-available/ACMGeneral_uwsgi.ini

sed -i '/localhost/s/]/, u\x27'"$BUILD_URL"'\x27]/' ../ACM_General/ACM_General/settings_local.py

ln -s /etc/uwsgi/apps-available/ACMGeneral_uwsgi.ini /etc/uwsgi/apps-enabled/
ln -s /etc/nginx/sites-available/ssl-acm.mst.edu /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
cd ../ACM_General
###
# www-data needs to own the directory for special nginx interactions
###
chown www-data:www-data -R $INSTALLATION_DIR 

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
cd ..
echo `pwd`
echo `ls`
compass compile

###
# Restarting the two services necessary to make it run.
###
service uwsgi restart
service nginx restart
