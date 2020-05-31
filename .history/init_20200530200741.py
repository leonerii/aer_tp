from udp_server import UDP_Server
from tcp_server import TCP_Server
from ndn_server import NDN_Server
import netifaces


def get_ip():
        ipv6 = netifaces.ifaddresses('eth0')

        return ipv6[netifaces.AF_INET6][0]['addr']

def main():
    localhost = get_ip()

    udp = UDP_Server(localhost=localhost, mcast_group='FF02::1', mcast_port=9999, hello_interval=2, dead_interv=8)
    tcp = TCP_Server(localhost)

    udp.start()
    tcp.start()


if __name__ == '__main__':
    main()