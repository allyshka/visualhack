FROM debian
LABEL TaskName="bind"

ARG HOST_DOMAIN
ENV HOST_DOMAIN ${HOST_DOMAIN:-bind.visualhack}
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
	bind9 \
	python \
	python-pip \
	dnsutils \
	tcpdump \
	libssl-dev \
	build-essential \
	screen

# install requirements
RUN pip install dnspython==1.15.0

ADD dnspython.patch /usr/local/lib/python2.7/dist-packages
RUN cd /usr/local/lib/python2.7/dist-packages && patch -p0 < dnspython.patch

# create configs
ADD named.conf.local /etc/bind/
RUN mkdir /etc/bind/zones/
ADD bind.visualhack.db /etc/bind/zones/
RUN echo -e "search $HOST_DOMAIN\nnameserver 127.0.0.1\n$(cat /etc/resolv.conf)" > /etc/resolv.conf
ADD poc.py /root/
ADD poc-axfr.py /root/

# build vulnerable version of bind server
RUN cd /root/ && git clone --branch v9_10_5 --depth=1 https://source.isc.org/git/bind9.git

WORKDIR /root/bind9
RUN ./configure && make && make install
RUN echo 'include "/etc/bind/named.conf";' > /etc/named.conf
RUN cp /usr/local/sbin/named /usr/sbin/named

EXPOSE 53

# test run
CMD ["/bin/bash", "-c", "service bind9 start && while true; do sleep 5; done"]