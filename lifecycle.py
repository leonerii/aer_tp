import time

ip_add = {
    "timestamp": 1,
    "next_hop": None
}

route_table = {}

route_table.update(ip_add)

t = time.localtime()


def lifecycle_table(route_table):
    for keys, values in route_table.items():
        timenow = time.localtime()
        if timenow.tm_min - route_table["timestamp"] < timenow.tm_min:
            print('Delete')
            #del route_table[ip_add]


print(t.tm_min)
lifecycle_table(route_table)
