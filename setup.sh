sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install python3 python3-pip postgresql libpq-dev uwsgi uwsgi-plugin-python3
sudo -u postgres psql -c "create database django_acmgeneral"
sudo -u postgres psql -c "create user djangouser with password 'djangoUserPassword'"
sudo -u postgres psql -c "grant all privileges on database django_acmgeneral to djangouser"
sudo pip3 install -r requirements.txt
cd ACM_General/
cp ACM_General/settings_local.template ACM_General/settings_local.py
sudo python3 manage.py makemigrations accounts core events home sigs thirdparty_auth
sudo python3 manage.py collectstatic
sudo python3 manage.py migrate
