#!/bin/bash

rm db.sqlite3
rm -rf ./sharkapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations sharkapi
python3 manage.py migrate sharkapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens

