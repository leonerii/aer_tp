import socket
import struct
import sys

message = sys.argv[1] if len(sys.argv) > 1 else 'message via multicast'

multicast_addr = '224.0.0.1'
port = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
sock.sendto(sys.argv[1], (multicast_addr, port))
sock.close()
