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

ENV LISTEN_PORT=7001

ENV FLAG="CYBN{T31l_m3_Wh4T_t0_D0}"
ENV OPENAI_API_KEY="ELLE-EST-REVOQUEE-BRO-CHERCHE-PAS-:)"

EXPOSE 7001
ENTRYPOINT ["./entrypoint.sh"]
