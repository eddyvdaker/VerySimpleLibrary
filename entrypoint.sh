#!/bin/sh

# wait for DB container to be up
sleep 5

gunicorn -b 0.0.0.0:5000 manage:app