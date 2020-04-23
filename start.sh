#!/bin/bash

LOCALHOST=$(ip addr show  eth0 | sed -e's/^.*inet6 \([^ ]*\)\/.*$/\1/;t;d' | head -1)

python3 network.py $LOCALHOST