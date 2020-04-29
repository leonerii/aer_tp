from threading import Thread, RLock
from json import loads
from time import time
from os import kill
from signal import SIGUSR1
from msg_unicast import send_unicast
#from mcast_send  import send 
from rrequest import send_multicast

class Receive_Handler(Thread):
    def __init__(self, route_table, lock, request, localhost, mcast_addr, mcast_port, queue):

        Thread.__init__(self)
        self.route_table = route_table
        self.localhost = localhost
        self.lock = lock
        self.mcast_port = mcast_port
        self.mcast_addr = mcast_addr
        self.queue = queue
        self.skt, self.addr = request  # importar da Class SOCKET
        self.msg = loads(self.skt.decode("utf-8"))
        self.address = self.msg['source']
        
    
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
            print(self.msg['data'])

        elif self.msg['dest'] in self.route_table.keys():
            self.msg['ttl'] = self.msg['ttl'] - 1

            if not self.msg['ttl']:
                return

            target = self.msg['dest']

            if self.route_table[target]['next_hop'] is None:
                print('The message - {} - sent to {}'.format(self.msg['data'],target))
                send_unicast(self.msg, target, self.mcast_port)

            else:
                next_hop = self.route_table[target]['next_hop']
                send_unicast(self.msg, next_hop, self.mcast_port)
                print('Message sent to next_hop: {}'.format(next_hop))

        elif self.msg['dest'] not in self.route_table.keys():
            self.queue[self.msg['id']] = self.msg

            rrequest = {
                "type": "ROUTE_REQUEST",
                'data': self.msg['data'],
                'id': self.msg['id'],
                'dest': self.msg['dest'],
                'ttl': 30,
                'path': [self.localhost],
                'source': self.localhost
            }

            # Send message via multicast
            # send_unicast(rrequest, self.mcast_addr, self.mcast_port)
            send_multicast(rrequest, self.mcast_addr, self.mcast_port)
            print('Message: {}'.format(rrequest))
            print('Sent to: {}'.format(self.mcast_addr))


    def rrequest_handler(self):
        if self.localhost in self.msg['path']:
            return

        elif self.msg['dest'] in self.route_table.keys() or self.msg['dest'] == self.localhost:
            self.msg['type'] = 'ROUTE_REPLY'
            self.msg['ttl'] = len(self.msg['path']) * 3
            self.msg['source'] = self.localhost
            print(self.msg)

            target = self.msg['path'].pop(-1)

            send_unicast(self.msg, target, self.mcast_port)
            print("Route Reply Sent to {}".format(target))
        
        else:
            print("Destination not in my route table")
            self.msg['ttl'] = self.msg['ttl'] - 1

            if self.msg['ttl']:
                self.msg['path'].append(self.localhost)

                #send_unicast(self.msg, self.mcast_addr, self.mcast_port)
                send_multicast(self.msg, self.mcast_addr, self.mcast_port)


    def rreply_handler(self):
        if not len(self.msg['path']):
            self.route_table[self.msg['dest']] = {
                'timestamp': time(),
                'next_hop': self.address
            }
            print("Destination saved in my route table")
            print("route table: {}".format(self.route_table))

            #Change msg type to data and increase ttl
            self.msg["type"] = "DATA"
            self.msg["ttl"] = 40
            
            # change source
            self.msg['source'] = self.localhost

            # get the original message from the queue
            data_msg = self.queue.pop(self.msg['id'], None)
            #data_msg = self.msg
            target = self.addr[0]
            send_unicast(data_msg, target, self.mcast_port)
            print('Final Message: {} Sent to destination: {}'.format(data_msg, target))


        #elif self.msg['ttl'] > 1:
        else:
            print("Sending Route Reply to: {}".format(self.msg['path'][-1]))
            self.msg['ttl'] = self.msg['ttl'] - 1

            self.route_table[self.msg['dest']] = {
                'timestamp': time(),
                'next_hop': self.address
            }

            target = self.msg['path'].pop(-1)
            print("target: {} TTL={}".format(target,self.msg['ttl']))

            send_unicast(self.msg, target, self.mcast_port)       
  
    
    def hello_handler(self):
        if self.msg['source'] == self.localhost:
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
        self.route_table[self.address] = {
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
                        'next_hop': self.address
                    }

            else:
                self.route_table[addr] = {
                    'timestamp': timestamp,
                    'next_hop': self.address
                }
