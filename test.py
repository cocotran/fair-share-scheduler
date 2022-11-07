from clock import Clock
from scheduler import Scheduler
from process import Process, User
from scheduler import Scheduler


clock = Clock(0.5)

p1 = Process("0", 4, 3)
p2 = Process("1", 1, 5)
p3 = Process("0", 5, 6)
# p4 = Process("4", 6, 1)
# p5 = Process("5", 7, 1)

u_1 = User("A")
u_1.set_process([p1, p2])
u_2 = User("B")
u_2.set_process([p3])

scheduler = Scheduler(4, clock, "Scheduler 1", [u_1, u_2])

clock.start()