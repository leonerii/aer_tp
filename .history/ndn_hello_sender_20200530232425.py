from threading import Thread, RLock
from time import sleep
from json import dumps
from uuid import uuid4
import socket

class NDN_HelloSender(Thread):
    def __init__(self, lock, hello_interval, cs, localhost, mcast_addr, mcast_port):

        Thread.__init__(self)
        self.lock           = lock
        self.hello_interval = hello_interval
        self.localhost      = localhost
        self.mcast_group    = mcast_addr
        self.mcast_port     = mcast_port
        self.cs             = cs     # Content Store

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
        Envia Messagem do tipo "HELLO" com informação em CS
        '''
        try:
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            # Hello message to be sent
            self.msg = {
                "type": "HELLO",
                #"source": self.localhost,
                }

            if self.cs:
                cs_data = self.cs.keys()
            else:
                cs_data = []
            self.msg[] = self.localhost
            for key, value in self.fib.items():
                self.msg[key] = value

            sock.sendto(dumps(self.msg).encode('utf-8'), (self.mcast_addr,self.mcast_port))

        except socket.gaierror as socket_error:
            print('Sending error: {}'.format(socket_error))

        finally:
            sock.close()
