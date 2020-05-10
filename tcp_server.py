import socket
from threading import Thread
from json import loads, dumps
from uuid import uuid4
from msg_unicast import send_unicast
from time import time_ns


class TCP_Server(Thread):
    def __init__(self, localhost, port=9999):
        Thread.__init__(self)

        #self.localhost = localhost
        self.localhost = '127.0.0.1'
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
                Mandar mensagem pro server UDP localhost.
                Fazer o encapsulamento da mensagem.
                Abrir socket UDP e enviar a mensagem com type DATA
                """
            
            elif self.msg['dest'] == self.localhost:
                self.request_handler()


    def request_handler(self):
        
        try:
            if self.msg['type'] == 'POST':
                print('Saving data to the database ...')
                event_key = self.msg['data']['rodovia']

                # TODO: Analisar o que fazer quando tentar fazer POST de informação sobre uma rodovia que já existe na base de dados
                if event_key in self.database.keys() and self.msg['data']['timestamp'] > self.database[event_key]['timestamp']: 
                    #event_key = event_key + '_v2'
                    self.database[event_key]['type_v'] = self.msg['data']
                    self.database[event_key]['reporter'] = self.msg['source']
                    self.database[event_key]['timestamp'] = time_ns()
                    print(self.database)
                    self.conn.send("data saved".encode('utf-8'))

                else:
                    self.database[event_key] = self.msg['data']
                    self.database[event_key]['reporter'] = self.msg['source']
                    self.database[event_key]['timestamp'] = time_ns()
                    print(self.database)

                    self.conn.send("data saved".encode('utf-8'))
                
            elif self.msg['type'] == 'GET':
                print('Get data from the database')
                event_key = self.msg['data']['rodovia']
                if self.msg['data']['rodovia'] in self.database.keys():
                    self.msg['data'] = self.database[self.msg['data']['rodovia']]
                    print(self.msg['data'])

                    self.conn.send(dumps(self.msg['data']).encode('utf-8'))

                else:
                    database_info_list = []
                    for key in self.database.keys():
                        database_info_list.append(key)
                    #raise Exception(f'Requested information \'{event_key}\' not found on the database')
                    print(f'Requested information \'{event_key}\' not found on local database')
                    self.conn.send(str(database_info_list).encode('utf-8'))

        except Exception as e:
            print(e)

        finally:
            self.conn.close()
