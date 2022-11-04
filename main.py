from process import Process
from scheduler import Scheduler

if __name__ == '__main__':

    #Read file content from input.txt
    with open('input.txt', 'r') as file:
        lines = file.readlines()

    # get the time quantum of the program from the first line (4)
    quantum = int(lines.pop(0))
    
    #Defining the user names and number, ready time and service time for each process
    user_dict = {}
    ready_time = []
    service_time = []

    # store the user _name and number of processes as well as each process' ready time and service time in their respective variables
    for line in lines:
        if line[0].isalpha():
            user_dict[line.split(" ")[0]] = int(line.split(" ")[1].rstrip())
        else:
            ready_time.append(int(line.split(" ")[0]))
            service_time.append(int(line.split(" ")[1].rstrip()))

    file.close()

    # array of Process objects to be executed
    processes = []

    # Counter to traverse each list created
    list_counter = 0 
    # generate a Process object and add it to the list of processes
    for user in user_dict:
        for i in range(0, user_dict[user]):
            processes.append(Process(user, i, ready_time[list_counter], service_time[list_counter]))
            list_counter += 1

    # sort the processes list by ready time in ascending order (to be used as a queue)
    processes.sort(key=lambda x: x.ready_time, reverse=False)

    # run the scheduler
    Scheduler(processes, quantum)