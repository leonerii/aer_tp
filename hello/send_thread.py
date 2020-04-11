from threading import Thread, RLock
from time import sleep
import socket
import sys
import struct

mcast_group_ipv4 = '239.0.0.1'
# Broadcast interval
mcast_delay = 5

class SendMessage(Thread):
    def __init__(self, route_table, lock):

        Thread.__init__(self)
        self.route_table = route_table
        self.lock = lock
        

    def run(self):
        try:
            send_message(route_table='tabela de roteamento')
            #self.lock.acquire()

        except Exception as e:
            print(f'Failed to create Threads: {e}')

        finally:
            pass
        print(f'finally')
            #self.lock.release()

    
def create_socket():
    # Multicast ttl (router hops)
    mcast_ttl = 1
    
    # IPV6Multicast group address
    mcast_group = 'FF02::1'
    ttl = struct.pack('@i', mcast_ttl)
    # Get Address Family
    addrinfo = socket.getaddrinfo(mcast_group_ipv4, None)[0]
    
    try:
        # Criar o UDP socket
        udp_socket = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
        #udp_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl)
        udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        
    except Exception as sock_error:
        print(f'Failed to create socket: {sock_error}')

    return udp_socket

def send_message(route_table):
    # Multi-cast group port
    mcast_port = 9999
    # Hello message
    mcast_message = 'hello'

    while True:
        try:
            # Enviar a mensagem multicast
            print(f'Sending multicast message to the multicast group: {mcast_group_ipv4} ...')
            create_socket().sendto(mcast_message.encode("utf-8") + route_table.encode(), (mcast_group_ipv4,mcast_port))
            
            # Resposta do Receiver
            received_msg = create_socket().recvfrom(4096)
            print('Preparing to receive back')
            response = received_msg[0].decode()
            src_ip = received_msg[1][0]
            
            # Imprimir a mensagem recebida
            print(f'Received from {src_ip}: {response}')
            
        except (KeyboardInterrupt, SystemExit) as e:
            print('Terminating connection with Node ...')
            break
        except socket.gaierror as sock_error:
            print(f'Sending error \'gaierror\': {sock_error}')
            break
    
        # Tempo de espera até enviar o próximo HELLO
        sleep(mcast_delay)

    # clean-up the socket
    create_socket().close()

# Criando as threads
t1 =  SendMessage(route_table=1, lock=2)
#t2 =  SendMessage(route_table=1, lock=2)

t1.start()
#t2.start()

connections = []
connections.append(t1)
#connections.append(t2)

for t in connections:
    t.join()


print(f'Cheguei ao fim do script')
# def main():
#     #send_message()
#     SendMessage(route_table=0,lock=1)

# if __name__ == "__main__":
#      main()
