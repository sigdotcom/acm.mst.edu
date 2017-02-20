# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "ubuntu/trusty64"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  config.vm.synced_folder ".", "/vagrant", type: "nfs"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.network "private_network", type: "dhcp"

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  $updates = <<-UPDATE
    apt-get update
    apt-get install -y python3 python3-pip postgresql libpq-dev nfs-common
  UPDATE

  $db = <<-DB
    sudo -u postgres psql -c "create database django_acmgeneral"
    sudo -u postgres psql -c "create user djangouser with password 'djangoUserPassword'"
    sudo -u postgres psql -c "grant all privileges on database django_acmgeneral to djangouser"
  DB

  $migrate = <<-MIGRATE
    cd /vagrant
    pip3 install -r requirements.txt
    cd ACM_General/
    cp ACM_General/settings_local.template ACM_General/settings_local.py
    python3 manage.py makemigrations accounts core events home sigs thirdparty_auth
    python3 manage.py collectstatic
    python3 manage.py migrate
  MIGRATE

  $setup = <<-SETUP
    tmux new-session -d -s django 'cd /vagrant/ACM_General && python3 manage.py runserver 0.0.0.0:8000'
    tmux ls
    tmux detach -s django
  SETUP

  config.vm.provision :shell, inline: $updates
  config.vm.provision :shell, inline: $db
  config.vm.provision :shell, inline: $migrate
  config.vm.provision :shell, inline: $setup
end
