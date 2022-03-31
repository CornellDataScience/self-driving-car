from .control_task_base import ControlTaskBase
import numpy as np

class WritePointCloud(ControlTaskBase):
    def setup(self):
        pass
    
    def default(self):
        with open('cloud.npy', 'a+') as f:
            np.save(f, np.zeros(10, 3))

    def execute(self):
        with open('cloud.npy', 'a+') as f:
            np.save(f, np.array([self.sfr.get('point_map')]))
