#!/usr/bin/env bash

#
#
#. /Users/fanjialiang2401/Anacoda/anaconda2/etc/profile.d/conda.sh conda activate jasmine
#
#pip -V
#pip list
##pip install -r requirements/requirements.txt
#
#sh ./setup_mysql.sh create
#
#
#gunicorn -c gunicorn.py jasmine:app
setup_mysql.sh start

chmod +x ./boot_python.sh

if [[ $? == "0" ]]; then
    echo "success"
else  echo"false"
exit $?
fi

setup_redis.sh start
if [[ $? == "0" ]]; then
    echo "success"
else  echo"false"
exit $?
fi

./boot_python.sh

