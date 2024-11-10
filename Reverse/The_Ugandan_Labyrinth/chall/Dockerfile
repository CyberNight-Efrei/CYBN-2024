FROM debian:bookworm

# Install packages
RUN apt-get update
RUN apt-get install -y supervisor

# Challenge setup
## Switch working environment
WORKDIR /app
## Add application
COPY challenge .
## Set executable
RUN chmod +x server

# Setup supervisor
COPY conf/supervisord.conf /etc/supervisord.conf

# Expose port the server is reachable on
EXPOSE 8080

# Set flag
ENV FLAG="CYBN{d4_w4y_1s_n0t_th3_34s13st_but_th3_funn13st}"

# Run supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]