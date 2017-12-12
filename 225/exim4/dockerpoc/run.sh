docker build -t eximpoc .
docker run --rm -ti --link=exim4 --name=eximpoc --hostname=eximpoc eximpoc /bin/bash