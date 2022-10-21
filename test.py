from time import sleep
from threading import Thread

from clock import Clock
from scheduler import Scheduler


clock = Clock()
scheduler = Scheduler(clock, "Scheduler 1")

clock.start()