from .control_task_base import ControlTaskBase

class PointTracker(ControlTaskBase):
    def __init__(self, config, sfr):
        self.config = config
        self.sfr = sfr
        
    def initialize(self):
        pass

    def default(self):
        pass

    def execute(self):
        print("Tracking points.")
        pass
