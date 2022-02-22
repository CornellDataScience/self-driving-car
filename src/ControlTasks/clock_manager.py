from .control_task_base import ControlTaskBase


class ClockManager(ControlTaskBase):
    def setup(self):
        pass

    def default(self):
        self.sfr.set("cycle_num", 0)

    def execute(self):
        cycle_num = self.sfr.get("cycle_num")
        cycle_num += 1

        print(f"[INFO] Cycle_num: {cycle_num}")
        self.sfr.set("cycle_num", cycle_num)
