import socket
from json import dumps


def create_socket():
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    return sock
    
def send_unicast(msg, uni_addr, mcast_port):
    sock = create_socket()
    sock.sendto(dumps(msg).encode('utf-8'), (uni_addr, mcast_port))