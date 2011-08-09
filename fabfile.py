import contextlib
from fabric.api import env, run, cd, sudo, put, get, require, settings, hide, local
from fabric.contrib import project
from fabric.contrib import files

import time

from fab_settings import global_settings, group_settings, servers

# prepare settings
groupmapping = {}
roledefs = {}
for role, servers in servers.items():
    roledefs[role] = []
    for server in servers:
       roledefs[role].append(server[0])
       groupmapping[server[0]] = server[1]
       
env.roledefs = roledefs

def config():
    """ Utility: Setup settings """
    for key, setting in global_settings.items():
        env[key] = setting % env
    for key, setting in group_settings[groupmapping[env.host_string]].items():
        env[key] = setting % env

def create_manage_command(cmd):
    """  Utility: return manage.py oneliner """
    cmdstr = "PYTHONPATH=%(extra_paths)s /home/%(user)s/%(project_name)s/bin/python /home/%(user)s/%(project_name)s/project/%(project_name)s/manage.py %%s" % env
    return cmdstr % cmd
    
def manage(cmd, use_sudo=False):
    runcmd = create_manage_command(cmd)
    if use_sudo:
        sudo(runcmd)
    else:
        run(runcmd)

def python(cmd):
    """  Utility: return python one liner """
    cmdstr = "PYTHONPATH=%(extra_paths)s DJANGO_SETTINGS_MODULE=settings /home/%(user)s/%(project_name)s/bin/python -c \"%%s\"" % env
    return cmdstr % cmd
    
def deploy_full(full_setup=False, first_run=False):
    """Full deploy: push, pip and reload."""
    push()
    update_dependencies()
    run(create_manage_command("collectstatic --noinput"))
    reload(full_setup=full_setup, first_run=first_run)

def deploy_project():
    push()
    run(create_manage_command("collectstatic --noinput"))
    reload()

def push_project():
    """ Push out new code to the server """
    with settings(warn_only=True):
        local("tar -czf ../innomed_deployment.tar.gz .")
        run("mkdir /home/%(user)s/tmp" % env)
        put("../innomed_deployment.tar.gz", "/home/%(user)s/tmp" % env)
        with cd("/home/%(user)s/tmp" % env):
            run("tar -xzf innomed_deployment.tar.gz") 
            run("rm -rf /home/%(user)s/%(project_name)s/project" % env)
            run("cp -rf project /home/%(user)s/%(project_name)s/project" % env)
            run("rm -rf /home/%(user)s/%(project_name)s/external_apps" % env)
            run("cp -rf external_apps /home/%(user)s/%(project_name)s/external_apps" % env)
            run("rm -rf /home/%(user)s/%(project_name)s/local_apps" % env)
            run("cp -rf local_apps /home/%(user)s/%(project_name)s/local_apps" % env)
        run("rm -rf /home/%(user)s/tmp" % env)
                                  
def push_django_settings():
    files.upload_template("config/local_settings.py", "/home/%(user)s/%(project_name)s/project/%(project_name)s/local_settings.py" % env, context=env)
               
def push_wsgi():
    files.upload_template("config/app.wsgi", "%(wsgipath)s" % env, use_sudo=True, context=env)

def push():
    push_project()
    push_django_settings()
    if not hasattr(env, 'use_nginx'):
        push_wsgi()

def update_dependencies():    
    """ Update requirements remotely """
    put("config/requirements.txt", "%(root)s/requirements.txt" % env)
    run("%(root)s/bin/pip install -r %(root)s/requirements.txt" % env)
        
def reload(full_setup=False, first_run=False):
    """ Reload webserver/webapp """
    if full_setup==False:
        sudo("kill -QUIT `cat %(nginx_pidfile)s`" % env)
    sudo("supervisorctl restart all")
    sudo("%(nginx_bin)s" % env)

# OK, simple stuff done. Here's a more complex example: provisioning
# a server the simplistic way.

