docker build -t squirrelvh .
docker run -td -p80:80 --rm --name=squirrelvh --hostname=squirrelvh squirrelvh