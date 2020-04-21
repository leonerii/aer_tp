import time
from threading import Thread, RLock


# ip_add = {
#    "timestamp": 1587411934636039986,
#    "next_hop": None
# }

# 30 seconds interval
dead_interval = 30000000000
# 15 seconds sleep
timesleep = 15
route_table = {}

# route_table['192.168.1.10'] = ip_add
# route_table['192.168.1.09'] = ip_add
# route_table['192.168.1.08'] = ip_add


class MyLifecycle(Thread):
    def __init__(self, route_table):

        Thread.__init__(self)
        self.route_table = route_table
        #self.lock = lock

    def lifecycle_table(self):
        while True:
            for keys, value in list(route_table.items()):
                timenow = time.time_ns()
                print(timenow)
                timetable = value['timestamp']
                print(route_table)
                if timenow > timetable + dead_interval:
                    print('Delete')
                    route_table.pop(keys)
            time.sleep(timesleep)


run = MyLifecycle(route_table)
run.lifecycle_table()
