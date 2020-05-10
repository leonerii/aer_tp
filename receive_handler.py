import socket
from threading import Thread, RLock
from json import loads, dumps
from time import time
from msg_unicast import send_unicast

class Receive_Handler(Thread):
    def __init__(self, route_table, lock, request, localhost, mcast_addr, mcast_port, queue):

        Thread.__init__(self)
        self.route_table = route_table
        self.localhost = localhost
        self.lock = lock
        self.mcast_port = mcast_port
        self.mcast_addr = mcast_addr
        self.queue = queue
        self.skt, _ = request  # importar da Class SOCKET
        self.msg = loads(self.skt.decode("utf-8"))
        self.addr = self.msg['source']
        
    
    def run(self):
        try:
            if self.msg["type"] == "HELLO":
                self.lock.acquire()
                self.hello_handler()

            elif self.msg['type'] == 'ROUTE_REQUEST':
                self.lock.acquire()
                self.rrequest_handler()

            elif self.msg['type'] == 'ROUTE_REPLY':
                self.lock.acquire()
                self.rreply_handler()

            elif self.msg['type'] == 'DATA':
                self.lock.acquire()
                self.send_data()

        except Exception as e:
            print(e.with_traceback())    
              
        finally:
            self.lock.release()


    def send_data(self):
        if self.msg['dest'] == self.localhost:
            """
            Enviar a mensagem para o server TCP localhost
            """
            tcp_sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            tcp_sock.connect((self.localhost, self.mcast_port))
            tcp_sock.sendall(dumps(self.msg['data']).encode("utf-8"))
            tcp_sock.close()

        elif self.msg['dest'] in self.route_table.keys():
            self.msg['ttl'] = self.msg['ttl'] - 1

            if not self.msg['ttl']:
                return

            target = self.msg['dest']

            if self.route_table[target]['next_hop'] is None:
                send_unicast(self.msg, target, self.mcast_port)

            else:
                next_hop = self.route_table[target]['next_hop']
                send_unicast(self.msg, next_hop, self.mcast_port)

        elif self.msg['dest'] not in self.route_table.keys():
            self.queue[self.msg['id']] = self.msg

            rrequest = {
                'type': 'ROUTE_REQUEST',
                'id': self.msg['id'],
                'dest': self.msg['dest'],
                'ttl': 30,
                'path': [self.localhost],
                'source': self.localhost
            }

            send_unicast(rrequest, self.mcast_addr, self.mcast_port)


    def rrequest_handler(self):
        if self.localhost in self.msg['path']:
            return
        
        elif self.msg['dest'] in self.route_table.keys() or self.msg['dest'] == self.localhost:
            print(dumps(self.msg))
            self.msg['type'] = 'ROUTE_REPLY'
            self.msg['ttl'] = len(self.msg['path']) * 3
            self.msg['source'] = self.localhost

            target = self.msg['path'].pop(-1)

            send_unicast(self.msg, target, self.mcast_port)
        
        elif self.msg['ttl'] - 1:
            print(dumps(self.msg))
            self.msg['ttl'] = self.msg['ttl'] - 1
            self.msg['path'].append(self.localhost)
            self.msg['source'] = self.localhost

            send_unicast(self.msg, self.mcast_addr, self.mcast_port)


    def rreply_handler(self):
        if not len(self.msg['path']) and self.msg['id'] in self.queue.keys():
            print(dumps(self.msg))
            self.route_table['dest'] = {
                'timestamp': time(),
                'next_hop': self.addr
            }

            data_msg = self.queue.pop(self.msg['id'])

            send_unicast(data_msg, self.addr, self.mcast_port)

        elif self.msg['ttl'] - 1 and self.msg['dest'] not in self.route_table.keys():
            print(dumps(self.msg))
            self.msg['ttl'] = self.msg['ttl'] - 1
            self.msg['source'] = self.localhost

            self.route_table[self.msg['dest']] = {
                'timestamp': time(),
                'next_hop': self.addr
            }

            target = self.msg['path'].pop(-1)

            send_unicast(self.msg, target, self.mcast_port)       
  
    
    def hello_handler(self):
        if self.addr == self.localhost:
            return

        """
        Apaga uma chave do dicionario para depois iterar somente nas
        chaves que importar para a atualizacao da route_table
        """
        del self.msg['type']
        del self.msg['source']

        """
        Adiciona ou atualiza a entrada do nó que recebemos a mensagem.
        """
        self.route_table[self.addr] = {
            'timestamp': time(),
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

            if addr == self.localhost:
                continue

            elif addr in self.route_table.keys(): 
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
            