from .control_task_base import ControlTaskBase
import time

class ClockManager(ControlTaskBase):
    def default(self):
        self.sfr.set('time', 0)

    def execute(self):
        local_time = self.sfr.get('time')
        local_time += 1
        print(local_time)
        self.sfr.set('time', local_time)

        time.sleep(0.001)