import threading
import time


# class used to handle the fair-share process scheduling and write to output.txt
class Scheduler:

    # default constructor
    def __init__(self, m_processes: list, m_quantum):
        # initialize the output file for writing
        self._output = open("output.txt", "w")
        self._new_processes = m_processes
        # queue of processes ready to be executed
        self._ready_queue = []
        # holds the elapsed time of the program
        self._total_elapsed_time = time.perf_counter()
        # holds (key) current active user(s) and (value) the number of active process(es) of the user(s)
        self._users_dict = {}
        # holds quantum value
        self._quantum = m_quantum
        # holds the time where a process starts/resumes running
        self._time_start = 0

        # check if a new process needs to be added to ready queue and/or execute a process in the ready queue
        while len(self._new_processes) or len(self._ready_queue):
            # update the elapsed time
            self._total_elapsed_time = time.perf_counter()
            # check if any new processes are ready to be executed
            self.verify_if_ready()
            # while there are processes waiting in the ready queue, dequeue a process and execute it using a single thread
            if len(self._ready_queue) != 0:
                t = threading.Thread(target=self.execute, args=(self._ready_queue.pop(0),))
                t.start()
                t.join()

        self._output.close()

    # add a process to the ready queue if its ready to run
    def verify_if_ready(self):
        if len(self._new_processes) != 0:
            for process in self._new_processes:
                if process.ready_time <= int(self._total_elapsed_time):
                    # adds a new user and process to dict, and increments existing users with a new process
                    key = process.user_id
                    if key in self._users_dict.keys():
                        self._users_dict[key] += 1
                    else:
                        self._users_dict[key] = 1
                    # add process to ready queue
                    self._ready_queue.append(process)
                    # remove process from new_processes queue
                    self._new_processes.pop(0)
                else:
                    break
            self.quantum_alloc()

    # update the quantum of each process remaining in the ready queue
    def quantum_alloc(self):
        for process in self._ready_queue:
            updated_quantum = int(self._quantum // len(self._users_dict) // self._users_dict[process.user_id])
            process.set_quantum(updated_quantum)

    # execute a process
    def execute(self, process):
        # thread has started its execution
        if process.state is None:
            self.write_to_output(process, 'Started')
            self.write_to_output(process, 'Resumed')
            self._time_start = time.perf_counter()
        # paused thread has resumed execution
        elif process.state == 'Paused':
            process.state = 'Resumed'
            self.write_to_output(process, 'Resumed')
            self._time_start = time.perf_counter()

        while True:
            # update the elapsed time
            self._total_elapsed_time = time.perf_counter()
            # check if any other processes became ready
            self.verify_if_ready()
            # break out of loop if time quantum is used up or process is finished
            # done in if-elif instead of 'or' for easier readability
            if self._total_elapsed_time - self._time_start >= process.quantum:
                process.time_left = process.time_left - process.quantum
                break
            elif self._total_elapsed_time - self._time_start >= process.time_left:
                process.time_left = process.time_left - process.quantum
                break

        # if the process is finished executing, report the finished status to output
        if process.time_left <= 0:
            self.write_to_output(process, 'Paused')
            self.write_to_output(process, 'Finished')

            # decrement the number of running processes for the users_dict
            self._users_dict[process.user_id] -= 1
            # remove a user from users_dict if it has no more processes
            if self._users_dict[process.user_id] == 0:
                self._users_dict.pop(process.user_id)
            # update remaining processes quantum
            self.quantum_alloc()
        # if the process needs more time to execute, set its state to 'Paused' and add it back to the ready queue
        else:
            process.state = 'Paused'
            self.write_to_output(process, 'Paused')
            # Send paused process to back of ready_queue
            self._ready_queue.append(process)

    # print output message to file
    def write_to_output(self, process, state):
        self._output.write(
            "Time {}, User {}, Process {}, {}\n".format(
                int(self._total_elapsed_time), process.user_id,
                process.process_id,
                state))
