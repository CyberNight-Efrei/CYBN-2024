FROM python:3-alpine

# Install dependencies
RUN apk add ucspi-tcp6

## Switch working environment
WORKDIR /app

## Add application
COPY src .

# Expose port the server is reachable on
EXPOSE 4000

# Set flag
ENV FLAG="CYBN{4_r3aL_pR0Gr4mm3R}"

# Run netcat server
CMD ["tcpserver", "-c", "255", "-HR", "0.0.0.0", "4000", "/usr/local/bin/python3", "app.py"]
