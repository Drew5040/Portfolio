#!/bin/bash

# Start Nginx
service nginx start

# Start Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