def setup_all():
    """ Setup all parts on one single server adds a fully running setup """
    setup_webserver()
    setup_webapp()
    setup_supervisord()
    update_dependencies()
    push()
    setup_dbserver()
    configure_db()
    deploy_full(full_setup=True)
    syncdb()
    add_site()
    add_superuser()
    setup_solr()
    solr_multicore()
    update_solr_schema()
    setup_postfix()
    setup_celery()
    setup_memcached()
    configure_supervisor_gunicorn()
    
def setup_instance():
    setup_webapp()
    update_dependencies()
    push()
    configure_db()
    deploy_full(first_run=True)
    syncdb()
    add_site()
    add_superuser()
    update_solr_schema()
    configure_celery()
    configure_memcached()
    configure_supervisor_gunicorn()

def setup_solr():
    """ Setup search server """
    with settings(warn_only=True):
        sudo("aptitude update")
        sudo("aptitude -y install python-software-properties")
        sudo("sudo add-apt-repository \"deb http://archive.canonical.com/ lucid partner\"")
        sudo("aptitude update")
        sudo("aptitude -y install sun-java6-jdk "
                              "tomcat6 "
                              "solr-tomcat")

def solr_multicore():
    if not files.exists('/etc/solr/oldconf'):
        sudo("cp -Rp /etc/solr/conf /etc/solr/oldconf")
        sudo("rm -rf /etc/solr/conf")
        sudo("rm -rf /var/lib/solr/data")
        sudo("chown -R tomcat6:tomcat6 /etc/solr")
        sudo("chown -R tomcat6:tomcat6 /var/lib/solr")
    cores = env.solr_cores.split(',')
    for core in cores:
        if not files.exists("/etc/solr/conf-%s" % core):
            sudo("cp -Rp /etc/solr/oldconf /etc/solr/conf-%s" % core)
            sudo("mkdir /usr/share/solr/%s" % core)
            sudo("ln -s /etc/solr/conf-%s /usr/share/solr/%s/conf" % (core,core))
            files.sed("/etc/solr/conf-%s/solrconfig.xml" % core, "/var/lib/solr/data", "/var/lib/solr/%s/data" % core, use_sudo=True)
    
    files.upload_template("solr/solr.xml", "/usr/share/solr/solr.xml", context={'cores': cores}, use_jinja=True, use_sudo=True)
    restart_tomcat() # restart but conf will be borked until you update_solr_schema() for each core

def update_solr_schema():
    run(create_manage_command("build_solr_schema > /home/%(user)s/schema.xml" % env))
    sudo("cp /home/%(user)s/schema.xml /etc/solr/conf-%(solr_core)s/schema.xml" % env)
    restart_tomcat()
    
def restart_tomcat():
    sudo("invoke-rc.d tomcat6 restart")

def setup_postfix():

    sudo("sysctl kernel.hostname=%(postfix_hostname)s" % env)

    sudo("invoke-rc.d dovecot stop")
    sudo("invoke-rc.d dovecot start")
    sudo("invoke-rc.d postfix restart")
    sudo("invoke-rc.d spamassassin restart")
    sudo("invoke-rc.d clamav-daemon restart")
    sudo("invoke-rc.d amavis restart")
    sudo("aptitude update")
    sudo("aptitude -y install postfix postfix-tls postfix-pgsql "
                            "dovecot-imapd dovecot-pop3d dovecot-common "
                            "amavisd-new spamassassin clamav-daemon "
                            "libnet-dns-perl libmail-spf-query-perl pyzor razor "
                            "arj bzip2 cabextract cpio file gzip lha nomarch pax rar unrar unzip unzoo zip zoo")
                                
    sudo("adduser clamav amavis")
    sudo("adduser amavis clamav")
    sudo("groupadd vmail")
    sudo("useradd -g vmail -s /bin/false -d /home/vmail vmail")
    sudo("mkdir /home/vmail")
    sudo("chown vmail:vmail /home/vmail")    
    sudo("groupadd spamd")
    sudo("useradd -g spamd -s /bin/false -d /var/log/spamassassin spamd")
    sudo("mkdir /var/log/spamassassin")
    sudo("chown spamd:spamd /var/log/spamassassin")
    configure_postfix()
    
