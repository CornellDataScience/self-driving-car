from .control_task_base import ControlTaskBase

import cv2


class ReadCamera(ControlTaskBase):

    def initialize(self):
        vc = cv2.VideoCapture(0)
        if vc.isOpened():
            # try to get the first frame
            rval, frame = vc.read()
        vc.release()

    def default(self):
        self.sfr.set("frame", 0)

    def execute(self):
        print("Reads frame from camera")
        vc = cv2.VideoCapture(0)
        # get next frame from camera and push to statefeldregistry
        while rval:
            rval, frame = vc.read()
        vc.release()
        self.sfr["frame"] = self.frame
