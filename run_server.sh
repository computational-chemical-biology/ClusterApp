#!/bin/bash
#export FLASK_ENV=development
#python3 ./main.py

# gunicorn -w 4 -b 0.0.0.0:5004 --timeout 3600 api.app:app
gunicorn -w 4 -b 0.0.0.0:5004 --timeout 3600 api.app:app
