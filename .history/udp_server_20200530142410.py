import socket
import struct
from threading import Thread
from datetime import datetime
from threading import RLock
from lifecycle import MyLifecycle
from hello_sender import HelloSender
from receive_handler import Receive_Handler
from json import dumps

class UDP_Server(Thread):


    def __init__(self, localhost, mcast_group, mcast_port, dead_interv, hello_interval):
        Thread.__init__(self)

        self.mcast_group = mcast_group
        self.mcast_port = mcast_port
        self.dead_interv = dead_interv
        self.hello_interval = hello_interval
        self.route_table = {}
        self.queue = {}
        self.lock = RLock()
        self.mcast_ttl = 1
        self.local_ip = localhost
        self.ttl = struct.pack('@i', self.mcast_ttl)
        #self.addrinfo = socket.getaddrinfo(self.mcast_group, None, socket.AF_INET6)[0]


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
        lifecycle = MyLifecycle(self.route_table, self.lock, self.dead_interv)
        lifecycle.start()

        print("my ipv6: " + self.local_ip)

        while True:

            #print ("\nWaiting packets")

            rcv_msg = self.sock.recvfrom(10240)

            receive_handler = Receive_Handler(
                                                self.route_table, self.lock, rcv_msg,
                                                self.local_ip, self.mcast_group,
                                                self.mcast_port, self.queue
                                            )
            receive_handler.start()

            # imprime a mensagem recebida com um 'timestamp' provisorio 'dt'
            #print ('Receiving data:')
            #print (rcv_msg)

            #print(dumps(self.route_table, indent=2))



    def send(self):

        hello_sender = HelloSender(
                                    self.route_table, self.lock,
                                    self.hello_interval, self.local_ip,
                                    self.mcast_ttl,
                                    self.mcast_group, self.mcast_port
                                )
        hello_sender.start()


    def run(self):
        self.create_socket()
        self.listen()
        self.send()
        self.receive()


"""
def main():
    net = Multicast(mcast_group='FF02::1', mcast_port=9999, hello_interval=2, dead_interv=8)

    net.create_socket()
    net.listen()
    net.send()
    net.receive()
"""