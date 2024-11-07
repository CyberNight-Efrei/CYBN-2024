#!/bin/bash

echo "Listening on port ${LISTEN_PORT}"

gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:${LISTEN_PORT} src.app:app
