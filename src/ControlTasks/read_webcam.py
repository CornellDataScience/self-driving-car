from .control_task_base import ControlTaskBase
import cv2


class Webcam(ControlTaskBase):
    def setup(self):
        self.vc = cv2.VideoCapture(0)
        if self.vc.isOpened():
            # try to get the first frame
            rval, frame = self.vc.read()

        # to make processing code happy
        self.execute()  #TODO REMOVE

    def default(self):
        self.sfr.set("curr_frame", None)
        self.sfr.set("prev_frame", None)

    def execute(self):
        current = self.sfr.get('curr_frame')
        self.sfr.set("prev_frame", current)
        if self.vc.isOpened():
            # try to get the first frame
            rval, frame = self.vc.read()
            self.sfr.set("curr_frame", frame)
