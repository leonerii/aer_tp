import socket
from threading import Thread, RLock
from json import loads, dumps
from time import time
from uuid import uuid4
from send_data import udp_data

class Receive_Handler(Thread):
    def __init__(self, lock, pit, fib, cs, conn, queue, localhost, udp_port=9999):

        Thread.__init__(self)
        self.pit = pit
        self.fib = fib
        self.lock = lock
        self.cs = cs
        self.conn = conn
        self.queue = queue
        self.localhost = localhost
        self.udp_port = udp_port
        self.msg = loads(self.conn.decode("utf-8"))
        self.addr = self.msg['source']


    def run(self):
        try:
            if self.msg["type"] == "GET":
                self.lock.acquire()
                self.get_handler()

            elif self.msg['type'] == 'POST':
                self.lock.acquire()
                self.post_handler()

            elif self.msg['type'] == 'INTEREST_REPLY':
                self.lock.acquire()
                self.ireply_handler()

            elif self.msg['type'] == 'INTEREST_REQUEST':
                self.lock.acquire()
                self.irequest_handler()

            elif self.msg['type'] == 'HELLO':
                self.lock.acquire()
                self.hello_handler()

        except Exception as e:
            print(e.with_traceback())

        finally:
            self.lock.release()


    def get_handler(self):
        msg_id = self.msg['id']

        if msg_id in self.cs.keys():
            self.conn.sendall(dumps(self.cs[msg_id]).encode('utf-8'))
            self.conn.close()

        elif msg_id in self.pit.keys():
            pit_entry = {
                'conn': self.conn
            }

            self.pit[msg_id][self.msg['source']] = pit_entry

            self.conn.sendall(dumps({
                'status': 'we are still looking for the data'
            }).encode('utf-8'))

        elif msg_id in self.fib.keys():
            udp_msg = {
                'type': 'DATA',
                'id': uuid4(),
                'data': {
                    'type': 'INTEREST_REQUEST',
                    'id': msg_id,
                    'source': self.localhost
                },
                'dest': self.fib[msg_id],
                'ttl': 30,
                'source': self.localhost
            }

            pit_entry = {
                'conn': self.conn
            }

            self.pit[msg_id][self.msg['source']] = pit_entry

            udp_data(dumps(udp_msg).encode('utf-8'), self.localhost, self.udp_port)

            self.conn.sendall(dumps({
                'status': 'we have requested the data'
            }).encode('utf-8'))

        else:
            udp_msg = {
                'type': 'DATA',
                'id': uuid4(),
                'data': {
                    'type': 'INTEREST_REQUEST',
                    'id': msg_id,
                    'source': self.localhost
                },
                'dest': 'multicast',
                'ttl': 30,
                'source': self.localhost
            }

            pit_entry = {
                'conn': self.conn
            }

            self.pit[msg_id][self.msg['source']] = pit_entry

            udp_data(dumps(udp_msg).encode('utf-8'), self.localhost, self.udp_port)

            self.conn.sendall(dumps({
                'status': 'we are looking for the data'
            }).encode('utf-8'))


    def irequest_handler(self):
        msg_id = self.msg['id']

        if msg_id in self.cs.keys():
            udp_msg = {
                'type': 'DATA',
                'id': uuid4(),
                'data': {
                    'type': 'INTEREST_REPLY',
                    'id': msg_id,
                    'source': self.localhost,
                    'data': self.cs[msg_id]
                },
                'dest': 'multicast',
                'ttl': 30,
                'source': self.localhost
            }

            udp_data(dumps(udp_msg).encode('utf-8'), self.localhost, self.udp_port)

        elif msg_id in self.pit.keys():
            if not self.msg['source'] == self.localhost:
                self.pit[msg_id][self.msg['source']] = {}

        elif msg_id in self.fib.keys():
            udp_msg = {
                'type': 'DATA',
                'id': uuid4(),
                'data': {
                    'type': 'INTEREST_REQUEST',
                    'id': msg_id,
                    'source': self.localhost
                },
                'dest': self.fib[msg_id],
                'ttl': 30,
                'source': self.localhost
            }

            self.pit[msg_id][self.msg['source']] = {}

            udp_data(dumps(udp_msg).encode('utf-8'), self.localhost, self.udp_port)

        self.conn.close()


    def ireply_handler(self):
        msg_id = self.msg['id']

        if msg_id in self.pit.keys():

            for key, value in self.pit[msg_id].items():
                if value:
                    try:
                        value['conn'].sendall(dumps(self.msg['data']).encode('utf-8'))
                        value['conn'].close()

                    except Exception as e:
                        print(e)
                        print('Unable to send message back')

                else:
                    udp_msg = {
                        'type': 'DATA',
                        'id': uuid4(),
                        'data': {
                            'type': 'INTEREST_REPLY',
                            'id': msg_id,
                            'source': self.localhost,
                            'data': self.msg['data']
                        },
                        'dest': key,
                        'ttl': 30,
                        'source': self.localhost
                    }

                    udp_data(dumps(udp_msg).encode('utf-8'), self.localhost, self.udp_port)

            self.cs[msg_id] = self.msg['data']
            del self.pit[msg_id]


    def hello_handler(self):
        #apagar self.msg['type']
        for key, value in self.msg.items():
            self.fib[key] = value


    def post_handler(self):
        msg_id = self.msg['id']

        self.cs[msg_id] = self.msg['data']
        self.fib[msg_id] = self.localhost