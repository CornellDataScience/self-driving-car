from .control_task_base import ControlTaskBase


def run_model(frame):
    pass


def calc_angle(processed_frame):
    pass


class LaneDetection(ControlTaskBase):
    def setup(self):
        pass

    def default(self):
        self.sfr.set("angle", 0.0)

    # Take in frame and output direction to move and store in sfr?
    def execute(self):
        curr_frame = self.sfr.get("curr_frame")
        self.sfr.set("angle", calc_angle(run_model(curr_frame)))
