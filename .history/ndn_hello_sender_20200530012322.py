from threading import Thread, RLock
from time import sleep
from json import dumps
from uuid import uuid4
import socket

class HelloSender(Thread):
    def __init__(self, lock, hello_interval, fib, cs, localhost, mcast_group, mcast_port):

        Thread.__init__(self)
        self.lock           = lock
        self.hello_interval = hello_interval
        self.localhost      = localhost
        self.mcast_group    = mcast_group
        self.mcast_port     = mcast_port
        self.fib            = fib   # 
        self.cs            = cs

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
        Envia Messagem do tipo "HELLO" e constroi a FIB
        '''
        try:
            client_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            # Hello message to be sent
            self.msg = {
                "type": "HELLO",
                #"source": self.localhost
                "data": self.cs.keys()
            }

            for key, value in self.fib.items():
                if value['next_hop'] == None:
                    self.msg[key] = value['timestamp']

            client_sock.sendto(dumps(self.msg).encode('utf-8'), (self.mcast_group,self.mcast_port))

        except socket.gaierror as socket_error:
            print('Sending error: {}'.format(socket_error))

        finally:
            client_sock.close()