def configure_postfix():
    files.upload_template("postfix/main.cf", "/etc/postfix/main.cf", use_sudo=True, context=env)    
    sudo("postconf -e \"content_filter = smtp-amavis:[127.0.0.1]:10024\"")
    files.upload_template("postfix/master.cf", "/etc/postfix/master.cf" % env, use_sudo=True, context=env)    
    files.upload_template("postfix/mailboxes.cf", "/etc/postfix/mailboxes.cf" % env, use_sudo=True, context=env)   
    files.upload_template("postfix/transport.cf", "/etc/postfix/transport.cf" % env, use_sudo=True, context=env)   
    files.upload_template("postfix/aliases.cf", "/etc/postfix/aliases.cf" % env, use_sudo=True, context=env)    
    files.upload_template("postfix/dovecot.conf", "/etc/dovecot/dovecot.conf" % env, use_sudo=True, context=env)   
    files.upload_template("postfix/dovecot-sql.conf", "/etc/dovecot/dovecot-sql.conf" % env, use_sudo=True, context=env)   
    put("postfix/spamassassin", "/etc/default/spamassassin", use_sudo=True)
    put("postfix/amavis.15-content_filter_mode", "/etc/amavis/conf.d/15-content_filter_mode", use_sudo=True)
    sudo("chown root:root /etc/amavis/conf.d/15-content_filter_mode")

def setup_dbserver():
    """ Setup database server with postgis_template db """
    sudo("aptitude update")
    sudo("aptitude -y install git-core "
                              "build-essential "
                              "libpq-dev subversion mercurial "
                              "postgresql-8.4 postgresql-server-dev-8.4")
    sudo("pg_dropcluster --stop 8.4 main")
    sudo("unset LANG && pg_createcluster --start -e UTF-8 8.4 main")
    sudo("mkdir /var/lib/postgresql/8.4/main/pg_log")
    sudo("chown postgres:postgres /var/lib/postgresql/8.4/main/pg_log")
    configure_dbserver()
                              
def configure_dbserver():
    put("postgresql/pg_hba.conf",
        "/etc/postgresql/8.4/main/pg_hba.conf" % env,
        use_sudo=True)
    put("postgresql/postgresql.conf",
        "/etc/postgresql/8.4/main/postgresql.conf" % env,
        use_sudo=True)
    sudo("invoke-rc.d postgresql-8.4 restart")
    time.sleep(7)

def setup_webserver():
    """
    Set up (bootstrap) a new server.
    
    This essentially does all the tasks in the script done by hand in one
    fell swoop. In the real world this might not be the best way of doing
    this -- consider, for example, what the various creation of directories,
    git repos, etc. will do if those things already exist. However, it's
    a useful example of a more complex Fabric operation.
    """

    # Initial setup and package install.
    sudo("aptitude update")
    sudo("aptitude -y install git-core python-dev python-setuptools "
                              "postgresql-dev postgresql-client build-essential "
                              "libpq-dev subversion mercurial "
                              "nginx "
                              "python-pip")

    files.upload_template("nginx/nginx_webserver.conf", "%(nginx_confdir)snginx.conf" % env, use_sudo=True, context=env)
    sudo("mkdir -p %(nginx_confdir)ssites-enabled" % env)

 
def setup_webapp():
    """ Setup virtualenv/startup scripts/configs for webapp """
    sudo("pip install -U virtualenv")
    run("virtualenv /home/%(user)s/%(project_name)s --distribute" % env)
    run("mkdir -p /home/%(user)s/%(project_name)s" % env)
    run("mkdir -p /home/%(user)s/static" % env)
    run("mkdir -p /home/%(user)s/static/media" % env)
    files.upload_template("nginx/nginx_webapp.conf", "%(nginx_confdir)ssites-enabled/%(servername)s.conf" % env, use_sudo=True, context=env)

def setup_celery():
    sudo("aptitude update")
    sudo("aptitude -y install python-software-properties")
    sudo("sudo add-apt-repository \"deb http://www.rabbitmq.com/debian/ testing main\"")
    run("wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc")
    sudo("apt-key add rabbitmq-signing-key-public.asc")
    sudo("aptitude update")
    sudo("aptitude -y install rabbitmq-server")
    configure_celery()
    
