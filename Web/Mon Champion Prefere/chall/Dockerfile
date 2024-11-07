FROM python:3.11-alpine

LABEL authors="onelots"
ENV LANG="fr_FR.UTF-8"

# Challenge directory setup
## Switch working environment
WORKDIR /app
## Add application
COPY challenge .

# Python setup
## Upgrade pip
RUN python -m pip install --upgrade pip
## Install dependencies
RUN pip install -r requirements.txt
## Disable pycache
ENV PYTHONDONTWRITEBYTECODE=1

# Expose port the server is reachable on
EXPOSE 8002

# Set flag
ENV FLAG="CYBN{J3_P4TCH_C0MM3_UN_D13U}"

# Run Gunicorn on port 8002
CMD ["gunicorn", "--bind", "0.0.0.0:8002", "app:app"]
