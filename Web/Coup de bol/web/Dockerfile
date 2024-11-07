FROM ubuntu:latest AS production

WORKDIR /build

# /// deps flag 1 & 2

RUN apt-get update 
RUN apt-get install -qy \
wget \
lzip \
make \
gcc \
libgmp3-dev \
libdb-dev \
curl \
python-is-python3 \
git

RUN wget https://kumisystems.dl.sourceforge.net/project/gnucobol/gnucobol/3.2/gnucobol-3.2.tar.lz \
&& tar --lzip -xf gnucobol-3.2.tar.lz

RUN cd gnucobol-3.2 && ./configure && make && make install

# /// deps flag 3

RUN apt-get install -qy \
software-properties-common \
sudo \
zip
RUN add-apt-repository ppa:ondrej/php 
RUN apt-get install -qy \
php5.6 \
php5.6-json \
php5.6-pdo \
php5.6-sqlite \
php5.6-iconv \
php5.6-yaml \
php5.6-ctype \
php5.6-dom \
php5.6-cgi \
php5.6-tokenizer

# /// deps general

RUN apt-get install -qy supervisor

ENV IS_DOCKER=true

# ////////////////////////////////////////////////////////////////////////////////

FROM production AS build-flag2

RUN apt-get update && apt-get install -qy python-is-python3 git

WORKDIR /app/kobe
COPY ./kobe /app/kobe

# "Ju57_4_s1mpl3_X0R" xoré avec HELLO
ENV FLAG2="0230797b107c1a3f7d2238297f13177817"

RUN python generate-flag2.py

RUN ./downhill.sh

RUN git config --global user.email "c.baul@bank.arpa"
RUN git config --global user.name "Colin BAUL"

RUN git add runner/the.cow
RUN git commit -m "add binary"


# ////////////////////////////////////////////////////////////////////////////////

FROM production AS build-flag3

WORKDIR /app/synforme

COPY ./synforme /app/synforme

RUN ./init.sh

RUN echo "CYBN{Fully_pwn3d_m4ch1n3}" > /root/flag3

# ////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////////

FROM production

RUN apt-get update && apt-get install -qy apache2

WORKDIR /app/kobe

COPY ./confs /app/confs

COPY --from=build-flag2 /app/kobe /app/kobe
COPY --from=build-flag2 /app/kobe/views /app/kobe/runner/views
RUN cp -R /app/kobe/.git /app/kobe/runner/.git

COPY --from=build-flag3 /app/synforme /app/synforme
COPY --from=build-flag3 /root/flag3 /root/flag3


ENV FLAG1="CYBN{D3v3l0pm3n7_r3s0urc3s_c4n_b3_us3fu1}"

RUN echo "$FLAG1" > /tmp/flag1

EXPOSE 80

CMD [ "-c", "/app/confs/supervisord.conf" ]

ENTRYPOINT [ "/usr/bin/supervisord" ]
