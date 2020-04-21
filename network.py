import socket
import struct
from datetime import datetime


class Multicast():

    def __init__(self):
        self.mcast_group = 'FF02::1'
        self.mcast_port = 9999
        self.rcv_msg = ''
          

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
        while True:
            print ("\nWaiting packets")

            self.rcv_msg = str(self.sock.recvfrom(10240))
            dt = str(datetime.now())

            # imprime a mensagem recebida com um 'timestamp' provisorio 'dt'
            print ('Receiving data:')
            print ('|'+str(dt)+' || '+self.rcv_msg+' |')
    
    
    def send(self):
        pass
        #chama a class do Adriano

net = Multicast()

def main():
    net.create_socket()
    net.listen()
    net.receive()

if __name__ == '__main__':
    main() 