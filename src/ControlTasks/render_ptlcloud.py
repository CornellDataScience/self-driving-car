from .control_task_base import ControlTaskBase
import open3d as o3d
import numpy as np

class RenderPointCloud(ControlTaskBase):
    def setup(self):
        pass
    
    def default(self):
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(np.zeros(3, 10))
        o3d.visualization.draw_geometries([pcd])


    def execute(self):
        points = np.load("cloud.npy")
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)
        o3d.visualization.draw_geometries([pcd])
