import socket
from threading import Thread
from json import load, dumps
from uuid import uuid4
from msg_unicast import send_unicast


class TCP_Server(Thread):
    def __init__(self, localhost, port=9999):
        Thread.__init__(self)

        self.localhost = localhost
        self.port = port
        self.socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.socket.bind((self.localhost, self.port))


    def run(self):
        self.socket.listen()

        while True:
            conn, _ = self.socket.accept()

            data = load(conn.recv(1024))

            msg = {
                'type': 'DATA',
                'id': str(uuid4()),
                'data': data,
                'dest': self.localhost,
                'ttl': 30,
                'source': self.localhost
            }

            send_unicast(msg, self.localhost, 9999)




