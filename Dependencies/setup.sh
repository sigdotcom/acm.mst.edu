sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install python3 python3-pip postgresql nginx libpq-dev uwsgi uwsgi-plugin-python3 xvfb
sudo -u postgres psql -c "drop database django_acmgeneral"
sudo -u postgres psql -c "create database django_acmgeneral"
sudo -u postgres psql -c "create user djangouser with password 'djangoUserPassword'"
sudo -u postgres psql -c "grant all privileges on database django_acmgeneral to djangouser"
sudo pip3 install -r requirements.txt
# WARNING: This -n will not quash any existing files so if you're looking for a
#          complete overwrite remove these flags
cp -n settings_local.template ../ACM_General/ACM_General/settings_local.py
cp -n ACMGeneral_uwsgi.ini /etc/uwsgi/apps-available
cp -n ssl-acm.mst.edu /etc/nginx/sites-available
sudo ln -s /etc/uwsgi/apps-available/ACMGeneral_uwsgi.ini /etc/uwsgi/apps-enabled/
sudo ln -s /etc/nginx/sites-available/ssl-acm.mst.edu /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
cd /usr/local/bin/
wget https://github.com/mozilla/geckodriver/releases/download/v0.15.0/geckodriver-v0.15.0-linux64.tar.gz
tar -xvzf geckodriver-v0.15.0-linux64.tar.gz
rm geckodriver-v0.15.0-linux64.tar.gz
cd - 
cd ../ACM_General
sudo chown www-data:www-data -R /var/django
find .. -name migrations -type d -exec rm -rf {} \;
sudo python3 manage.py makemigrations accounts core events home sigs thirdparty_auth payments --noinput
sudo python3 manage.py collectstatic --noinput
sudo python3 manage.py migrate --noinput
sudo chown www-data:www-data -R /var/django
sudo service uwsgi restart
sudo service nginx restart
