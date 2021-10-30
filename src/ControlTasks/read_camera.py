from .control_task_base import ControlTaskBase


class ReadCamera(ControlTaskBase):

    def __init__(self, config, sfr, frame):
        self.config = config
        self.sfr = sfr
        self.frame = frame

    def initialize(self):
        pass

    def default(self):
        pass

    def execute(self):
        print("Reads frame from camera")
        self.sfr["frame"] = self.frame
