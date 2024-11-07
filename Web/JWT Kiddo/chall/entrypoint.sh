#!/bin/sh

# Secure entrypoint
chmod 600 /entrypoint.sh

# Create keys directories
mkdir -p /app/private/keys
mkdir -p /app/public/keys

# Generate keys
openssl genrsa -out /app/private/keys/key-0.pem 2048
openssl rsa -in /app/private/keys/key-0.pem -pubout -out /app/public/keys/key-0.pem

/usr/bin/supervisord -c /etc/supervisord.conf