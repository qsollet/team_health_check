#!/bin/sh

# Can use only one worker as using a global variable
gunicorn -w 1 -b 0.0.0.0:8080 main:app