def configure_celery():
    sudo("rabbitmqctl add_user %(db_user)s %(db_password)s" % env)
    sudo("rabbitmqctl add_vhost %(db_name)s" % env)
    sudo("rabbitmqctl set_permissions -p %(db_name)s %(db_user)s  \".*\" \".*\" \".*\"" % env)

def setup_memcached():
    sudo("aptitude -y install memcached")
    put("memcached/memcached", "/etc/init.d/memcached", use_sudo=True)
    sudo("chown root:root /etc/init.d/memcached")
    sudo("chmod 755 /etc/init.d/memcached")
    put("memcached/start-memcached", "/usr/share/memcached/scripts/start-memcached", use_sudo=True)
    sudo("chown root:root /usr/share/memcached/scripts/start-memcached")
    sudo("chmod 755 /usr/share/memcached/scripts/start-memcached")
    configure_memcached()

def configure_memcached():
    files.upload_template("memcached/memcached.conf", "/etc/memcached_%(user)s.conf" % env, use_sudo=True, context=env)

def setup_supervisord():
    sudo("aptitude update")
    sudo("aptitude -y install supervisor")   
    
def configure_supervisor_gunicorn():
    files.upload_template("supervisor/gunicorn_supervisor.conf", "/etc/supervisor/conf.d/gunicorn_%(user)s.conf" % env, use_sudo=True, context=env)
    sudo("killall -HUP supervisord")

def add_db(dbname, owner, template=''):
    """ Add database: add_db:dbname,owner,<template> """
    if template:
        template = ' TEMPLATE %s' % template
    sudo('psql -c "CREATE DATABASE %s%s ENCODING \'unicode\' OWNER %s" -d postgres -U %s' % (dbname, template, owner, env.postgres_user or 'postgres'))

def add_dbuser(user, passwd):
    """ Add database user: add_dbuser:user,password """
    with settings(warn_only=True):
        sudo('psql -c "CREATE USER %s WITH NOCREATEDB NOCREATEUSER PASSWORD \'%s\'" -d postgres -U %s' % (user, passwd, env.postgres_user or 'postgres'))
    
def configure_db():
    """ Set up webapps database """
    add_dbuser(env.db_user, env.db_password)
    add_db(env.db_name, env.db_user)

def syncdb():
    """ Run syncdb """
    run(create_manage_command("syncdb --noinput --all"))

def migrate(arg=''):
    """ Run migrate """
    run(create_manage_command("migrate %s" % arg))

def rebuild_index():
    """ Run rebuild_index """
    manage("rebuild_index")

def add_site():
    """ Add example django site """
    run(python("from django.contrib.sites.models import Site;Site.objects.create(domain='%(servername)s', name='%(project_name)s')" % env))
    
def add_superuser():
    """ Add django superuser """
    run(python("from django.contrib.auth.models import User;User.objects.create_superuser('%(db_user)s', '%(db_user)s@%(servername)s', '%(db_password)s')" % env))
    
def dump_database():
    run("%(pg_dump)s -U %(db_user)s -O -x -c %(db_name)s > /home/%(user)s/fab_dmp.sql" % env)
    get("/home/%(user)s/fab_dmp.sql" % env, "../fab_dmp.sql")
    run("rm /home/%(user)s/fab_dmp.sql" % env)

def load_database():
    put("../fab_dmp.sql", "/home/%(user)s/fab_dmp.sql" % env)
    run("cat /home/%(user)s/fab_dmp.sql | %(psql)s -U %(db_user)s %(db_name)s" % env)
    run("rm /home/%(user)s/fab_dmp.sql" % env)

def dump_media():
    run("cd %(mediaroot)s && tar czvf /home/%(user)s/fab_media.tar.gz *" % env)
    get("/home/%(user)s/fab_media.tar.gz" % env, "../fab_media.tar.gz")
    run("rm /home/%(user)s/fab_media.tar.gz" % env)

def load_media():
    put("../fab_media.tar.gz", "/home/%(user)s/fab_media.tar.gz" % env)
    run("cd %(mediaroot)s && tar xzvf /home/%(user)s/fab_media.tar.gz" % env)
    run("rm /home/%(user)s/fab_media.tar.gz" % env)
