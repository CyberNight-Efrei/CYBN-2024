FROM python:3.12.4-slim

# Install packages
RUN apt update
RUN apt install -y socat

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

# Expose port the server is reachable on
EXPOSE 3001

# Switch to non-root user
USER nobody

# Set flag
ENV FLAG="CYBN{REDACTED_SECURE_CHAIN}"

# Run supervisord
CMD ["socat", "-dd", "TCP-LISTEN:3001,reuseaddr,fork", "exec:python -u /app/app.py"]