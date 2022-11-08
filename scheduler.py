from threading import Thread

from clock import Clock
from observable import Subscriber


class Scheduler(Subscriber, Thread):
    def __init__(self, quantum: int, clock: Clock, name: str, user=[]) -> None:
        Thread.__init__(self)
        Subscriber.__init__(self, name)
        clock.register(self)
        self._clock = clock
        self._quantum = quantum
        self._users = user
        self._user_queue = []  # list of Users with ready processes
        self._process_queue = []

    def update(self, message):
        if message == 0:
            return

        self.update_user_queue(message)
        if message % self._quantum == 1:  # new  cycle
            self.calculate_time()

        if not self._process_queue:
            self._clock.stop()
            return

        item = self._process_queue[0]
        process = item["process"]
        if item["time"] > 0:
            process.execute(message)
            item["time"] -= 1
        if item["time"] <= 0 and process.state != "finished":
            process.pause(message + 1)
            self._process_queue.pop(0)
        elif process.state == "finished":
            self._process_queue.pop(0)
            if item["time"] > 0:    # if not all allocated time is used
                self.update_user_queue(message)
                self.calculate_time()   # force new cycle

    def update_user_queue(self, current_time: int) -> None:
        self._user_queue = []  # reset
        for user in self._users:
            user.update(current_time)
            if user.has_ready_process():
                self._user_queue.append(user)

    def calculate_time(self) -> None:
        self._process_queue = []  # reset
        if len(self._user_queue):
            user_time = self._quantum / len(self._user_queue)
            for user in self._user_queue:
                process_time = user_time / len(user.process_queue)
                for process in user.process_queue:
                    self._process_queue.append(
                        {"process": process, "time": int(process_time)}
                    )
