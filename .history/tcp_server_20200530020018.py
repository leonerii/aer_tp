import socket
from threading import Thread
from json import loads, dumps
from uuid import uuid4
from send_data import udp_data
from time import time_ns


class TCP_Server(Thread):
    def __init__(self, localhost, port=9999):
        Thread.__init__(self)

        #self.localhost = localhost
        self.localhost = '127.0.0.1'
        self.port = port
        #self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
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
            self.msg = loads(self.conn.recv(1024))
            """
            Tratar a mensagem recebida aqui
            """

            if not self.msg['dest'] == self.localhost:
                """
                Fazer o encapsulamento da mensagem.
                Abrir socket UDP e enviar a mensagem com type DATA
                Mandar mensagem pro server UDP localhost.
                Aguardar a resposta atavés do socket TCP.

                aux_conn, _ self.socket.accept()
                self.msg = loads(self.aux_conn.recv(1024))
                aux_conn.close()

                Mandar a mensagem de volta a interface desencapsulada.

                self.conn.sendall(self.msg['data'])
                """
                self.route_request()


            elif self.msg['dest'] == self.localhost:
                self.request_handler()


    def request_handler(self):

        try:
            if self.msg['type'] == 'POST':
                print('Saving data to the database ...')
                event_key = self.msg['data']['road']

                if event_key in self.database.keys():
                    self.msg['data']['road']['reporter'] = self.msg['source']
                    self.msg['data']['road']['timestamp'] = time_ns()
                    self.database[event_key].append(self.msg['data'])

                    self.conn.send("data saved".encode('utf-8'))

                else:
                    self.msg['data']['road']['reporter'] = self.msg['source']
                    self.msg['data']['road']['timestamp'] = time_ns()
                    self.database[event_key] = self.msg['data']

                    self.conn.send("data saved".encode('utf-8'))

            elif self.msg['type'] == 'GET':
                print('Getting data from the database ...')
                event_key = self.msg['data']['road']

                if self.msg['data']['road'] in self.database.keys():
                    self.msg['data'] = self.database[self.msg['data']['road']]

                    self.conn.send(dumps(self.msg['data']).encode('utf-8'))

                else:
                    database_info_list = [key for key in self.database.keys()]
                    response = f'{event_key} - not found on DB. \nFound: {database_info_list}'
                    self.conn.send(str(response).encode('utf-8'))

        except Exception as e:
            print(e)

        finally:
            self.conn.close()


    def route_request(self):
        print('Routing request . . . ')

        self.msg = {
        'type': 'DATA',
        'id': str(uuid4()),
        'data': self.msg,
        'dest': self.msg['dest'],
        'ttl': 30,
        'source': self.localhost
        }

        udp_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        udp_socket.sendto(dumps(self.msg).encode('utf-8'), (self.localhost, 9999))
        print(f'Message sent {self.msg}')

        # Resposta
        udp_response = udp_socket.recvfrom(1024)
        udp_socket.close()
        print(f'CLOSING UDP SOCKET')

        # Enviar mensagem ao client
        self.msg = loads(udp_response[0].decode('utf-8'))
       # print(msg)
        self.conn.sendall(dumps(self.msg['data']).encode('utf-8'))