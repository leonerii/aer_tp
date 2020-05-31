from threading import Thread
from ndn_receive_handler import Receive_Handler
from ndn_hello_sender 

class NDN_Server(Thread):
    def __init__(self, localhost, port=9999, data_ids={}):
        Thread.__init__(self)
        self.localhost = localhost
        self.port = port
        self.data_ids = data_ids


    def run(self):
        #inicializar pit, fib e cs
        #if
        #criar socket server tcp

        while True:
            rcv_msg = self.sock.recvfrom(10240)

            ndn_handler = Receive_Handler(
                                        self.lock, self.pit, self.fib,
                                        self.cs, self.conn, self.queue, self.localhost,
                                        self.udp_port

                )
            ndn_handler.start()

        # Send HELLO NDN messages
        hello_sender = HelloSender(
                                    self.route_table, self.lock,
                                    self.hello_interval, self.local_ip,
                                    self.mcast_ttl,
                                    self.mcast_group, self.mcast_port
                                )
        hello_sender.start()
