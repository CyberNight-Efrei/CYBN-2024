FROM ubuntu:22.04

USER root

# Install required tools.
RUN apt-get -qq update \
    && apt-get -qq --no-install-recommends install sudo \
    && apt-get -qq --no-install-recommends install gcc \
    && apt-get -qq --no-install-recommends install libc-bin \
    && apt-get -qq --no-install-recommends install binutils-multiarch \
    && apt-get -qq --no-install-recommends install nano \
    && apt-get -qq --no-install-recommends install build-essential \
    && apt-get -qq --no-install-recommends install openssh-server \
    && apt-get -qq clean    \
    && rm -rf /var/lib/apt/lists/*

# Setup the default marche.

RUN useradd -rm -d /home/marche6 -s /bin/bash marche6
RUN echo 'marche6:marche6' | chpasswd

RUN useradd -rm -d /home/marche7 -s /bin/bash marche7
RUN echo 'marche7:TheBigestAndLongestPasswordisFormarche7' | chpasswd

RUN useradd -rm -d /home/marche8 -s /bin/bash marche8
RUN echo 'marche8:WhatAGreatAnWonderfulPasswordFormarche8' | chpasswd

RUN useradd -rm -d /home/marche9 -s /bin/bash marche9
RUN echo 'marche9:AmazingAndAstonishingPasswodFormarche9' | chpasswd

RUN useradd -rm -d /home/marche10 -s /bin/bash marche10
RUN echo 'marche10:SucculentDesirableAndMarvelousPasswordmarche10' | chpasswd

USER marche6

COPY prog6 /home/marche6/prog
COPY prog.c /home/marche6/prog.c
COPY bashrc /home/marche6/.bashrc

USER marche7

COPY prog7 /home/marche7/prog
COPY prog.c /home/marche7/prog.c
COPY bashrc /home/marche7/.bashrc
#RUN echo 'TheBigestAndLongestPasswordisFormarche7' > /home/marche7/.password

USER marche8

COPY prog8 /home/marche8/prog
COPY prog.c /home/marche8/prog.c
COPY bashrc /home/marche8/.bashrc
# RUN echo 'WhatAGreatAnWonderfulPasswordFormarche8' > /home/marche8/.password

USER marche9

COPY prog9 /home/marche9/prog
COPY prog.c /home/marche9/prog.c
COPY bashrc /home/marche9/.bashrc
# RUN echo 'AmazingAndAstonishingPasswodFormarche9' > /home/marche9/.password

USER marche10

COPY bashrc /home/marche10/.bashrc

# RUN echo 'SucculentDesirableAndMarvelousPasswordmarche10' > /home/marche10/.password
RUN echo "CYBN{Sh@r3d_0bj3Ct_i5_FuN_t0_3Xpl0I7}" > /home/marche10/flag.txt

# Configure permissions
USER root

COPY libmyrandom.so /usr/lib/libmyrandom.so

RUN chown marche6:marche6 /home/marche6/*
RUN chmod 755 /home/marche6
RUN chown marche7:marche6 /home/marche6/prog
RUN chmod 4550 /home/marche6/prog
RUN chmod 540 /home/marche6/prog.c

RUN chown marche7:marche7 /home/marche7/*
RUN chmod 755 /home/marche7
RUN chmod 555 /home/marche7/prog
RUN chmod 540 /home/marche7/prog.c
#RUN chmod 440 /home/marche7/.password

RUN chown marche8:marche8 /home/marche8/*
RUN chmod 755 /home/marche8
RUN chown marche9:marche8 /home/marche8/prog
RUN chmod 4550 /home/marche8/prog
RUN chmod 540 /home/marche8/prog.c
RUN echo "/home/marche8/special/libs" > /etc/ld.so.conf.d/marche8.conf
RUN chmod 644 /etc/ld.so.conf.d/marche8.conf
RUN ldconfig
#RUN chmod 440 /home/marche8/.password

RUN chown marche9:marche9 /home/marche9/*
RUN chmod 755 /home/marche9
RUN chmod 555 /home/marche9/prog
RUN chmod 540 /home/marche9/prog.c
#RUN chmod 440 /home/marche9/.password

RUN chown marche10:marche10 /home/marche10/*
RUN chmod 750 /home/marche10
#RUN chmod 440 /home/marche10/.password

RUN echo 'export TERM=xterm-256color' >> /etc/profile

# Configure SSHD.
# SSH login fix. Otherwise marche is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
RUN mkdir /var/run/sshd
RUN bash -c 'install -m755 <(printf "#!/bin/sh\nexit 0") /usr/sbin/policy-rc.d'
RUN RUNLEVEL=1 dpkg-reconfigure openssh-server
RUN ssh-keygen -A -v
RUN update-rc.d ssh defaults

# Define marches as recgnised ssh marches
RUN echo 'Match User marche6' >> /etc/sshd_config
RUN echo 'Match User marche7' >> /etc/sshd_config
RUN echo 'Match User marche8' >> /etc/sshd_config
RUN echo 'Match User marche9' >> /etc/sshd_config
RUN echo 'Match User marche10' >> /etc/sshd_config
RUN echo 'Port 2224' >> /etc/ssh/sshd_config

# Configure sudo
RUN echo "marche7 ALL=(marche8) NOPASSWD: /home/marche7/prog" >> /etc/sudoers
RUN echo "Defaults:marche7 env_keep+=LD_LIBRARY_PATH" >> /etc/sudoers
RUN echo "marche8 ALL=(root) NOPASSWD: /usr/sbin/ldconfig \"\"" >> /etc/sudoers
RUN echo "marche9 ALL=(marche10) NOPASSWD:SETENV: /home/marche9/prog" >> /etc/sudoers

# Remove read and executable permissions for the users.
RUN chmod go-rx /usr/bin/passwd
RUN chmod go-rx /usr/sbin/chpasswd

# Setup default command and/or parameters.
EXPOSE 2224
CMD ["/usr/bin/sudo", "/usr/sbin/sshd", "-D", "-o", "ListenAddress=0.0.0.0"]
