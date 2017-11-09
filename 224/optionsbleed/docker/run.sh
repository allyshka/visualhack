docker build -t apache2425 .
docker run --cap-add=SYS_PTRACE --security-opt seccomp=unconfined -d -p80:80 --name=obleed --hostname=optionsbleed apache2425
