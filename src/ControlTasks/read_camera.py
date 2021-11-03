from .control_task_base import ControlTaskBase
import cv2

class ReadCamera(ControlTaskBase):
    def setup(self):
        self.vc = cv2.videoCapture(0)

    def default(self):
        self.sfr.set("prev_frame", None)
        self.sfr.set("curr_frame", None)

    def execute(self):
        print("Read from Camera")
        # poll the frames
        # add current frame and update last frame in sfr
        rval, frame = self.vc.read()
        curr_frame = self.sfr.get("curr_frame")
        self.sfr.set("prev_frame", curr_frame)
        self.sfr.set("curr_frame", frame)
