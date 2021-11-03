from .control_task_base import ControlTaskBase

import cv2


class ReadCamera(ControlTaskBase):

    def initialize(self):
        vc = cv2.VideoCapture(0)

        if vc.isOpened():
            # try to get the first frame
            rval, frame = vc.read()
            prev_frame = None
        else:
            rval = False

    def default(self):

    def execute(self):
        print("Reads frame from camera")
        vc = cv2.VideoCapture(0)
        # get next frame from camera and push to statefeldregistry
        while rval:
            prev_frame = frame
            rval, frame = vc.read()

        vc.release()

        self.sfr["frame"] = self.frame
