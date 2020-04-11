from threading import Thread, RLock
from json import loads
from time import time_ns

class Receive_Handler(Thread):
    def __init__(self, route_table :dict, lock :RLock, request):

        Thread.__init__(self)
        self.route_table = route_table
        self.lock = lock
        self.skt, self.addr = request
        self.msg = loads(self.skt[0].decode("utf-8"))

    
    def run(self):
        try:
            if self.msg['type'] == 'HELLO':
                self.lock.acquire()
                self.hello_handler()

            elif self.msg['type'] == 'ROUTE_REQUEST':
                pass

            elif self.msg['type'] == 'ROUTE_REPLY':
                pass
            
            
        finally:
            self.lock.release()

    
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
            