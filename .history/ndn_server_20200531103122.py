from threading import Thread
from ndn_receive_handler import Receive_Handler
from ndn_hello_sender import NDN_HelloSender
import socket

class NDN_Server(Thread):
    def __init__(self, localhost, port=9999, data_ids={}):
        Thread.__init__(self)
        self.localhost = localhost
        self.port = port
        self.data_ids = data_ids
        self.queue = {}
        self.cs = {}
        self.fib = {}
        self.pit = {}


    def run(self):
        #inicializar pit, fib e cs
        """
        data_ids = {
            'N104.continente': '',
            'N101.A3' : '',
            'N14.braga_parque': '',
            'N4.celerois' : ''
        }

        self.fib = {
            'N104.continente': {
                'Name': 'N104.continente'
                'interfaces' : ['source1','source2']
                },
            'N14.A3': {
                'Name': 'N14.A3'
                'interfaces' : ['source1','source2']
                }
            }

        self.cs = {
            'N104.continente': 'acidente',
            'N101.A3' : ''
        }

        self.pit = {
            'N104.continente': [$requester1, $requester2],
            'N101.pingodoce': [$requester]
        }
        """
        if self.data_ids:
            for key,value in data_ids.items():
                self.cs[key] = value

        #criar socket server tcp
        tcp_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        tcp_socket.bind((self.localhost, self.port))
        tcp_socket.listen()

        # Receiving NDN Messages
        while True:
            self.conn, _ = self.socket.accept()
            rcv_msg = self.sock.recvfrom(10240)

            ndn_handler = Receive_Handler(
                                        self.lock, self.pit, self.fib,
                                        self.cs, self.conn, self.queue, self.localhost,
                                        self.udp_port

                )

            ndn_handler.start()

        # Send NDN HELLO messages
        ndn_hello_sender = NDN_HelloSender(
                                    self.fib, self.lock,self.localhost,
                                    self.hello_interval, self.cs,
                                    self.mcast_addr, self.mcast_port
                                )
        ndn_hello_sender.start()
