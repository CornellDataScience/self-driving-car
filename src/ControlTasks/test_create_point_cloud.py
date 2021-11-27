import numpy as np
from .control_task_base import ControlTaskBase


class TestCreatePointCloud(ControlTaskBase):
    def setup(self):
        pass

    def default(self):
        pass

    def execute(self):
        points = np.zeros((100000, 3)) * 10
        self.sfr.set("point_cloud", points)
