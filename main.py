from clock import Clock
from scheduler import Scheduler
from process import Process, User
from scheduler import Scheduler

#open input.sample.txt file
def get_raw_input(file_name: str):
    with open(file_name, "r") as f:
        arr = [line.strip() for line in f.readlines()]
        f.close()
        return arr


def get_input_from_file(arr):
    config = {}
    #Get the time quantum of the program
    quantum_time = int(arr.pop(0))
    while arr:
        user = arr[0][0]
        processes_num = int(arr[0][2])
        config[user] = []
        arr.pop(0)
        for _ in range(processes_num):
            config[user].append(arr.pop(0))
    return quantum_time, config

# store the user _threads and processes threads in their respective variables
def get_users_and_processes(input_data):
    user_threads = []
    processes_threads = []
    for user in input_data.keys():
        user_thread = User(user)
        processes_thread = []
        # count used to traverse  list of process specifications
        count = 0
        for p in input_data[user]:
            processes_thread.append(Process(count, int(p[0]), int(p[2])))
            count += 1
        user_thread.set_process(processes_thread)
        user_threads.append(user_thread)
        processes_threads += processes_thread
    return user_threads, user_threads + processes_threads


if __name__ == "__main__":
    # initialize the output file for writing
    open('output.txt', 'w').close() # reset
    config = get_raw_input("input.sample.txt")
    quantum_time, input_data = get_input_from_file(config)
    user_threads, all_threads = get_users_and_processes(input_data)

    # Set up
    clock = Clock(0.5)
    scheduler = Scheduler(quantum_time, clock, "Scheduler", user_threads)
     # run the scheduler & clock
    clock.start()
    scheduler.start()
    for t in all_threads:
        t.start()

    for t in all_threads:
        t.join()
    scheduler.join()
    clock.join()
