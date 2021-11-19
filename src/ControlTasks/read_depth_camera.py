from .control_task_base import ControlTaskBase

import depthai as dai


class DepthCamera(ControlTaskBase):
    def setup(self):
        # Create Pipeline
        pipeline = dai.Pipeline()

        self.rgb_setup(pipeline)
        self.depth_setup(pipeline)

        self.pipeline = pipeline
        self.device = dai.Device(self.pipeline)

        # Connect to device and start pipeline
        # Output queue will be used to get the disparity frames from the outputs defined above
        self.disparity_q = self.device.getOutputQueue(name="disparity",
                                                      maxSize=4,
                                                      blocking=False)

        # with dai.Device(pipeline) as device:
        #     self.video = device.getOutputQueue(name="video", maxSize=1, blocking=False)
        # self.videoIn = video.get()
        self.execute()  # TODO: Get rid of later

    def default(self):
        self.sfr.set("curr_frame", None)
        self.sfr.set("prev_frame", None)
        self.sfr.set("depth_frame", None)
        self.sfr.set("depth_data", None)

    def execute(self):
        print("Reads frame from camera")
        self.rgb_execute()
        self.depth_execute()
        print("Done")

    def rgb_setup(self, pipeline):
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

    def depth_setup(self, pipeline):
        # Closer-in minimum depth, disparity range is doubled (from 95 to 190):
        extended_disparity = False
        # Better accuracy for longer distance, fractional disparity 32-levels:
        subpixel = False
        # Better handling for occlusions:
        lr_check = False

        # Define sources and outputs
        monoLeft = pipeline.create(dai.node.MonoCamera)
        monoRight = pipeline.create(dai.node.MonoCamera)
        depth = pipeline.create(dai.node.StereoDepth)
        xout = pipeline.create(dai.node.XLinkOut)

        xout.setStreamName("disparity")

        # Properties
        monoLeft.setResolution(
            dai.MonoCameraProperties.SensorResolution.THE_400_P)
        monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
        monoRight.setResolution(
            dai.MonoCameraProperties.SensorResolution.THE_400_P)
        monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)

        # Create a node that will produce the depth map (using disparity output as it's easier to visualize depth this way)
        depth.initialConfig.setConfidenceThreshold(245)
        # Options: MEDIAN_OFF, KERNEL_3x3, KERNEL_5x5, KERNEL_7x7 (default)
        depth.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
        depth.setLeftRightCheck(lr_check)
        depth.setExtendedDisparity(extended_disparity)
        depth.setSubpixel(subpixel)

        # Linking
        monoLeft.out.link(depth.left)
        monoRight.out.link(depth.right)
        depth.disparity.link(xout.input)

        self.sfr.set("depth_max_disparity",
                     depth.initialConfig.getMaxDisparity())

    def rgb_execute(self):
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

    def depth_execute(self):
        inDepth = self.disparity_q.get(
        )  # blocking call, will wait until a new data has arrived
        depth_frame = inDepth.getFrame()
        depth_data = inDepth.getData()  # flattened array of depth

        # populate the SFR
        self.sfr.set("depth_frame", depth_frame)
        self.sfr.set("depth_data", depth_data)
