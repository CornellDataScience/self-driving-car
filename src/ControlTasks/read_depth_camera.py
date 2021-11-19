from .control_task_base import ControlTaskBase

import cv2
import depthai as dai


class DepthCamera(ControlTaskBase):
    def setup(self):
        # Create Pipeline
        pipeline = dai.Pipeline()

        # Define source and input
        camRgb = pipeline.create(dai.node.ColorCamera)
        xoutVideo = pipeline.create(dai.node.XLinkOut)

        xoutVideo.setStreamName("video")

        # Properties
        camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        camRgb.setResolution(
            dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        # camRgb.setVideoSize(960, 540)
        camRgb.setVideoSize(1920, 1080)

        xoutVideo.input.setBlocking(False)
        xoutVideo.input.setQueueSize(1)

        # Linking
        camRgb.video.link(xoutVideo.input)

        self.pipeline = pipeline
        self.device = dai.Device(self.pipeline)
        # with dai.Device(pipeline) as device:
        #     self.video = device.getOutputQueue(name="video", maxSize=1, blocking=False)
        # self.videoIn = video.get()
        self.execute()  # TODO: Get rid of later

    def default(self):
        self.sfr.set("curr_frame", None)
        self.sfr.set("prev_frame", None)

    def execute(self):
        print("Reads frame from camera")
        # with self.device as device:
        # video = device.getOutputQueue(name="video", maxSize=1, blocking=False)
        video = self.device.getOutputQueue(name="video",
                                           maxSize=1,
                                           blocking=False)
        videoIn = video.get()

        current = self.sfr.get('curr_frame')
        self.sfr.set("prev_frame", current)

        frame = videoIn.getCvFrame()
        self.sfr.set("curr_frame", frame)
        print("Done")
