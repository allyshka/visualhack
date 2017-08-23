docker build -t pmk .
docker run -ti -p80:80 -p3306:3306 --name=pmkvh --hostname=pmkvh pmk /bin/bash