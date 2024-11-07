FROM python:3.12-slim

WORKDIR /challenge

RUN apt-get update \
    && rm -rf /var/lib/apt/lists/*

COPY ./src ./src
COPY ./entrypoint.sh .
COPY ./schema.sql .
COPY ./requirements.txt .

RUN python3 -m pip install --no-cache-dir -r requirements.txt \
        && groupadd challenge \
    && useradd --no-create-home -d /challenge -g challenge challenge \
    && chown -R challenge:challenge /challenge/ \
    && chmod -R 755 /challenge/

ENV LISTEN_PORT=8003

ENV FLAG1="CYBN{Wh4t_4_w31rd_w4y"
ENV FLAG2="_t0_st0r3_d4t4}"

RUN echo "partie 2 du flag: ${FLAG2}" > /flag


EXPOSE 8003
ENTRYPOINT ["./entrypoint.sh"]
