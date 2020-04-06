import socket
import struct
from datetime import datetime

MCAST_GRP = 'FF02::1'
MCAST_PORT = 9999
IS_ALL_GROUPS = True

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if IS_ALL_GROUPS:
    # on this port, receives ALL multicast groups
    sock.bind(('', MCAST_PORT))
else:
    # on this port, listen ONLY to MCAST_GRP
    sock.bind((MCAST_GRP, MCAST_PORT))
mreq = struct.pack("16sI".encode('utf-8'), socket.inet_pton(socket.AF_INET6, MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

while True:
    # For Python 3, change next line to "print(sock.recv(10240))"
    print ("\nWaiting packets")

    rcv_msg = str(sock.recvfrom(10240))
    dt = str(datetime.now())
      
    #intf = socket.gethostbyname(str(rcv_msg))
    print ('Receiving data:')
    print ('|'+str(dt)+' || '+rcv_msg+' |')
  
 
    