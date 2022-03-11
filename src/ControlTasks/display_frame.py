# break up into smaller control tasks as needed
from .control_task_base import ControlTaskBase
import cv2


class DisplayFrame(ControlTaskBase):
    def setup(self):
        cv2.namedWindow("preview")

    def default(self):
        pass

    def execute(self):
        processed_frame = self.sfr.get("processed_frame")
        if processed_frame is not None:
            cv2.imshow("preview", processed_frame)
        else:
            print("Processed_frame was None")
        cv2.waitKey(1)
