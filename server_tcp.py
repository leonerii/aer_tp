import socket
from json import loads, dumps
from time import time_ns

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
'rodovia': 'N102',
'type': 'accident',
'reference': 'close to Pingo doce',
'timestamp': time_ns(),
'reporter' : localhost
}

N103 = {
'rodovia': 'N103',
'type': 'accident',
'reference': 'close to A3',
'timestamp': time_ns(),
'reporter' : localhost
}

database['N102'] = N102
database['N103'] = N103

try:
    #msg, addr = sock.recv(4096)
    msg = conn.recv(4096)
    print(f'Connected from {addr[0]}')
    msg = loads(msg.decode("utf-8"))

    if msg['type'] == 'POST':
        print('Saving data to the database ...')
        event_key = msg['data']['rodovia']
    
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
        event_key = msg['data']['rodovia']
        if msg['data']['rodovia'] in database.keys():
            msg['data'] = database[msg['data']['rodovia']]
            print(msg['data'])

            conn.send(dumps(msg['data']).encode('utf-8'))

        else:
            database_info_list = []
            for key in database.keys():
                database_info_list.append(key)
            #raise Exception(f'Requested information \'{event_key}\' not found on the database')
            print(f'Requested information \'{event_key}\' not found on the database')
            conn.send(str(database_info_list).encode('utf-8'))

except Exception as e:
    print(e)

conn.close()
