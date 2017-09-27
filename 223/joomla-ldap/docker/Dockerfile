FROM debian:latest
LABEL TaskName="joomla"

ARG MYSQL_USER
ENV MYSQL_USER ${MYSQL_USER:-joomla}
ARG MYSQL_PASS
ENV MYSQL_PASS ${MYSQL_PASS:-SGKz6BRgaC}
ARG HOST_SCHEME
ENV HOST_SCHEME ${HOST_SCHEME:-http://}
ARG HOST_DOMAIN
ENV HOST_DOMAIN ${HOST_DOMAIN:-joomla.visualhack}
ENV HOST_NAME ${HOST_SCHEME}${HOST_DOMAIN}

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install --no-install-recommends -y apt-utils
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
	ldap-server \
	mysql-server \
	apache2 \
	slapd \
	ldap-utils \
	ldapscripts \
	php \
	php-xml \
	php-mysqli \
	php-ldap \
	php-mcrypt \
	git \
	wget \
	nano \
	screen

# joomla.visualhack
# vh
# secretpasswd

# short tags enable
RUN sed -i "s~short_open_tag = Off~short_open_tag = On~" /etc/php/7.0/apache2/php.ini
# create user and allow mysql connect from any adress
RUN service mysql start && mysql -u root -e "CREATE DATABASE $MYSQL_USER; GRANT ALL PRIVILEGES ON *.* TO '$MYSQL_USER'@'%' IDENTIFIED BY '$MYSQL_PASS';"
# change bind mysql address
RUN sed -i "s~127.0.0.1~0.0.0.0~" /etc/mysql/mariadb.conf.d/50-server.cnf

WORKDIR /var/www/html
RUN rm index.html && wget "https://downloads.joomla.org/cms/joomla3/3-7-5/Joomla_3-7.5-Stable-Full_Package.tar.gz?format=gz" && mv "Joomla_3-7.5-Stable-Full_Package.tar.gz?format=gz" j.tar.gz
RUN tar xvzf "j.tar.gz"
RUN chown -R www-data:www-data /var/www/html/


EXPOSE 80
EXPOSE 3306

# dirty loop exec
CMD ["/bin/bash", "-c", "service mysql start && service apache2 start && while true; do sleep 5; done"]