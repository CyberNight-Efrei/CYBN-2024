FROM python:3-alpine

WORKDIR /app

COPY src .

RUN chmod a+x entrypoint.sh

EXPOSE 1001

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ENV FLAG="CYBN{y0u'r3_gOnn4_M4Ke_m3_CrY_w1tH_Th3S3_z3_SK1llz}"

# Run netcat server
ENTRYPOINT ["/bin/sh","/app/entrypoint.sh"]