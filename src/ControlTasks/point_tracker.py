from .control_task_base import ControlTaskBase

class PointTracker(ControlTaskBase):
    def __init__(self, config, sfr):
        super.__init__(sfr)
        self.config = config
        
    def initialize(self):
        pass

    def default(self):
        pass

    def execute(self):
        print("Tracking points.")
        pass
