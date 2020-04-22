import socket
import struct
from datetime import datetime
from threading import RLock
from lifecycle import MyLifecycle
from hello_sender import SendMessage
from receive_handler import Receive_Handler

class Multicast():

    def __init__(self):
        self.mcast_group = 'FF02::1'
        self.mcast_port = 9999
        self.route_table = {}
        self.dead_interv = 30
        self.recycle_time = 45
        self.lock = RLock()
        self.hello_interval = 2
        self.mcast_ttl = 1
        self.ttl = struct.pack('@i', self.mcast_ttl)
        self.addrinfo = socket.getaddrinfo(self.mcast_group, None, socket.AF_INET6)[0]

          
    def create_socket(self):
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    

    def listen(self):
        # abre porta 9999
        self.sock.bind(('', self.mcast_port)) 
        
        # Join Multicast Group
        member_request = struct.pack("16sI".encode('utf-8'), socket.inet_pton(socket.AF_INET6, self.mcast_group), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, member_request)


    def receive(self):
        local_ip = socket.getaddrinfo(socket.gethostname(),None, socket.AF_INET6)[0][4][0]
        lifecycle = MyLifecycle(self.route_table, self.lock, self.dead_interv, self.recycle_time)
        lifecycle.start()

        while True:
            
            #print ("\nWaiting packets")

            rcv_msg = self.sock.recvfrom(10240)
                        
            receive_handler = Receive_Handler(self.route_table, self.lock, rcv_msg, local_ip, self.mcast_group, self.mcast_port)
            receive_handler.start()

            # imprime a mensagem recebida com um 'timestamp' provisorio 'dt'
            #print ('Receiving data:')
            #print (rcv_msg)

            print(self.route_table)
            
        
    
    def send(self):
        
        hello_sender = SendMessage( 
                                    self.route_table, self.lock, 
                                    self.hello_interval, self.mcast_ttl, 
                                    self.mcast_group, self.mcast_port
                                )
        hello_sender.start()
        



def main():
    net = Multicast()
    
    net.create_socket()
    net.listen()
    net.send()
    net.receive()
    

if __name__ == '__main__':
    main() 