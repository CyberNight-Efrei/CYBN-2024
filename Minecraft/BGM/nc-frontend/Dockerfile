FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get -y --no-install-recommends install socat \ 
    && rm -rf /var/lib/apt/lists/*

COPY src .

RUN chmod -R 755 /app

EXPOSE 1001

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ENV FLAG="CYBN{y0u'r3_gOnn4_M4Ke_m3_CrY_w1tH_Th3S3_z3_SK1llz}"

# Run netcat server
ENTRYPOINT ["/bin/sh","/app/entrypoint.sh"]