docker build -t exim4 .
docker run --rm -ti -p25:25 --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --name=exim4 --hostname=exim4 exim4 /bin/bash