from .control_task_base import ControlTaskBase

class ReadCamera(ControlTaskBase):
    def __init__(self, config, sfr):
        super.__init__(sfr)
        self.config = config
        
    def initialize(self):
        pass

    def default(self):
        pass

    def execute(self):
        print("Read from Camera")
        pass
