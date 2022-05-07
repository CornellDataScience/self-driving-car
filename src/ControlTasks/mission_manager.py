from .control_task_base import ControlTaskBase


class MissionManager(ControlTaskBase):
    def setup(self):
        self.var1 = self.config.get("var1")
        self.var2 = self.config.get("var2")
        self.var3 = self.config.get("var3")
        print(self.var1)
        print(self.var2)
        print(self.var3)

    def default(self):
        pass

    def execute(self):
        pass
