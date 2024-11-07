FROM python:3.12.4-slim

# Install packages
RUN apt update
RUN apt install -y supervisor

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
EXPOSE 4000

# Set flag
ENV FLAG="CYBN{REDACTED_CAPTCHA_1}"

# Run supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]