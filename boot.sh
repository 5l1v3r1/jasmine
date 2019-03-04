#!/usr/bin/env bash

function run() {
   gunicorn -b  0.0.0.0:5000 --access-logfile - --error-logfile - run:app

}

function deploy() {
   ssh  ubuntu@111.231.82.45 "cd /home/ubuntu/flask_project/jasmine; git pull"
   ssh  ubuntu@111.231.82.45 "cd /home/ubuntu/flask_project/jasmine; /home/ubuntu/miniconda3/bin/docker-compose up -d --build"
}
function run_celery() {
    celery worker -B -A run_celery.celery --loglevel=info
}

function migrate() {
flask user create_user
}

Action=$1
shift
 case "$Action" in
 run)
    run ;;
 deploy)
    deploy;;
 run_celery)
 run_celery;;
 migrate)
 migrate;;
    *) echo 'usage:
     runserver: ./boot.sh run
     update code and deploy: ./boot.sh deploy
     run celery worker    ./boot.sh run_celery
     migrate data       ./boot.sh migrate
     ' ;;

esac
