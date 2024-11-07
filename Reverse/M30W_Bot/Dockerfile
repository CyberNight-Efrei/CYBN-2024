FROM debian:buster-slim

WORKDIR /usr/src/app

COPY ./src .

RUN apt-get update && apt-get install build-essential curl ucspi-tcp -y
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

ENV PATH="/root/.cargo/bin:${PATH}"

RUN cargo build --release

RUN cp /usr/src/app/target/release/meowbot_c2 /usr/local/bin/meowbot_c2

EXPOSE 8080

# Set the environment variable in the runtime container
ENV FLAG="CYBN{P30pl3_h4t3_RusT_R3_l1Ke_B0tS}"

CMD ["meowbot_c2"]
