#!/bin/bash

docker run --detach --name core \
    --cap-add=ALL --publish 22 \
    --publish 50051 --privileged \
    --volume /lib/modules:/lib/modules \
    --volume $PWD:/opt \
    devdkerr/core

docker cp /home/$USER/.ssh/id_rsa.pub core:/root/.ssh/authorized_keys
docker exec core chmod 600 /root/.ssh/authorized_keys
docker exec core chown root:root /root/.ssh/authorized_keys

ssh -i /home/$USER/.ssh/id_rsa \
    -p $(docker inspect --format='{{ (index (index .NetworkSettings.Ports "22/tcp") 0).HostPort }}' core) \
    -X root@localhost\
    core-gui