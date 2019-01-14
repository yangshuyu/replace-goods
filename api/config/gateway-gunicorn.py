import os
import eventlet
eventlet.monkey_patch()

import multiprocessing

import gunicorn

reload = False
loglevel = 'info'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(D)s %(f)s %(a)s'
errorlog = '-'

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = ''
