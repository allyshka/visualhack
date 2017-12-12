FROM ubuntu:latest
LABEL TaskName="pocexim"

ARG HOST_DOMAIN
ENV HOST_DOMAIN ${HOST_DOMAIN:-pocexim.visualhack}
ENV HOST_NAME ${HOST_SCHEME}${HOST_DOMAIN}

WORKDIR /root/
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install --no-install-recommends -y apt-utils
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
	nano \
	wget \
	python \
	python-dev \
	python-pip

RUN wget "https://bugs.exim.org/attachment.cgi?id=1052" -O poc_v1.py && wget "https://bugs.exim.org/attachment.cgi?id=1049" -O poc_v2.py && pip install --upgrade pip && pip install pwntools