# Descrition: Implement a class to run a tread on a single run
# of a watch dog timer.
# Date: 03/30/2013

import threading
import time

class RunerThread(threading.Thread):

    def __init__(self, id, timeout, interval = 0.1) -> None:
        threading.Thread.__init__(self)
        self._id = id
        self._timeout = timeout
        self._interval = interval
        self._stop_event = threading.Event()
    
    def start(self) -> None:
        self._start_time = time.time()
        return super().start()

    def set_timeout(self, timeout):
        self._timeout = timeout
    
    def time_left(self):
        return self._timeout - (time.time() - self._start_time)

    def run(self):
        while not self._stop_event.is_set():
            if time.time() - self._start_time > self._timeout:
                self.stop()
            time.sleep(self._interval)

    def stop(self):
        self._stop_event.set()