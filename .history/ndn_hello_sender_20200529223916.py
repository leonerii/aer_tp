from threading import Thread, RLock
from time import sleep
from json import dumps
from uuid import uuid4
import socket

class HelloSender(Thread):
    def __init__(self, lock, hello_interval, localhost, mcast_group, mcast_port):

        Thread.__init__(self)
        self.lock           = lock
        self.hello_interval = hello_interval
        self.localhost      = localhost
        self.mcast_group    = mcast_group
        self.mcast_port     = mcast_port

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
            # Hello message to be sent
            self.msg = {
                "type": "HELLO",
                "source": self.localhost
            }

            for keys, values in self.route_table.items():
                if values['next_hop'] == None:
                    self.msg[keys] = values['timestamp']

            client_sock.sendto(dumps(self.msg).encode('utf-8'), (self.mcast_group,self.mcast_port))

        except socket.gaierror as socket_error:
            print('Sending error: {}'.format(socket_error))

        finally:
            client_sock.close()

    def route_request(self, target, msg):
        client_sock = self.create_socket()
        try:
            self.id = uuid4()
            self.pid = getpid()

            self.msg = {
                "type": "ROUTE_REQUEST",
                "dest": target,
                "path": [""],
                "pid": self.pid,
                "ttl": self.ttl,
                "id": f'{self.id}'
            }
            print(self.msg)

            print('Route Request ...')
            client_sock.sendto(dumps(self.msg).encode('utf-8'), (self.mcast_group,self.mcast_port))

        except socket.gaierror as socket_error:
            print('Sending error: {}'.format(socket_error))

        finally:
            client_sock.close()

    def route_reply(self):
        client_sock = self.create_socket()
        self.pid = getpid()

        try:
            self.msg = {
            "type": "ROUTE_REPLY",
            "dest": "target",
            "path": [""],
            "pid": self.pid,
            "ttl": self.ttl
            }
            print(self.msg)

            print('Route Request ...')
            client_sock.sendto(dumps(self.msg).encode('utf-8'), (self.mcast_group,self.mcast_port))

        except socket.gaierror as socket_error:
            print('Sending error: {}'.format(socket_error))

        finally:
            client_sock.close()

"""
rota = SendMessage(route_table=1, lock=1, hello_interval=2, ttl=4, mcast_group="FF02::1", mcast_port=9999)
rota.route_request('localhost', 'route')
print("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
rota.route_reply()
"""
