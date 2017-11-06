sudo -u postgres psql -c "drop database django_acmgeneral"
sudo -u postgres psql -c "create database django_acmgeneral"
sudo -u postgres psql -c "create user djangouser with password 'djangoUserPassword'"
sudo -u postgres psql -c "grant all privileges on database django_acmgeneral to djangouser"
sudo -u postgres psql -c "alter user djangouser createdb"

