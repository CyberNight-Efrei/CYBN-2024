FROM ubuntu:22.04

USER root

# Install required tools.
RUN apt-get -qq update \
    && apt-get -qq --no-install-recommends install sudo \
    && apt-get -qq --no-install-recommends install gcc \
    && apt-get -qq --no-install-recommends install tree \
    && apt-get -qq --no-install-recommends install less \
    && apt-get -qq --no-install-recommends install nano \
    && apt-get -qq --no-install-recommends install build-essential \
    && apt-get -qq --no-install-recommends install openssh-server \
    && apt-get -qq clean    \
    && rm -rf /var/lib/apt/lists/*

# Setup the default marche.

RUN useradd -rm -d /home/marche3 -s /bin/bash marche3
RUN echo 'marche3:marche3' | chpasswd

RUN useradd -rm -d /home/marche4 -s /bin/bash marche4
RUN echo 'marche4:YoCheckThatPasswordFormarche4' | chpasswd

RUN useradd -rm -d /home/marche5 -s /bin/bash marche5
RUN echo 'marche5:JeezInsanePasswordFormarche5' | chpasswd

RUN useradd -rm -d /home/marche6 -s /bin/bash marche6
RUN echo 'marche6:OmegaBigaAndStrongPasswordFormarche6' | chpasswd

USER marche3

#RUN echo 'diff .bashrc /home/marche4/.bashrc' > /home/marche3/.bash_history

USER marche4

RUN echo 'YoCheckThatPasswordFormarche4' > '/home/marche4/do not forgor'
COPY showfile.c /home/marche4/showfile.c
RUN gcc /home/marche4/showfile.c -o /home/marche4/showfile

USER marche5

COPY tree.c /home/marche5/tree.c
RUN gcc /home/marche5/tree.c -o /home/marche5/tree
RUN echo 'JeezInsanePasswordFormarche5' > /home/marche5/.password

USER marche6

RUN mkdir /home/marche6/myapp
RUN touch /home/marche6/myapp/config
RUN touch /home/marche6/myapp/app
RUN mkdir /home/marche6/myapp/logs
RUN touch "/home/marche6/myapp/logs/2017-06-18T07:56:47"
RUN touch "/home/marche6/myapp/logs/2017-06-19T08:35:12"
RUN touch "/home/marche6/myapp/logs/2017-06-22T03:22:44"

RUN echo 'CYBN{sU1d_i5_v3Ry_s3nSIT1ve_B3_c@reFUL}' > /home/marche6/flag.txt

# Configure permissions
USER root

RUN chmod 775 /home/marche3
RUN chmod 775 /home/marche4
RUN chmod -R 770 /home/marche4/*

RUN chown root:marche4 /usr/bin/diff
RUN chmod g+s /usr/bin/diff

RUN chown marche4:marche4 /home/marche4/*
RUN chown marche5:marche4 /home/marche4/showfile
RUN chmod 440 "/home/marche4/do not forgor"
RUN chmod 4550 /home/marche4/showfile
RUN chmod 540 /home/marche4/showfile.c

RUN chown marche5:marche5 /home/marche5/*
RUN chown marche6:marche5 /home/marche5/tree
RUN chmod 4551 /home/marche5/tree
RUN chmod 540 /home/marche5/tree.c

# Configure SSHD.
# SSH login fix. Otherwise marche is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
RUN mkdir /var/run/sshd
RUN bash -c 'install -m755 <(printf "#!/bin/sh\nexit 0") /usr/sbin/policy-rc.d'
RUN RUNLEVEL=1 dpkg-reconfigure openssh-server
RUN ssh-keygen -A -v
RUN update-rc.d ssh defaults

# Define marches as recgnised ssh marches
RUN echo 'Match User marche3' >> /etc/sshd_config
RUN echo 'Match User marche4' >> /etc/sshd_config
RUN echo 'Match User marche5' >> /etc/sshd_config
RUN echo 'Port 2223' >> /etc/ssh/sshd_config

# Remove read and executable permissions for the users.
RUN chmod go-rx /usr/bin/passwd
RUN chmod go-rx /usr/sbin/chpasswd

# Setup default command and/or parameters.
EXPOSE 2223
CMD ["/usr/bin/sudo", "/usr/sbin/sshd", "-D", "-o", "ListenAddress=0.0.0.0"]
