from threading import Thread

# default constructor
class Process(Thread):
    def __init__(self, id: str, arrive_time: int, quantum_time: int, user=None) -> None:
        Thread.__init__(self)
        # process number
        self.id = id
        # time at which the process arrives
        self.arrive_time = arrive_time
        # amount of quantum time allocated to process
        self._quantum_time = quantum_time
         # process state
        self.state = "not ready"
        self._user = user

    def __repr__(self) -> str:
        return f"Process{self.id}: {self._quantum_time}-{self.state}"

    def set_user(self, user):
        self._user = user
     #Execution of processes
    def execute(self, current_time: int, step=1):
        # thread has started its execution
        if self._quantum_time > 0:
            if self.state == "ready":
                self.state = "started"
                self.log(current_time)
                # paused thread has resumed execution
            elif self.state == "paused":
                self.state = "resumed"
                self.log(current_time)

            self._quantum_time -= step

        if self._quantum_time <= 0:
            self.state = "finished"
            self._user.remove_process(self.id)
            self.log(current_time + 1)

    def pause(self, current_time):
        self.state = "paused"
        self.log(current_time)
      # print output message to file
    def log(self, current_time: int) -> None:
        msg = f"Time {current_time}, User {self._user}, Process {self.id}, {self.state}"
        print(msg)
        with open("output.txt", "a") as f:
            f.write(msg + "\n")
            f.close()


class User(Thread):
    def __init__(self, name: str, processes=[]) -> None:
        Thread.__init__(self)
        self.name = name
        self.processes = processes
        self.process_queue = []

    def __repr__(self) -> str:
        return self.name

    def set_process(self, processes):
        self.processes = processes
        for process in self.processes:
            process.set_user(self)

    def update(self, message):
        for process in self.processes:
            if message == process.arrive_time:
                self.update_queue(process)
                self.processes.remove(process)

    def has_ready_process(self) -> bool:
        return len(self.process_queue) > 0

    def update_queue(self, process: Process) -> None:
        self.process_queue.append(process)
        process.state = "ready"

    def remove_process(self, process_id):
        for process in self.process_queue:
            if process.id == process_id:
                self.process_queue.remove(process)
