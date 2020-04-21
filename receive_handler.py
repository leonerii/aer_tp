from threading import Thread, RLock
from json import loads
from time import time_ns
from os import kill
from signal import SIGUSR1

class Receive_Handler(Thread):
    def __init__(self, route_table :dict, lock :RLock, request, localhost):

        Thread.__init__(self)
        self.route_table = route_table
        self.localhost = localhost
        self.lock = lock
        self.skt, self.addr = request  # importar da Class SOCKET
        self.msg = loads(self.skt[0].decode("utf-8"))
        self.addr = self.addr[0]

    
    def run(self):
        try:
            if self.msg['type'] == 'HELLO':
                self.lock.acquire()
                self.hello_handler()

            elif self.msg['type'] == 'ROUTE_REQUEST':
                self.lock.acquire()
                self.rrequest_handler()

            elif self.msg['type'] == 'ROUTE_REPLY':
                self.lock.acquire()
                self.rreply_handler()
              
        finally:
            self.lock.release()


    def rrequest_handler(self):
        if self.localhost in self.msg['path']:
            pass

        elif self.msg['dest'] in self.route_table.keys() or self.msg['dest'] == self.localhost:
            self.msg['type'] = 'ROUTE_REPLY'
            self.msg['ttl'] = len(self.msg['path']) * 3

            target = self.msg['path'].pop(-1)

            send(target, self.msg)
        
        else:
            self.msg['ttl'] = self.msg['ttl'] - 1

            if self.msg['ttl']:
                self.msg.append(self.localhost)

                for key, values in self.route_table.items():
                    if values['next_hop'] == None:
                        send(key, self.msg)


    def rreply_handler(self):
        if self.msg['dest'] == self.localhost:
            self.route_table['dest'] = {
                'timestamp': time_ns(),
                'next_hop': self.addr
            }

            kill(self.msg['pid'], SIGUSR1)

        elif self.msg['ttl'] > 1:
            self.msg['ttl'] = self.msg['ttl'] - 1

            target = self.msg['path'].pop(-1)

            send(target, self.msg)        
  
    
    def hello_handler(self):
        """
        Apaga uma chave do dicionario para depois iterar somente nas
        chaves que importar para a atualizacao da route_table
        """
        del self.msg['type']

        """
        Adiciona ou atualiza a entrada do nó que recebemos a mensagem.
        """
        self.route_table[self.addr] = {
            'timestamp': time_ns(),
            'next_hop': None
        }

        """
        Itera no dicionario recebido e atualiza a tabela de rotas.
        Se a entrada existe na tabela de rotas e o registro que recebemos é mais
        recente (timestamp maior), atualizo a entrada na tabela de rotas, se
        não, não faço nada.
        Se a entrada não existe na tabela de rotas, simpleste adiciono a antrada
        a tabela.
        """
        for addr, timestamp in self.msg.items():

            if addr in self.route_table.keys(): 
                if self.route_table[addr]['timestamp'] < timestamp:
                    self.route_table[addr] = {
                        'timestamp': timestamp,
                        'next_hop': self.addr
                    }

            else:
                self.route_table[addr] = {
                    'timestamp': timestamp,
                    'next_hop': self.addr
                }
            