import time
from threading import Thread, RLock



class MyLifecycle(Thread):
    def __init__(self, route_table, lock, dead_interval):

        Thread.__init__(self)
        self.route_table = route_table
        self.lock = lock
        self.dead_interval = dead_interval

    def run(self):
        while True:
            try:
                print("rodei")
                self.lock.acquire()
                self.lifecycle_table()

            finally:
                self.lock.release()
                time.sleep(self.dead_interval)

    def lifecycle_table(self):
        for keys, value in list(self.route_table.items()):
            timenow = time.time()
            timetable = value['timestamp']
            if timenow > timetable + self.dead_interval:
                self.route_table.pop(keys)
