import cv2
import depthai as dai
import numpy as np
# Closer-in minimum depth, disparity range is doubled (from 95 to 190):
extended_disparity = False
# Better accuracy for longer distance, fractional disparity 32-levels:
subpixel = False
# Better handling for occlusions:
lr_check = False
# Create pipeline
pipeline = dai.Pipeline()
# Define sources and outputs
monoLeft = pipeline.create(dai.node.MonoCamera)
monoRight = pipeline.create(dai.node.MonoCamera)
depth = pipeline.create(dai.node.StereoDepth)
xout = pipeline.create(dai.node.XLinkOut)
xout.setStreamName("disparity")
# Properties
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
# Create a node that will produce the depth map (using disparity output as it's easier to visualize depth this way)
depth.initialConfig.setConfidenceThreshold(245)
# Options: MEDIAN_OFF, KERNEL_3x3, KERNEL_5x5, KERNEL_7x7 (default)
depth.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
depth.setLeftRightCheck(lr_check)
depth.setExtendedDisparity(extended_disparity)
depth.setSubpixel(subpixel)
f = 441.25
# Linking
monoLeft.out.link(depth.left)
monoRight.out.link(depth.right)
depth.disparity.link(xout.input)
# Connect to device and start pipeline
with dai.Device(pipeline) as device:
    print(device.Config)
    # Output queue will be used to get the disparity frames from the outputs defined above
    q = device.getOutputQueue(name="disparity", maxSize=4, blocking=False)
    while True:
        inDepth = q.get()  # blocking call, will wait until a new data has arrived
        frame = inDepth.getFrame()
        data = inDepth.getData().reshape(frame.shape) # flattened array of depth
        fx = f/frame.shape[1]
        fy = f/frame.shape[0]
        cloud = []
        cx = 640/frame.shape[1]
        cy = 360/frame.shape[0]
        for v in range(frame.shape[0]):
            for u in range(frame.shape[1]):
                x_c = (u - cx)*data[v, u]/fx
                y_c = (v - cy)*data[v, u]/fy
                cloud.append([x_c, y_c, data[v, u]])
        # Normalization for better visualization
        frame = (frame * (255 /  depth.initialConfig.getMaxDisparity())).astype(np.uint8)
        print(frame)
        cv2.imshow("disparity", frame)
        # Available color maps: https://docs.opencv.org/3.4/d3/d50/group__imgproc__colormap.html
        frame = cv2.applyColorMap(frame, cv2.COLORMAP_JET)
        cv2.imshow("disparity_color", frame)
        if cv2.waitKey(1) == ord('q'):
            break
