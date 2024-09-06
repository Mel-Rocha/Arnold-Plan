import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

bind = '0.0.0.0:8000'
workers = 2
threads = 2

# Configurações adicionais
worker_class = 'sync'
worker_connections = 1000
timeout = 300
keepalive = 2
max_requests = 10000

# Configuração de logs
loglevel = 'info'
errorlog = '/var/log/access.log'
accesslog = '/var/log/error.log'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'


def post_fork(server, worker):
    pass
