import time
from threading import Thread, RLock

# 30 seconds interval
dead_interval = 30000000000


class MyLifecycle(Thread):
    def __init__(self, route_table, lock, timesleep, dead_interval):

        Thread.__init__(self)
        self.timesleep = timesleep
        self.route_table = route_table
        self.lock = lock
        self.dead_interval = dead_interval

    def run(self):
        while True:
            try:
                self.lock.acquire()
                self.lifecycle_table()

            finally:
                self.lock.release()
                time.sleep(timesleep)

    def lifecycle_table(self):
        for keys, value in list(self.route_table.items()):
            timenow = time.time_ns()
            timetable = value['timestamp']
            if timenow > timetable + self.dead_interval:
                self.route_table.pop(keys)
