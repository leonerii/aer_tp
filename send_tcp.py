import socket
from json import dumps, loads
from init import get_ip
import uuid
#from time import time_ns
import time
#from interface import Gui

class Client:
    def __init__(self, port=9999):
        self.localhost = get_ip()
        self.port = port

    def send_message(self):
        try:
            self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            self.sock.settimeout(15)

            """
            Utilizar dictionary 'mensagem' da função 'post()':
            """
            action = input('GET or POST ?')

            if action == 'GET':
                road = input(f'Please enter the road name: ')
                ref = input('Road reference: ')

                interface  = {
                    'type': 'GET',
                    'id': '{}.{}'.format(road, ref),
                    'source' : self.localhost,
                }

                self.sock.sendto(dumps(interface).encode('utf-8'), self.localhost, self.port)
                res = loads(self.sock.recv(1024).decode('utf-8'))
                print(dumps(res, indent=2))

            elif action == 'POST':
                road = input(f'Please enter the road name: ')
                ref = input('Road reference: ')
                message = input('Message: ')

                interface  = {
                    'type': 'POST',
                    'id': '{}.{}'.format(road, ref),
                    'source' : self.localhost,
                    'data' : message
                }

                self.sock.sendto(dumps(interface).encode('utf-8'), self.localhost, self.port)
                res = loads(self.sock.recv(1024).decode('utf-8'))
                print(dumps(res, indent=2))

            else:
                print('error')

        except socket.timeout as err:
            print('Timeout: {}'.format(err))

        except Exception as sock_error:
            print(f'Failed to create socket: {sock_error}')
        
        finally:        
            self.sock.close()


if __name__ == "__main__":
    client = Client()
    client.send_message()
