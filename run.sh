#!/bin/bash

deploy_dir=`dirname $(readlink -f ${BASH_SOURCE[0]})`
cd $deploy_dir

. /etc/profile
. env/bin/activate
. /data/app/profile/replace-goods

exec gunicorn -c  gunicorn.py -b 0.0.0.0:50016 -w 1 -t 3 wsgi:application
