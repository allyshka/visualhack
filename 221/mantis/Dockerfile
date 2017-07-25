FROM debian:latest
LABEL TaskName="mantis"

ARG MYSQL_USER
ENV MYSQL_USER ${MYSQL_USER:-mantis}
ARG MYSQL_PASS
ENV MYSQL_PASS ${MYSQL_PASS:-trdk7e0Z4G}
ARG HOST_SCHEME
ENV HOST_SCHEME ${HOST_SCHEME:-http://}
ARG HOST_DOMAIN
ENV HOST_DOMAIN ${HOST_DOMAIN:-mantis.visualhack}
ENV HOST_NAME ${HOST_SCHEME}${HOST_DOMAIN}

# Update and preinstall requisites && apt-get -y upgrade
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install --no-install-recommends -y apt-utils
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
	cron \
	curl \
	nginx \
	unzip \
	mysql-server \
	php-fpm \
	php-mysql \
	php-curl \
	php-mbstring \
	php-gd \
	php7.0-xml \
	wget \
	nano \
	screen

# nginx configs create
ADD default /etc/nginx/sites-enabled/default
RUN sed -i "s~thereisyourservername~$HOST_DOMAIN~" /etc/nginx/sites-enabled/default

# remove garbage
RUN rm -rf /var/www/html/*

# short tags enable
RUN sed -i "s~short_open_tag = Off~short_open_tag = On~" /etc/php/7.0/fpm/php.ini
# create user and allow mysql connect from any adress
RUN service mysql start && mysql -u root -e "GRANT ALL PRIVILEGES ON *.* TO '$MYSQL_USER'@'%' IDENTIFIED BY '$MYSQL_PASS';"
# change bind mysql address
RUN sed -i "s~127.0.0.1~0.0.0.0~" /etc/mysql/mariadb.conf.d/50-server.cnf

# download stuff
WORKDIR /var/www/html
RUN wget https://netix.dl.sourceforge.net/project/mantisbt/mantis-stable/2.3.0/mantisbt-2.3.0.zip && unzip mantisbt-2.3.0.zip && mv mantisbt-2.3.0/* . && rm -rf mantisbt-2.3.0
RUN wget https://github.com/vrana/adminer/releases/download/v4.3.1/adminer-4.3.1-mysql.php

# set rights
RUN chown -R www-data:www-data /var/www/html/

# HTTP
EXPOSE 80
# MySQL
EXPOSE 3306

# dirty loop exec
CMD ["/bin/bash", "-c", "service mysql start && service php7.0-fpm start && service nginx start && while true; do sleep 5; done"]