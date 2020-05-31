from threading import Thread, RLock
from ndn_receive_handler import Receive_Handler
from ndn_hello_sender import NDN_HelloSender
from json import dumps
import socket

class NDN_Server(Thread):
    def __init__(self, localhost, port=9999, hello_interval=5, init_cs={}):
        Thread.__init__(self)
        self.localhost = localhost
        self.port = port
        self.cs = init_cs
        self.lock = RLock()
        self.queue = {}
        self.fib = {}
        self.pit = {}
        self.hello_interval = hello_interval


    def run(self):
        #TCP Server
        tcp_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        tcp_socket.bind((self.localhost, self.port))
        tcp_socket.listen()

        ndn_hello_sender = NDN_HelloSender(
                                    self.lock, self.hello_interval, 
                                    self.cs, self.fib, self.localhost,
                                    'multicast', self.port
                                )

        ndn_hello_sender.start()

        # Receiving NDN Messages
        while True:
            self.conn, _ = tcp_socket.accept()

            ndn_handler = Receive_Handler(
                                        self.lock, self.pit, self.fib,
                                        self.cs, self.conn, self.localhost
                )

            ndn_handler.start()
            
            
            print('########## CS #########')
            print(dumps(self.cs, indent=2))
            print('\n########## FIB #########')
            print(dumps(self.fib, indent=2))
            print()

        # Send NDN HELLO messages
