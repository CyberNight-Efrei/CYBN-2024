#!/bin/bash

echo "Listening on port ${LISTEN_PORT}"

gunicorn --bind 0.0.0.0:${LISTEN_PORT} src.app:app
