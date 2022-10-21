from time import sleep
from threading import Thread


class Clock(Thread):
    def __init__(self, secs=1) -> None:
        self._secs = secs
        self._step = 1
        self._running = False
        self.current_time = 1   # stated in A2 description
        Thread.__init__(self)

    def start(self) -> None:
        self._running = True
        while self._running:
            print(self.current_time)
            self.current_time += self._step
            sleep(self._secs)    # for testing purpose
    
    def stop(self) -> None:
        self._running = False