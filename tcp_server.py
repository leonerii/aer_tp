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
        self.msg = {}
        self.database = {}


    def run(self):
        self.socket.listen()

        while True:
            """
            Inicialização das variaveis
            """
            self.conn, _ = self.socket.accept()
            self.msg = load(self.conn.recv(1024))

            """
            Tratar a mensagem recebida aqui
            """


    def request_handler(self):
        
        # sock = create_socket()
        # send_tcp = self.conn.sendall($message)

        if self.msg['dest'] == self.localhost:
            if self.msg['data']['type'] == 'POST':
                print('Save data to the database')
                self.database[self.msg['data']['data']['rodovia']] = self.msg['data']['data']
                
                # Change src and dest
                self.msg['dest'] = self.msg['source']
                self.msg['source'] = self.localhost
                
                send_tcp('data saved', self.localhost, 9999)

            elif self.msg['data']['type'] == 'GET':
                print('Get data in the database')
                self.msg['data']['data'] = self.database[self.msg['data']['data']['rodovia']]
                
                # Change src and dest
                self.msg['dest'] = self.msg['source']
                self.msg['source'] = self.localhost

                send_tcp(self.msg, self.localhost, 9999)




