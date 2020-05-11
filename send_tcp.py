import socket
from json import dumps
import uuid
from time import time_ns

localhost = '127.0.0.1'
port = 9999

def send_message():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    except Exception as sock_error:
        print(f'Failed to create socket: {sock_error}')

    try:
        
        road = input(f'Please enter the road reference: ')
        interface  = {
            'road': road,
            'type' : 'accident',
            'ref' : 'close to A3',
            'timestamp' : time_ns()
        }

        method = input(f'Please enter message method GET|POST: ')
        dest = input(f'Please enter the destination for the msg: ')

        msg = {
            'type': method,
            'source': localhost,
            'dest': dest,
            'data': interface
        }

        print(f'Sending message {msg} to: {localhost} ...')
        sock.connect((localhost, port))
        sock.sendall(dumps(msg).encode("utf-8"))

        # Resposta
        received_msg = sock.recvfrom(4096)
        print('Preparing to receive back')
        response = received_msg[0].decode()
        print(f'Message Received: {response}')
        
    except (KeyboardInterrupt, SystemExit) as e:
        print('Terminating connection with Node ...')

    except socket.gaierror as sock_error:
        print(f'Sending error \'gaierror\': {sock_error}')
    
    except OSError as os_error:
        print(f'Sending error \'OSError\': {os_error}')
    
    finally:        
        sock.close()

def main():
    send_message()


if __name__ == "__main__":
    main()
