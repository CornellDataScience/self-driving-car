from .control_task_base import ControlTaskBase
import time

class ClockManager(ControlTaskBase):
    def __init__(self):
        self.SFR.set("time", 0)

    def default(self):
        pass

    def execute(self):
        print(self.SFR.get("time"))
        self.SFR.set("time", self.SFR.get("time") + 1)
        time.sleep(0.001)