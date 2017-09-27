docker build -t joomla375 .
docker run -p80:80 -p3306:3306 --name=joomla --hostname=joomla joomla375