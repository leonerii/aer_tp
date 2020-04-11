import socket
import time
import datetime
import threading
import struct
import sys


# IPV6Multicast group address
mcast_group = 'FF02::1'
mcast_group_ipv4 = '239.0.0.1'
local_interface = '0.0.0.0'

# Multi-cast group port
mcast_port = 9999

# Get Address Family
addrinfo = socket.getaddrinfo(mcast_group, None)[0]
addrinfo_ipv4 = socket.getaddrinfo(mcast_group_ipv4, None)[0]

nodes       = []
rt          = {}

def create_socket():
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Enable loop-back multi-cast - the local machine will also receive multicasts
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    except socket.error as sock_error:
        print(f'Socket error: {sock_error}')
        sys.exit()

    return udp_socket

def receive_message():
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Enable loop-back multi-cast - the local machine will also receive multicasts
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    except socket.error as sock_error:
        print(f'Socket error: {sock_error}')
        sys.exit()
        
    # Preparing to receive connections
    try:
        udp_socket.bind((local_interface,mcast_port))
        print(f'Node listening on port: {local_interface}:{mcast_port}')
    
    except Exception as e:
        print(f'Binding error: {e} IP: {local_interface}')
        sys.exit()
        
    # Set multicast interface to local_ip
    udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(local_interface))
    
    # Joining multicast group
    group = socket.inet_aton(mcast_group_ipv4)
    memb_req = struct.pack('4sL', group, socket.INADDR_ANY)
    udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, memb_req)
    print(f'Joining multicast group: {mcast_group_ipv4}')

    while True:
        try:
            client, header = udp_socket.recvfrom(4096)

            # descodificar o payload do pacote
            message = client.decode()
            print(f'Connected from {header[0]} with message: {message[:5]} {message[5:]}')

            # Enviar a resposta
            if message[:5] == 'hello':
                 udp_socket.sendto('Hi info received'.encode("utf-8"), header)
            else:
                 print(f'Invalid message')

        except Exception as er:
            print(er)
        
        # finally:
        #     print(f'finally {(client[5:]).decode()}')
            
def main():
    receive_message()


if __name__ == "__main__":
    main()
