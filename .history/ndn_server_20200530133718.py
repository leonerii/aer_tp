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


    def run(self):
        #inicializar pit, fib e cs
        if self.data_ids:
            pass

        #criar socket server tcp
            tcp_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            tcp_socket.bind((self.localhost, self.port))

        # Receiving NDN Messages
            while True:
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
                                        self.mcast_group, self.mcast_port
                                    )
            ndn_hello_sender.start()

        else:
            

