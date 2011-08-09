A complete server setup with django cms

Keywords:

* Nginx
* Gunicorn
* Django CMS
* cmsplugin-blog
* django-threadedcomments
* djano-uni-form
* django-cms-facetsearch
* cmsplugin-blog-search
* Supervisord
* Postgresql
* Rabbitmq
* Celery
* Memcached
* Solr
* Postfix, Dovecot - managed from the django admin!

Fully working example with templates using blueprint css

Usage:

www.vagrantup.com
Get vagrant up and running

Then login and run this::

    sudo aptitude update

    sudo aptitude install -y git-core python python-dev python-setuptools

    sudo easy_install -U pip ; sudo pip install fabric ; sudo pip install jinja2

    git clone http://github.com/fivethreeo/complete-cms-deployment.git

    cd complete-cms-deployment

    # config below is needed because of what seems like a neat trick in fab_settings.py, needs a brilliant mind to set mine straight, yours?

    fab -R vagrant config setup_all
    # if fails vagrant destroy and add a " -w" here
    # you will get 4 prompts 2 for java 2 for postfix, use tab and space to navigate

If completed successfully point your browser to http://localcost:forwarded_vagrant_port_80/

Postfix might require a restart to get going.