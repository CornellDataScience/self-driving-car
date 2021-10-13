from .control_task_base import ControlTaskBase
import time

class ClockManager(ControlTaskBase):
    def __init__(self):
        self.time = 0
        self.sfr = None

    def default(self):
        pass

    def execute(self):
        print(self.time)
        self.time += 1
        time.sleep(0.001)