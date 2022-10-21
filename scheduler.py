from clock import Clock
from observable import Subscriber


class Scheduler(Subscriber):
    def __init__(self, clock: Clock, name: str) -> None:
        super().__init__(name)
        clock.register(self)
