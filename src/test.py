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

    # maxDisp = config.getMaxDisparity()
    # subpixelLevels = pow(2, config.get().algorithmControl.subpixelFractionalBits)
    # subpixel = config.get().algorithmControl.enableSubpixel
    # dispIntegerLevels = maxDisp if not subpixel else maxDisp / subpixelLevels

    frame = image.getFrame()

    # frame.tofile(name+".raw")

    # if name == 'depth':
    #     dispScaleFactor = baseline * focal
    #     with np.errstate(divide='ignore'):
    #         frame = dispScaleFactor / frame

    #     frame = (frame * 255. / dispIntegerLevels).astype(np.uint8)
    #     frame = cv2.applyColorMap(frame, cv2.COLORMAP_HOT)
    # elif 'confidence_map' in name:
    #     pass
    # elif name == 'disparity_cost_dump':
    #     # frame.tofile(name+'.raw')
    #     pass
    # elif 'disparity' in name:
    #     if 1: # Optionally, extend disparity range to better visualize it
    #         frame = (frame * 255. / maxDisp).astype(np.uint8)

    #     # if 1: # Optionally, apply a color map
    #     #     frame = cv2.applyColorMap(frame, cv2.COLORMAP_HOT)

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

        # inCfg = device.getOutputQueue("stereo_cfg", 8, blocking=False)
        # currentConfig = inCfg.get()
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






