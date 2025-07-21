#!/bin/sh

#It runs the migrations after each update and running the file or else prod won't be updated.
flask db upgrade

exec gunicorn --bind 0.0.0.0:80 "app:create_app()"