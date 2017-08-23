FROM debian:8
LABEL TaskName="processmaker"

ARG MYSQL_USER
ENV MYSQL_USER ${MYSQL_USER:-processmaker}
ARG MYSQL_PASS
ENV MYSQL_PASS ${MYSQL_PASS:-trdk7e0Z4G}
ARG HOST_SCHEME
ENV HOST_SCHEME ${HOST_SCHEME:-http://}
ARG HOST_DOMAIN
ENV HOST_DOMAIN ${HOST_DOMAIN:-processmaker.visualhack}
ENV HOST_NAME ${HOST_SCHEME}${HOST_DOMAIN}

# Update and preinstall requisites && apt-get -y upgrade
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install --no-install-recommends -y apt-utils
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
	cron \
	curl \
	apache2 \
	unzip \
	mysql-server \
	libapache2-mod-php5 \
	php5-fpm \
	php5-mysql \
	php5-curl \
	php5-gd \
	php5-mcrypt \
	php5-ldap \
	wget \
	nano \
	screen

# apache configs create
ADD pmos.conf /etc/apache2/sites-enabled/pmos.conf
RUN sed -i "s~thereisyourservername~$HOST_DOMAIN~" /etc/apache2/sites-enabled/pmos.conf
# add part of config
ADD apache.part.conf /tmp/apache.part.conf
RUN a2enmod rewrite && cat /tmp/apache.part.conf >> /etc/apache2/apache2.conf

# remove garbage
RUN rm -rf /var/www/html/*

# create user and allow mysql connect from any adress
RUN service mysql start && mysql -u root -e "GRANT ALL ON *.* TO '$MYSQL_USER'@'%' identified by '$MYSQL_PASS' WITH GRANT OPTION;"
# change bind mysql address
RUN sed -i "s~127.0.0.1~0.0.0.0~" /etc/mysql/my.cnf

# download stuff
WORKDIR /opt
RUN wget https://netcologne.dl.sourceforge.net/project/processmaker/ProcessMaker/3.0.1.5/processmaker-3.0.1.5-community.tar.gz && tar xvzf processmaker-3.0.1.5-community.tar.gz && rm -rf processmaker-3.0.1.5-community.tar.gz
RUN chmod 770 /opt/processmaker/shared && cd /opt/processmaker/workflow/engine/ && chmod 770 config content/languages plugins xmlform js/labels && chown -R www-data:www-data /opt/processmaker

# HTTP
EXPOSE 80
# MySQL
EXPOSE 3306

# dirty loop exec
CMD ["/bin/bash", "-c", "service mysql start && service apache2 start && while true; do sleep 5; done"]