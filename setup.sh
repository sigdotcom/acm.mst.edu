sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3 python3-pip postgresql libpq-dev
sudo -u postgres psql -c "create database django_acmgeneral"
sudo -u postgres psql -c "create user djangouser with password 'djangoUserPassword'"
sudo -u postgres psql -c "grant all privileges on database django_acmgeneral to djangouser"
cd ACM_General/
python3 manage.py makemigrations accounts core events home sigs thirdparty_auth
python3 manage.py collectstatic
python3 manage.py migrate
