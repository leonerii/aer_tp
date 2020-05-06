import socket
from json import dumps
from time import time

class TCPServerHandler()

    # def create_socket(self):
        
    #         try:
    #             client_sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    #             client_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, self.ttl)
                
    #             return client_sock
            
    #         except Exception as sock_error:
    #             print('Failed to create socket: {}'.format(sock_error))

    def request_handler(self):
        
        # sock = create_socket()
        if self.msg['dest'] == self.localhost:
            if self.msg['data']['type']] == 'POST':
                print('Save data to the database')
                self.database[self.msg['data']['data']['rodovia']] = self.msg['data']['data']
                
                # Change src and dest
                self.msg['dest'] = self.msg['source']
                self.msg['source'] = self.localhost
                
                send_tcp('data saved', localhost, 9999)

            elif self.msg['data']['type']] == 'GET':
                print('Get data in the database')
                self.msg['data']['data'] = self.database[self.msg['data']['data']['rodovia']]
                
                # Change src and dest
                self.msg['dest'] = self.msg['source']
                self.msg['source'] = self.localhost

                send_tcp(self.msg, localhost, 9999)
