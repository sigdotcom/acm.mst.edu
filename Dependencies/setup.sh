sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install python3 python3-pip postgresql nginx libpq-dev uwsgi uwsgi-plugin-python3
sudo -u postgres psql -c "create database django_acmgeneral"
sudo -u postgres psql -c "create user djangouser with password 'djangoUserPassword'"
sudo -u postgres psql -c "grant all privileges on database django_acmgeneral to djangouser"
sudo pip3 install -r requirements.txt
cp settings_local.template ../ACM_General/ACM_General/settings_local.py
cp ACMGeneral_uwsgi.ini /etc/uwsgi/apps-available
cp ssl-acm.mst.edu /etc/nginx/sites-available
sudo ln -s /etc/uwsgi/apps-available/ACMGeneral_uwsgi.ini /etc/uwsgi/apps-enabled/
sudo ln -s /etc/nginx/sites-available/ssl-acm.mst.edu /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
cd ../ACM_General
sudo python3 manage.py makemigrations accounts core events home sigs thirdparty_auth
sudo python3 manage.py collectstatic
sudo python3 manage.py migrate
sudo service uwsgi restart
sudo service nginx restart
