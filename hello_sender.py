from threading import Thread, RLock
from time import sleep

class SendMessage(Thread):
    def __init__(self, route_table :dict, lock :RLock, mcast_group, mcast_port, sock):

        Thread.__init__(self)
        self.route_table    = route_table
        self.lock           = lock
        self.mcast_group = mcast_group
        self.mcast_port = mcast_port
        self.sock   = sock
            
    def run(self):
        try:
            self.lock.acquire()
            self.hello_sender()

        except Exception as e:
            print(f'Failed: {e}')

        finally:
            self.lock.release()

    def hello_sender(self, route_table):

        '''
        Envia Messagem do tipo "HELLO" juntamente com a tabela de roteamento (route_table)
        e fecha o socket
        '''
        self.hello_interval = 30

        self.msg = {
                "type": "HELLO"
                }
        self.msg.update(self.route_table)

        while True:
            try:
                print(f'Sending multicast message to the multicast group: {self.mcast_group} ...')
                self.sock.sendto(str(self.msg).encode('utf-8'), (self.mcast_group,self.mcast_port))

            except socket.gaierror as socket_error:
                print(f'Sending error \'gaierror\': {socket_error}')
                break
            finally:
                self.sock.close()
        
        sleep(self.hello_interval)

