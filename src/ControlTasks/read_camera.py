from .control_task_base import ControlTaskBase

import cv2


class ReadCamera(ControlTaskBase):

    def setup(self):
        vc = cv2.VideoCapture(0)
        if vc.isOpened():
            # try to get the first frame
            rval, frame = vc.read()
        vc.release()

    def default(self):
        curr_frame = None
        prev_frame = None

    def execute(self):
        print("Reads frame from camera")
        vc = cv2.VideoCapture(0)

        # get next frame from camera and push to statefeldregistry
        while rval:
            prev_frame = curr_frame
            rval, curr_frame = vc.read()
        vc.release()
        self.sfr["frame"] = self.frame
