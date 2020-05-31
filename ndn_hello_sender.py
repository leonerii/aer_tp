from threading import Thread, RLock
from time import sleep
from json import dumps
from uuid import uuid4
import socket
import send_data

class NDN_HelloSender(Thread):
    def __init__(self, lock, hello_interval, cs, fib, localhost, mcast_addr, mcast_port):

        Thread.__init__(self)
        self.lock           = lock
        self.hello_interval = hello_interval
        self.localhost      = localhost
        self.mcast_group    = mcast_addr
        self.mcast_port     = mcast_port
        self.cs             = cs     # Content Store
        self.fib            = fib

    def run(self):
        while True:
            try:
                self.lock.acquire()
                self.ndn_hello_sender()

            except Exception as e:
                print('Failed: {}'.format(e.with_traceback()))

            finally:
                self.lock.release()
                sleep(self.hello_interval)



    def ndn_hello_sender(self):
        '''
        Envia Messagem do tipo "HELLO" com informação em CS e FIB
        '''
        try:
            # Hello message to be sent
            self.msg = {
                "type": "HELLO",
                }

            if self.cs:
                for named_data in self.cs.keys():
                    self.msg[named_data] = [self.localhost]

            for key, value in self.fib.items():
                self.msg[key] = value

            udp_msg = {
                'type': 'DATA',
                'id': str(uuid4()),
                'data': self.msg,
                'dest': self.mcast_group,
                'ttl': 30,
                'source': self.localhost
            }

            send_data.udp_data(udp_msg, '::1', 9999)

        except Exception as e:
            print('Sending error: {}'.format(e))
