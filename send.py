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

    #while True:
    try:
        
        road = input(f'Please enter the road reference: ')
        interface  = {
            'rodovia': road,
            'type' : 'accident',
            'reference' : 'close to A3',
            'timestamp' : time_ns()
        }

        method = input(f'Please enter message method GET|POST: ')

        msg = {
            'type': method,
            'source': localhost,
            'dest': localhost,
            'data': interface
            }

        # Enviar a mensagem multicast
        print(f'Sending message {msg} to: {localhost} ...')
        sock.connect((localhost, port))
        sock.sendall(dumps(msg).encode("utf-8"))

        # Resposta do Receiver
        received_msg = sock.recvfrom(4096)
        print('Preparing to receive back')
        response = received_msg[0].decode()
        print(f'Message Received: {response}')

        # src_ip = received_msg[1][0]
        
        # # Imprimir a mensagem recebida
        # print(f'Received from {src_ip}: {response}')
        
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
