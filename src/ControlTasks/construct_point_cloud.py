from .control_task_base import ControlTaskBase


class PointCloud(ControlTaskBase):
    def setup(self):
        pass

    def default(self) -> None:
        self.sfr.set('point_cloud', None)

    def execute(self) -> None:
        depth_frame = self.sfr.get('depth_frame')
        depth_data = self.sfr.get('depth_data')

        f = 441.25
        fx = f / depth_frame.shape[1]
        fy = f / depth_frame.shape[0]
        cloud = []
        cx = 640  #/depth_frame.shape[1]
        cy = 360  #/depth_frame.shape[0]
        for v in range(depth_frame.shape[0]):
            for u in range(depth_frame.shape[1]):
                x_c = (u - cx) * depth_data[v, u] / fx
                y_c = (v - cy) * depth_data[v, u] / fy
                cloud.append([x_c, y_c, depth_data[v, u]])

        self.sfr.set('point_cloud', cloud)