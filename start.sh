LOCALHOST=$(ip addr show  eth0 | sed -e's/^.*inet6 \([^ ]*\)\/.*$/\1/;t;d' | tail -1)

python3 network.py $LOCALHOST