#!/usr/bin/env bash

mysql -uroot -P 3305 -h 127.0.0.1 jasmine < jasmine.sql

echo $?

