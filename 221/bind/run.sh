docker build -t bind .
docker run -ti --name=bindvh --hostname=bindvh --cap-add DAC_READ_SEARCH --cap-add SYS_RESOURCE bind /bin/bash