from threading import Thread, RLock
from ndn_receive_handler import Receive_Handler
from ndn_hello_sender import NDN_HelloSender
import socket

class NDN_Server(Thread):
    def __init__(self, localhost, port=9999, mcast_group='FF02::1', hello_interval=5, data_ids={}):
        Thread.__init__(self)
        self.localhost = localhost
        self.mcast_group = mcast_group
        self.port = port
        self.data_ids = data_ids
        self.lock = RLock()
        self.queue = {}
        self.cs = {}
        self.fib = {}
        self.pit = {}
        self.hello_interval = hello_interval


    def run(self):
        # Check whether we have data in data_ids to add them to cs
        if self.data_ids:
            for key,value in self.data_ids.items():
                self.cs[key] = value

        #TCP Server
        tcp_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        tcp_socket.bind((self.localhost, self.port))
        tcp_socket.listen()

        # Receiving NDN Messages
        while True:
            self.conn, _ = tcp_socket.accept()
            rcv_msg = tcp_socket.recvfrom(10240)

            ndn_handler = Receive_Handler(
                                        self.lock, self.pit, self.fib,
                                        self.cs, self.conn, self.localhost
                )

            ndn_handler.start()

        # Send NDN HELLO messages
        ndn_hello_sender = NDN_HelloSender(
                                    self.lock, self.hello_interval, 
                                    self.cs, self.localhost,
                                    'multicast', self.port
                                )

        ndn_hello_sender.start()
