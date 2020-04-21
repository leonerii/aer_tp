from threading import Thread, RLock, Timer
#from time import sleep
import socket
import struct


class SendMessage(Thread):
    def __init__(self, route_table :dict, lock :RLock):

        Thread.__init__(self)
        self.route_table    = route_table
        self.lock           = lock
            
    def run(self):
        try:
            self.hello_sender(route_table='hello')
            
            #self.lock.acquire()

        except Exception as e:
            print(f'Failed: {e}')

        finally:
            pass
            #self.lock.release()

    
    def create_socket(self):
        '''
        Cria socket UDP para o sender, define o número de hops (saltos - mcast_ttl)

        '''
        self.mcast_ttl = 2
        self.mcast_group = 'FF02::1'
        self.addrinfo = socket.getaddrinfo(self.mcast_group, None)[0]
        
        # Fazer com que o ttl seja interpretado com "packed binary data"
        self.ttl = struct.pack('@i', self.mcast_ttl)
        
        try:
            self.udp_socket = socket.socket(self.addrinfo[0], socket.SOCK_DGRAM)
            self.udp_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, self.ttl)
            
        except Exception as sock_error:
            print(f'Failed to create socket: {sock_error}')

        return self.udp_socket

    def hello_sender(self,route_table):
        '''
        Envia Messagem do tipo "HELLO" juntamente com a tabela de roteamento (route_table)
        e fecha o socket
        '''
        self.mcast_group = 'FF02::1'
        self.mcast_port = 9999
        #self.mcast_delay = 5

        while True:
            try:
                print(f'Sending multicast message to the multicast group: {self.mcast_group} ...')
                self.create_socket().sendto(self.route_table.encode(), (self.mcast_group,self.mcast_port))
                
            except socket.gaierror as sock_error:
                print(f'Sending error \'gaierror\': {sock_error}')
                break
            finally:
                self.create_socket().close()
            
            # sleep(self.mcast_delay)

'''
Cria uma instância da class e executa a thread e depois espera 30 segundos para voltar a repetir o processo
'''       

def main():
    print(f'Criando a instancia da class . . . ')
    hello = SendMessage(
        route_table='hello',
        lock=1
    )
    print(f'Esperar 5 segundos...')
    Timer(5.0, main).start()

if __name__ == "__main__":
    main()
