import socket
from json import dumps


def udp_create_socket():
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    return sock
    
def udp_data(msg, addr, port):
    sock = udp_create_socket()
    sock.sendto(dumps(msg).encode('utf-8'), (addr, port))
    sock.close()