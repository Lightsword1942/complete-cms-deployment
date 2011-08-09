
extra_paths = ':'.join([
    '/home/%(user)s/%(project_name)s/local_apps',
    '/home/%(user)s/%(project_name)s/project',
    '/home/%(user)s/%(project_name)s/project/%(project_name)s'
])
global_settings = {
    'django_debug': 'True',
    'project_name': 'cms_example',
    'root': '/home/%(user)s/%(project_name)s',
    'db_user': 'cms_example',
    'db_password': 'itisasecret',
    'db_host': 'localhost',
    'extra_paths': extra_paths,
    'use_nginx': 'true',
    'nginx_user': 'www-data',
    'nginx_confdir': '/etc/nginx/',
    'nginx_pidfile': '/var/run/nginx.pid',
    'nginx_bin': '/usr/sbin/nginx',
    'gunicorn_host': '127.0.0.1',
    'extra_settings': '',
    'staticroot': '/home/%(user)s/static',
    'mediaroot': '/home/%(user)s/static/media',
    'pg_dump': '/usr/bin/pg_dump',
    'psql': '/usr/bin/psql',
    'postgres_user': 'postgres',
    'solr_cores': 'develop' # 'develop,staging,production'
}

group_settings = {

    'vagrantdevelop': {
        'key_filename': '/home/vagrant/vagrant.ppk',
        'servername': 'develop.cms-example.com',
        'gunicorn_port': '8001',
        'gunicorn_autostart': 'true',
        'db_name': 'develop_cms_example',
        'postfix_hostname': 'cms-example.com',
        'memcached_port': '11214',
        'solr_cores': 'develop',
        'solr_core': 'develop'
    },

}

servers = {
#   'role', [
#       ['me@server:port', 'settings_group']
#   ],
    'vagrant': [['vagrant@127.0.0.1:22', 'vagrantdevelop']]
}