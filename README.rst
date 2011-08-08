A complete server setup with django cms

Keywords:

Nginx
Gunicorn
Supervisord
Postgresql
Rabbitmq
Celery
Memcached
Solr
Postfix - managed from the django admin!
Dovecot - ditto

Usage:

www.vagrantup.com
Get vagrant up and running
then login and run this:

sudo aptitude update

sudo aptitude install -y git-core python python-dev python-setuptools

sudo easy_install -U pip ; sudo pip install fabric ; sudo pip install jinja2

wget https://raw.github.com/mitchellh/vagrant/master/keys/vagrant.ppk

git clone ssh://oyvind@mainframe.cylon.no/home/oyvind/complete-cms-deployment

cd complete-cms-deployment

# config below is needed because of what seems like a neat trick in fab_settings.py, needs a brilliant mind to set mine straight, yours?

fab -R vagrant config setup_all # if fails vagrant destroy and add a " -w" here
# you will get 4 prompts 2 for java 2 for postfix, use tab and space to navigate