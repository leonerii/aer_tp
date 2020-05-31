from udp_server import UDP_Server
from ndn_server import NDN_Server
from random import choice
import netifaces


def get_ip():
        ipv6 = netifaces.ifaddresses('eth0')
        
        return ipv6[netifaces.AF_INET6][0]['addr']

def main():
    localhost = get_ip()

    data = {
        'N101.continente': 'acidente perto do continente na rotunda xyz',
        'N101.leroy_merlin': 'transito parado',
        'N114.perto_da_UM': 'trabalhos na estrada',
        'N103.perto_da_A1': 'acidente muito feio',
        'N112.acostamento_km_20': 'carro parado',
        'A3.galp': 'policia',
        'A7.perto_da_A11': 'oleo na pista',
        'A1.lisboa': 'transito pesado',
        'A3.porto': 'chuva forte',
        'A28.porto_leixoes': 'buraco na estrada',
        'A3.braga': 'gelo na pista',
        'A1.porto': 'transito tranquilo'
    }

    key = choice(list(data.keys()))

    udp = UDP_Server(localhost=localhost, mcast_group='FF02::1', mcast_port=9999, hello_interval=2, dead_interv=8)
    ndn = NDN_Server(localhost, port=9999, init_cs={
            key: data[key]
        }
    )

    udp.start()
    ndn.start()


if __name__ == '__main__':
    main()