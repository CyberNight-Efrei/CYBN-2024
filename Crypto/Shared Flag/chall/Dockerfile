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
EXPOSE 3002

# Switch to non-root user
USER nobody

# Set flag
ENV FLAG="CYBN{5m4ll_Gr0up5_c4n_0pt1m1s3_Brut3F0rc3}"

# Run supervisord
CMD ["socat", "-dd", "TCP-LISTEN:3002,reuseaddr,fork", "exec:python -u /app/app.py"]