#!/bin/bash

export PYTHONPATH=../Common:.${PYTHONPATH:+:$PYTHONPATH}
exec gunicorn --bind :8080 --workers 8 --access-logfile - --preload bkr.server.wsgi:application
