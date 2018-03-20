FROM debian:latest
LABEL TaskName="squirrelvh"

ARG HOST_DOMAIN
ENV HOST_DOMAIN ${HOST_DOMAIN:-squirrel.visualhack}

# Update and preinstall requisites && apt-get -y upgrade
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
	sendmail \
	wget \
	nano \
	apache2 \
	dovecot-core \
	dovecot-imapd \
	php

# Create download folder and download SquirrelMail distro
RUN install -d /usr/local/src/downloads
WORKDIR /usr/local/src/downloads
RUN wget http://prdownloads.sourceforge.net/squirrelmail/squirrelmail-webmail-1.4.22.tar.gz
RUN mkdir /usr/local/squirrelmail

# set needed privileges
WORKDIR /usr/local/squirrelmail
RUN mkdir data temp attach
RUN chown www-data:www-data data temp attach
# extract SquirrelMail
RUN tar xzf /usr/local/src/downloads/squirrelmail-webmail-1.4.22.tar.gz
RUN mv squirrelmail-webmail-1.4.22 www
# configure dovecot IMAP
RUN echo "protocols = imap" >> /etc/dovecot/dovecot.conf
RUN echo \!include auth-passwdfile.conf.ext >> /etc/dovecot/conf.d/10-auth.conf
# create user for using in dovecot
RUN useradd -G mail attacker
RUN install -d -g attacker -o attacker /home/attacker
RUN cat /etc/passwd|grep attacker|sed 's/x/{PLAIN}passw/; s/.$//' > /etc/dovecot/users
RUN printf 'Alias /squirrelmail /usr/local/squirrelmail/www\n<Directory /usr/local/squirrelmail>\n\tAllowOverride None\n\tRequire all granted\n</Directory>\n' >> /etc/apache2/apache2.conf
# Create SquirrelMail configuration file
RUN sed "s/domain = 'example.com'/domain = 'squirrelvh'/; s#/var/local/squirrelmail/#/usr/local/squirrelmail/#g" /usr/local/squirrelmail/www/config/config_default.php > /usr/local/squirrelmail/www/config/config.php

EXPOSE 80

# test run
CMD ["/bin/bash", "-c", "service dovecot start && service apache2 start && service sendmail start; while true; do sleep 5; done"]