#!/bin/bash

echo "Listening on port ${LISTEN_PORT}"

python -c "from src.db import init_db; init_db()"
gunicorn --bind 0.0.0.0:${LISTEN_PORT} src.app:app
