from threading import Thread, RLock
from time import sleep
import struct

class SendMessage(Thread):
    def __init__(self, route_table :dict, lock :RLock):

        Thread.__init__(self)
        self.route_table    = route_table
        self.lock           = lock
            
    def run(self):
        try:
            self.lock.acquire()
            self.hello_sender()

        except Exception as e:
            print(f'Failed: {e}')

        finally:
            self.lock.release()
    
    def create_socket(self):
        # hops
        self.mcast_ttl = 2
        self.mcast_group = 'FF02::1'
        self.ttl = struct.pack('@i', mcast_ttl)
        
        # De acordo com o tipo de IP (ipv4 ou ipv6) definir a familia
        addrinfo = socket.getaddrinfo(mcast_group_ipv4, None)[0]
        
        try:
            # Criar o socket do client
            self.client_sock = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
            self.client.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, self.ttl)
         
        except Exception as sock_error:
            print(f'Failed to create socket: {sock_error}')

        return udp_socket

    def hello_sender(self, route_table):

        '''
        Envia Messagem do tipo "HELLO" juntamente com a tabela de roteamento (route_table)
        e fecha o socket
        '''
        self.hello_interval = 30

        while True:
            try:
                # Messagem a ser enviada

                self.msg = {
                "type": "HELLO"
                }

                for keys, values in list(route_table.items()):
                    if values['next_hop'] == None:
                    self.msg[keys] = values['timestamp']

                print(f'Sending multicast message to the multicast group ...')
                self.create_socket().sendto(str(self.msg).encode('utf-8'), (self.mcast_group,self.mcast_port))

            except socket.gaierror as socket_error:
                print(f'Sending error \'gaierror\': {socket_error}')
                break
            finally:
                self.create_socket().close()
        
        sleep(self.hello_interval)

