from ControlTasks.ControlTaskBase import ControlTaskBase


class ClockManager(ControlTaskBase):
    def __init__():
        SFR.register("cycles", 0)

    def execute():
        cycle_num = SFR.get("cycles")
        cycle_num += 1
        SFR.set("cycles", cycle_num)