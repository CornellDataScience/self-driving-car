from src.ControlTasks.control_task_base import ControlTaskBase

import cv2


class StaticFrame(ControlTaskBase):
    def setup(self):
        # load an image saved in the codebase
        self.static_frame = cv2.imread("src/resources/cornell_road.png")
        # to make processing code happy
        self.execute()

    def default(self):
        self.sfr.set("curr_frame", None)
        self.sfr.set("prev_frame", None)

    """returns a fixed image frame"""

    def execute(self):
        self.sfr.set("curr_frame", self.static_frame)
        self.sfr.set("prev_frame", self.static_frame)