from json import dumps, loads
from time import sleep
from uuid import uuid4
import socket


def create_socket():
    try:
        client_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        client_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, 1)
        
        return client_sock
        
    except Exception as sock_error:
        print('Failed to create socket: {}'.format(sock_error))

def run():
    try:
        input_data = input('Type your message: ')
        dest = input('Destination address: ')

        sock = create_socket()
        msg = {
            'type': 'DATA',
            'id': uuid4(),
            'data': input_data,
            'dest': dest,
            'ttl': 30,
            'port': sock.getsockname()[1]
        }

        sock.sendto(dumps(msg).encode('utf-8'), ('::1', 9999))
    except Exception as e:
        print(e.with_traceback())

    finally:
        sock.close()





