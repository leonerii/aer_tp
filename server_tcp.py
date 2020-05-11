import socket
from json import loads, dumps
from time import time_ns
from uuid import uuid4

localhost = '127.0.0.1'
port = 9999
server= (localhost, port)
database = {}


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       
sock.bind(server)
sock.listen(1)
print(f'Server listening on port: {port}')

conn, addr = sock.accept()

#while True:
N102 = {
'road': 'N102',
'type': 'accident',
'reference': 'close to Pingo doce',
'timestamp': time_ns(),
'reporter' : localhost
}

N103 = {
'road': 'N103',
'type': 'accident',
'reference': 'close to A3',
'timestamp': time_ns(),
'reporter' : localhost
}

database['N102'] = N102
database['N103'] = N103

try:
    #msg, addr = sock.recv(4096)
    msg = conn.recv(1024)
    print(f'Connected from {addr[0]}')
    msg = loads(msg.decode("utf-8"))
    
    if not msg['dest'] == localhost:
        # Fazer o encapsulamento da mensagem.
        print('Routing request . . . ')
        
        msg = {
        'type': 'DATA',
        'id': str(uuid4()),
        'data': msg,
        'dest': msg['dest'],
        'ttl': 30,
        'source': localhost
        }
        
        # Abrir socket UDP e enviar a mensagem com type DATA
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.sendto(dumps(msg).encode('utf-8'), (localhost, 9999))
        print(f'Message sent {msg}')

        # Resposta
        udp_response = udp_socket.recvfrom(1024)
        udp_socket.close()
        print(f'CLOSING UDP SOCKET')
       
        # Mandar a mensagem de volta a interface desencapsulada.
        msg = loads(udp_response[0].decode('utf-8'))
       # print(msg)
        conn.sendall(dumps(msg['data']).encode('utf-8'))
        

    if msg['type'] == 'POST':
        print('Saving data to the database ...')
        event_key = msg['data']['road']
    
        if event_key in database.keys() and msg['data']['timestamp'] > database[event_key]['timestamp']: 
            #event_key = event_key + '_v2'
            database[event_key]['type_v'] = msg['data']
            database[event_key]['reporter'] = msg['source']
            database[event_key]['timestamp'] = time_ns()
            print(database)
            conn.send("data saved".encode('utf-8'))

        else:
            database[event_key] = msg['data']
            database[event_key]['reporter'] = msg['source']
            database[event_key]['timestamp'] = time_ns()
            print(database)

            conn.send("data saved".encode('utf-8'))
        
    elif msg['type'] == 'GET':
        print('Get data from the database')
        event_key = msg['data']['road']
        if msg['data']['road'] in database.keys():
            msg['data'] = database[msg['data']['road']]
            print(msg['data'])

            conn.send(dumps(msg['data']).encode('utf-8'))

        else:
            print(f'Requested information \'{event_key}\' not found on the database')
            database_info_list = [key for key in database.keys()]
            response = f'{event_key} - not found DB. \nFound: {database_info_list}'
            conn.send(str(response).encode('utf-8'))

except Exception as e:
    print(e)

conn.close()
