#!/bin/sh

gunicorn -w ${GUNICORN_WORKER} --bind=${GUNICORN_BIND_IP}:${GUNICORN_BIND_PORT} main:app
