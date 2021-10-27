from .control_task_base import ControlTaskBase
import time

class ClockManager(ControlTaskBase):
    def __init__(self, config, sfr):
        self.time = 0
        self.config = config
        self.sfr = sfr

    def default(self):
        pass

    def execute(self):
        print(self.time)
        self.time += 1
        time.sleep(0.001)