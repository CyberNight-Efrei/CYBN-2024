FROM python:3.12-slim

WORKDIR /challenge

RUN apt-get update \
    && apt-get -y --no-install-recommends install graphviz \
    && rm -rf /var/lib/apt/lists/*

COPY ./src ./src
COPY ./entrypoint.sh .
COPY ./requirements.txt .

RUN python3 -m pip install --no-cache-dir -r requirements.txt \
	&& groupadd challenge \
    && useradd --no-create-home -d /challenge -g challenge challenge \
    && chown -R challenge:challenge /challenge/ \
    && chmod -R 755 /challenge/

ENV LISTEN_PORT=8000

ENV FLAG="CYBN{Wh@t_A_cRAzy_PaRS3r}"

RUN echo "${FLAG}" > /flag

EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
