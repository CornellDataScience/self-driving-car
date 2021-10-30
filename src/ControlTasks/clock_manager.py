from .control_task_base import ControlTaskBase
import time

class ClockManager(ControlTaskBase):
    def __init__(self, config, sfr):
        super().__init__(sfr)
        self.config = config

    def default(self):
        self.sfr.set('time', 0)

    def execute(self):
        print('Time: ' + self.sfr.get('time'))
        self.sfr.set('time', self.sfr.get('time') + 1)
        time.sleep(0.001)