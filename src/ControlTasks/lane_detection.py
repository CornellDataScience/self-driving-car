from .control_task_base import ControlTaskBase
from lane import get_lines
from lane import line

import glob
import matplotlib.image as mpimg
import cv2

import math

# https://github.com/maunesh/advanced-lane-detection-for-self-driving-cars


def calc_angle(l, r):
    arc_length = 20  # Find real length
    steering_wheel_angle = 0  # FIND THIS
    steering_ratio = 20  # Find real length
    wheel_base = 20  # Find real length

    # guide https://www.physicsforums.com/threads/steering-wheel-angle-radius-of-curvature.59881/

    # HANDLING DEVIATION = ???, maybe left then straight, would need to time

    road_info, curvature, deviation = line.get_measurements(l, r)

    if road_info == "Straight":
        return 0
    elif road_info == "curving to Left":
        steering_wheel_angle = -100 * steering_ratio * math.asin(wheel_base / curvature)
    elif road_info == "curving to Right":
        steering_wheel_angle = 100 * steering_ratio * math.asin(wheel_base / curvature)
    
    steering_wheel_angle + (float(deviation.split()[0][:-1])/5)

    return steering_wheel_angle


class LaneDetection(ControlTaskBase):
    def setup(self):
        self.left_line = None
        self.right_line = None

    def default(self):
        self.sfr.set("steering_angle", 0.0)

    # Take in frame and output direction to move and store in sfr?
    def execute(self):
        curr_frame = self.sfr.get("curr_frame")
        # curr_frame = cv2.imread(
        #     "lane/s-curve-road-skyline-drive-tucked-blue-ridge-mountains-shenandoah-national-park-virgina-31148867.jpeg"
        # )
        self.left_line, self.right_line = get_lines.pipeline(curr_frame)
        self.sfr.set("steering_angle", calc_angle(self.left_line, self.right_line))
        print("Angle to turn: " + str(self.sfr.get("steering_angle")))
