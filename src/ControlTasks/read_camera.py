from .control_task_base import ControlTaskBase

class ReadCamera(ControlTaskBase):
    def initialize(self):
        pass

    def default(self):
        pass

    def execute(self):
        print("Read from Camera")
        # poll the frames
        # add current frame and update last frame in sfr
        pass
