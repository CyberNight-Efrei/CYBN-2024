FROM python:3.12.4-slim

# Install packages
RUN apt update
RUN apt install -y supervisor openssl

# Challenge directory setup
## Switch working environment
WORKDIR /app
## Add application
COPY challenge .

# Python setup
## Upgrade pip
RUN python -m pip install --upgrade pip
## Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
## Disable pycache
ENV PYTHONDONTWRITEBYTECODE=1

# Setup supervisor
COPY conf/supervisord.conf /etc/supervisord.conf

# Expose port the server is reachable on
EXPOSE 8001

# Set flag
ENV FLAG="CYBN{h4ck3r_2_h4ck3r5}"

# Run entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]