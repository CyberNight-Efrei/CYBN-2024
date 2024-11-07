FROM python:3.12-slim

WORKDIR /challenge

RUN apt-get update \
    && apt-get -y --no-install-recommends install socat less \
    && rm -rf /var/lib/apt/lists/*

COPY ./challenge.py .
COPY ./entrypoint.sh .
COPY ./requirements.txt .

RUN python3 -m pip install --no-cache-dir -r requirements.txt \
	&& groupadd challenge \
    && useradd --no-create-home -d /challenge -g challenge challenge \
    && chown -R challenge:challenge /challenge/ \
    && chmod -R 755 /challenge/

ENV LISTEN_PORT=7000
ENV FLAG=${FLAG}

RUN echo "CYBN{D4mn_th4t_p4yl04d_1s_hug3}" > /flag

EXPOSE 7000
ENTRYPOINT ["./entrypoint.sh"]
