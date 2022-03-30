import depthai as dai
import cv2
import g2o
import math
import numpy as np

from threading import Thread

from slam import SLAM
from components import Camera
from components import StereoFrame
from feature import ImageFeature
from params import Params

params = Params()

slam = SLAM(params)

cam = Camera(
    718.856, 718.856, 607.1928, 185.2157,
    1280, 370, 0.1, 50.0)

i = 0
#  while True:
img_l = cam.left()
img_r = cam.right()
cv2.imshow("left", img_l)
cv2.imshow("right", img_r)
cv2.waitKey(0)

img_l = cam.left()
img_r = cam.right()
#  print("img_l: ", img_l)
cv2.imshow("left", img_l)
cv2.imshow("right", img_r)
cv2.waitKey(0)

featurel = ImageFeature(img_l, params) # process_frame.get_features(Cam.left)
featurer = ImageFeature(img_r, params) # process_frame.get_features(Cam.right)
#  timestamp = dataset.timestamps[i]

#  time_start = time.time()

t = Thread(target=featurer.extract)
t.start()
featurel.extract()
t.join()

featurel.draw_keypoints(delay=0)
featurer.draw_keypoints(delay=0)

frame = StereoFrame(i, g2o.Isometry3d(), featurel, featurer, cam)

slam.initialize(frame)

i += 1



