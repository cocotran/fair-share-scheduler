from time import sleep
from threading import Thread

from observable import Publisher


class Clock(Publisher, Thread):
    def __init__(self, secs=1) -> None:
        Publisher.__init__(self)
        self._secs = secs
        self._step = 1
        self._running = False
        self.current_time = 1  # stated in A2 description
        Thread.__init__(self)

    def start(self) -> None:
        self.dispatch(self.current_time)
        self._running = True
        while self._running:
            self.current_time += self._step
            self.dispatch(self.current_time)
            sleep(self._secs)  # for testing purpose

    def stop(self) -> None:
        self._running = False
