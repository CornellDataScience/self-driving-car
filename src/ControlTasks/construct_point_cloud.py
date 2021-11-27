from .control_task_base import ControlTaskBase


class PointCloud(ControlTaskBase):
    def setup(self):
        pass

    def default(self) -> None:
        self.sfr.set('point_cloud', None)

    def execute(self) -> None:
        depth_frame = self.sfr.get('disparity_frame')
        depth_data = self.sfr.get('disparity_data')

        depth_data = depth_data.reshape(depth_frame.shape)

        f = 441.25
        fx = f # / depth_frame.shape[1]
        fy = f # / depth_frame.shape[0]
        cloud = []
        cx = 200  #/depth_frame.shape[1]
        cy = 320  #/depth_frame.shape[0]
        for v in range(0,depth_frame.shape[0],8):
            for u in range(0,depth_frame.shape[1],8):
                x_c = (u - cx) * depth_data[v, u] / fx
                y_c = (v - cy) * depth_data[v, u] / fy
                cloud.append([x_c, y_c, depth_data[v, u]])

        self.sfr.set('point_cloud', cloud)
