class Process:

    # default constructor
    def __init__(self, user: str, pid: int, ready_t: int, service_t: int):
        # User process
        self._user_id = user
        self._process_id = pid
        self._quantum = 0
        self._ready_time = ready_t
        self._time_left = service_t
        # process state
        self._state = None

    #Getters
    
    @property           #creating read-only properties using property() as a decorator
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

    #Setters
    
    def set_quantum(self, new_quantum):
        self._quantum = new_quantum

    @time_left.setter
    def time_left(self, time):
        self._time_left = time

    @state.setter
    def state(self, new_state):
        self._state = new_state

   