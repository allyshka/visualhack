# CVE-2017-16943 and CVE-2017-16944 vulnerability stand
FROM ubuntu:latest
LABEL TaskName="exim4"

ARG HOST_DOMAIN
ENV HOST_DOMAIN ${HOST_DOMAIN:-exim4.visualhack}
ENV HOST_NAME ${HOST_SCHEME}${HOST_DOMAIN}

# Update and preinstall requisites && apt-get -y upgrade
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install --no-install-recommends -y apt-utils
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
	git \
	cron \
	curl \
	unzip \
	wget \
	nano \
	python \
	python-pip \
	python-dev \
	dnsutils \
	tcpdump \
	libssl-dev \
	build-essential \
	gdb \
	procps \
	netcat \
	libdb-dev \
	libpcre3-dev \
	screen

WORKDIR /root/
# RUN wget https://github.com/Exim/exim/archive/exim-4_89.tar.gz && tar xvzf exim-4_89.tar.gz && mv exim-exim-4_89/ exim489
# RUN wget "https://bugs.exim.org/attachment.cgi?id=1052" -O poc.py && pip install pwntools
# Create required users for mailer daemon
RUN groupadd -g 31 exim && useradd -d /dev/null -c "Exim Daemon" -g exim -s /bin/false -u 31 exim
RUN git clone --branch exim-4_89 https://github.com/Exim/exim.git --depth=1
WORKDIR /root/exim/src/
RUN mkdir Local && wget "https://bugs.exim.org/attachment.cgi?id=1051" -O Local/Makefile && sed -ie 's,^EXIM_USER.*$,EXIM_USER=exim,' Local/Makefile  && \
    printf "CFLAGS  += -g\n" >> Local/Makefile
RUN make && make install && \
	ln -sfv exim /usr/sbin/sendmail && \
	install -v -d -m750 -o exim -g exim /var/spool/exim

EXPOSE 25

# test run
CMD ["/bin/bash", "-c", "while true; do sleep 5; done"]