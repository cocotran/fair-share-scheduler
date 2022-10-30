# class used to encapsulate the specifications of each process
class Process:

    # default constructor
    def __init__(self, user: str, pid: int, ready_t: int, service_t: int):
        # user the process belongs to
        self._user_id = user
        # process number
        self._process_id = pid
        # amount of quantum time allocated to process
        self._quantum = 0
        # time at which the process is ready to be executed
        self._ready_time = ready_t
        # time left until process completes its execution
        self._time_left = service_t
        # process state
        self._state = None

    """ Getters """

    @property
    def user_id(self):
        return self._user_id

    @property
    def process_id(self):
        return self._process_id

    @property
    def quantum(self):
        return self._quantum

    @property
    def ready_time(self):
        return self._ready_time

    @property
    def time_left(self):
        return self._time_left

    @property
    def state(self):
        return self._state

    """ Setters """

    @time_left.setter
    def time_left(self, time):
        self._time_left = time

    @state.setter
    def state(self, new_state):
        self._state = new_state

    def set_quantum(self, new_quantum):
        self._quantum = new_quantum