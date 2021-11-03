from .control_task_base import ControlTaskBase

import cv2


class ReadCamera(ControlTaskBase):

    def setup(self):
        vc = cv2.VideoCapture(0)
        if vc.isOpened():
            # try to get the first frame
            rval, frame = vc.read()
        vc.release()

        self.execute() #TODO REMOVE

    def default(self):
        self.sfr.set("curr_frame", None)
        self.sfr.set("prev_frame", None)

    def execute(self):
        print("Reads frame from camera")
        vc = cv2.VideoCapture(0)
        current = self.sfr.get('curr_frame')
        self.sfr.set("prev_frame", current)
        if vc.isOpened():
            # try to get the first frame
            rval, frame = vc.read()
            self.sfr.set("curr_frame", frame)
        vc.release()
