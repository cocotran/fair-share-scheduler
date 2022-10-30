# import the necessary packages
from process import Process
from scheduler import Scheduler

# entrypoint of script execution
if __name__ == '__main__':

    # open input.txt and read file content
    with open('input.txt', 'r') as file:
        lines = file.readlines()

    # get the time quantum of the program
    quantum = int(lines.pop(0))

    # dictionary containing the user names and number of processes under each user
    user_dict = {}
    # list containing the ready time for each process
    ready_time = []
    # list containing the service time for each process
    service_time = []

    # store the user _name and number of processes as well as each process' ready time and service time in their respective variables
    for line in lines:
        if line[0].isalpha():
            user_dict[line.split(" ")[0]] = int(line.split(" ")[1].rstrip())
        else:
            ready_time.append(int(line.split(" ")[0]))
            service_time.append(int(line.split(" ")[1].rstrip()))

    # close the file
    file.close()

    # array of Process objects to be executed
    processes = []

    # counter used to traverse each previously generated list for process specifications
    counter = 0 
    # generate a Process object and add it to the list of processes
    for user in user_dict:
        for i in range(0, user_dict[user]):
            processes.append(Process(user, i, ready_time[counter], service_time[counter]))
            counter += 1

    # sort the processes list by ready time in ascending order (to be used as a queue)
    processes.sort(key=lambda x: x.ready_time, reverse=False)

    # run the scheduler
    Scheduler(processes, quantum)