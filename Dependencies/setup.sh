###
# Installing all the necessary dependencies. 
###
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install python3 python3-pip postgresql nginx libpq-dev uwsgi uwsgi-plugin-python3 xvfb
sudo pip3 install -r requirements.txt

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
mkdir -p /var/django/
cd ../../
sudo cp -rf acm.mst.edu /var/django/
cd /var/django/acm.mst.edu/Dependencies

###
# Moving he propeer configuration files into place.
###
# WARNING: This -n will not quash any existing files so if you're looking for a
#          complete overwrite remove these flags
cp -n settings_local.template ../ACM_General/ACM_General/settings_local.py
cp -n ACMGeneral_uwsgi.ini /etc/uwsgi/apps-available
cp -n env_vars.template /etc/uwsgi/apps-available/env_vars.txt
cp -n ssl-acm.mst.edu /etc/nginx/sites-available
sudo ln -s /etc/uwsgi/apps-available/ACMGeneral_uwsgi.ini /etc/uwsgi/apps-enabled/
sudo ln -s /etc/nginx/sites-available/ssl-acm.mst.edu /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
cd ../ACM_General
###
# www-data needs to own the directory for special nginx interactions
###
sudo chown www-data:www-data -R /var/django

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
# Restarting the two services necessary to make it run.
###
sudo service uwsgi restart
sudo service nginx restart
