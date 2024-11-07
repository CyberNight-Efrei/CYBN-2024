FROM python:3.12-slim

WORKDIR /challenge

COPY ./src ./src
COPY ./entrypoint.sh .
COPY ./requirements.txt .

RUN python3 -m pip install --no-cache-dir -r requirements.txt \
	&& groupadd challenge \
    && useradd --no-create-home -d /challenge -g challenge challenge \
    && chown -R challenge:challenge /challenge/ \
    && chmod -R 755 /challenge/

ENV LISTEN_PORT=6000

ENV FLAG="CYBN{W4sh1ng_f0r_r33F}"

EXPOSE 6000
ENTRYPOINT ["./entrypoint.sh"]
