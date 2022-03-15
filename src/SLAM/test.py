import depthai as dai
import cv2
import math
import numpy as np

pipeline = dai.Pipeline()

monoL = pipeline.create(dai.node.MonoCamera)
monoR = pipeline.create(dai.node.MonoCamera)

monoL.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoR.setBoardSocket(dai.CameraBoardSocket.RIGHT)

xoutL = pipeline.create(dai.node.XLinkOut)
xoutR = pipeline.create(dai.node.XLinkOut)

xoutL.setStreamName('left')
xoutR.setStreamName('right')

monoL.setResolution(
    dai.MonoCameraProperties.SensorResolution.THE_720_P)
monoR.setResolution(
dai.MonoCameraProperties.SensorResolution.THE_720_P)

# monoL.setVideoSize(960, 540)
# monoR.setVideoSize(960, 540)

xoutL.input.setBlocking(False)
xoutR.input.setBlocking(False)

xoutL.input.setQueueSize(1)
xoutR.input.setQueueSize(1)

monoL.out.link(xoutL.input)
monoR.out.link(xoutR.input)

baseline = 75
fov = 71.86
width=1280
focal = width/(2*math.tan(fov/2/180*math.pi))

def convertToCv2Frame(name, image, config):
    frame = image.getFrame()
    return frame

print("before device")
with dai.Device(pipeline) as device:
    print("with device")
    streams = ['left', 'right']
    q_list = []
    while True:
        for s in streams:
            q = device.getOutputQueue(s, 8, blocking=False)
            q_list.append(q)
            print("loop 1 done")
        print("config got")

        queues = q_list.copy()
        for q in queues:
            data = q.get()
            print("data got")
            frame = convertToCv2Frame(q.getName(), data, None)
            cv2.imshow(q.getName(), frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
