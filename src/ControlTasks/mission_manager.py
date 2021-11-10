from .control_task_base import ControlTaskBase
import time


class MissionManager(ControlTaskBase):
    def initialize(self):
        self.var1 = self.config["var1"]
        self.var2 = self.config["var2"]
        self.var3 = self.config["var3"]
        print(self.var1)
        print(self.var2)
        print(self.var3)

    def default(self):
        pass

    def execute(self):
        pass
