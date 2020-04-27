import socket
import netifaces
import uuid
from json import dumps

def create_socket():
    try:
        client_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        client_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, 1)

        return client_sock

    except Exception as sock_error:
        print('Failed to create socket: {}'.format(sock_error))

def get_ip():
    ipv6 = netifaces.ifaddresses('eth0')

    return ipv6[netifaces.AF_INET6][0]['addr']

def send_multicast(msg, mcast_addr, mcast_port):
    ipv6 = get_ip()
    try:
        sock = create_socket()
        
        sock.sendto(dumps(msg).encode('utf-8'), (mcast_addr, mcast_port))

    except Exception as e:
        print(e)

    finally:
        sock.close()

#send_multicast(mcast_port=9999)
