# break up into smaller control tasks as needed
from .control_task_base import ControlTaskBase
import cv2
import numpy as np


class DisplayFrameWithDepth(ControlTaskBase):
    def setup(self):
        cv2.namedWindow("preview")
        # cv2.namedWindow("depth")

    def default(self):
        pass

    def execute(self):
        processed_frame = self.sfr.get("processed_frame")
        if processed_frame is not None:
            cv2.imshow("preview", processed_frame)
        else:
            print("Processed_frame was None")

        depth_frame = (self.sfr.get("depth_frame") *
                       (255 / self.sfr.get("depth_max_disparity"))).astype(
                           np.uint8)
        if depth_frame is not None:
            cv2.imshow("depth", depth_frame)
        else:
            print("depth_frame was None")

        cv2.waitKey(1)
