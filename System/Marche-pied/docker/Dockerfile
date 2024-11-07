FROM ubuntu:22.04

USER root

# Install required tools.
RUN apt-get -qq update \
    && apt-get -qq --no-install-recommends install sudo \
    && apt-get -qq --no-install-recommends install less \
    && apt-get -qq --no-install-recommends install openssh-server \
    && apt-get -qq clean    \
    && rm -rf /var/lib/apt/lists/*

# Setup the default marche.
ARG PWD_USER2=WhatAStrongPasswordFormarche2

RUN useradd -rm -d /home/marche1 -s /bin/bash marche1
RUN echo 'marche1:marche1' | chpasswd

RUN useradd -rm -d /home/marche2 -s /bin/bash marche2
RUN echo 'marche2:WhatAStrongPasswordFormarche2' | chpasswd

RUN useradd -rm -d /home/marche3 -s /bin/bash marche3
RUN echo 'marche3:CantGuessPasswordFormarche3' | chpasswd

USER marche2

RUN mkdir /home/marche2/config
RUN echo 'Incoming config... please be patient team !' > /home/marche2/config/tbd
RUN echo 'WhatAStrongPasswordFormarche2' > /home/marche2/remember_password.txt

USER marche3

RUN echo 'Here is an important message for everyone: I got ratioed. I may be absent from office for a couple of years. Thanks for your understanding.' > /home/marche3/message.txt
RUN echo 'CYBN{Mak3_SUr3_T0_coNF1Gur3_sUD0_C0rr3C7ly}' > /home/marche3/flag.txt


# Configure permissions
USER root

RUN chmod 775 /home/marche1
RUN chmod 775 /home/marche2
RUN chmod -R 770 /home/marche2/*

# Configure SSHD.
# SSH login fix. Otherwise marche is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
RUN mkdir /var/run/sshd
RUN bash -c 'install -m755 <(printf "#!/bin/sh\nexit 0") /usr/sbin/policy-rc.d'
RUN RUNLEVEL=1 dpkg-reconfigure openssh-server
RUN ssh-keygen -A -v
RUN update-rc.d ssh defaults

# Define marches as recgnised ssh marches
RUN echo 'Match User marche1' >> /etc/sshd_config
RUN echo 'Match User marche2' >> /etc/sshd_config
RUN echo 'Match User marche3' >> /etc/sshd_config
RUN echo 'Port 2222' >> /etc/ssh/sshd_config

# Configure sudo.
RUN echo "marche1 ALL=(marche2) NOPASSWD: /bin/cat /home/marche2/config/*" >> /etc/sudoers
RUN echo "marche2 ALL=(marche3) NOPASSWD: /bin/less /home/marche3/message.txt" >> /etc/sudoers

# Remove read and executable permissions for the users.
RUN chmod go-rx /usr/bin/passwd
RUN chmod go-rx /usr/sbin/chpasswd

# Setup default command and/or parameters.
EXPOSE 2222
CMD ["/usr/bin/sudo", "/usr/sbin/sshd", "-D", "-o", "ListenAddress=0.0.0.0"]
