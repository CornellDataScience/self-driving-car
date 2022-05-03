from .control_task_base import ControlTaskBase
from lane import get_lines
from lane import line
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
        steering_wheel_angle = steering_ratio * math.asin(wheel_base / curvature)
    elif road_info == "curving to Right":
        steering_wheel_angle = steering_ratio * math.asin(wheel_base / curvature)

    return steering_wheel_angle


class LaneDetection(ControlTaskBase):
    def setup(self):
        self.left_line = None
        self.right_line = None

    def default(self):
        self.sfr.set("angle", 0.0)

    # Take in frame and output direction to move and store in sfr?
    def execute(self):
        print("executing Lane")
        curr_frame = self.sfr.get("curr_frame")
        self.left_line, self.right_line = get_lines.pipeline(curr_frame)
        self.sfr.set("angle", calc_angle(self.left_line, self.right_line))
        print("DETECTING LANES")
        print("angle to turn:" + self.sfr.get("angle"))
