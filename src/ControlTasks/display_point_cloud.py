import sys
import OpenGL.GL as gl
import numpy as np
from .control_task_base import ControlTaskBase
sys.path.append('./pypangolin.cpython-310-darwin.so')
import pypangolin as pangolin


class DisplayPointCloud(ControlTaskBase):

    def setup(self):
        # Create display window
        pangolin.CreateWindowAndBind('PointCloud', 640, 480)
        gl.glEnable(gl.GL_DEPTH_TEST)  # TODO: figure out what this does

        # Initialize render state (space & view)
        # Define Projection and initial ModelView matrix
        scam = pangolin.OpenGlRenderState(
            pangolin.ProjectionMatrix(640, 480, 420, 420, 320, 240, 0.2, 100),
            pangolin.ModelViewLookAt(-2, 2, -2, 0, 0, 0, pangolin.AxisDirection.AxisY)
        )
        handler = pangolin.Handler3D(scam)

        # Create Interactive View in window
        dcam = pangolin.CreateDisplay()
        dcam.SetBounds(0.0, 1.0, 0.0, 1.0, 640.0/480.0)
        dcam.SetHandler(handler)
        dcam.Resize(pangolin.Viewport(0, 0, 640*2, 480*2))

        self.dcam = dcam
        self.scam = scam

    def default(self):
        pass

    def execute(self):

        points = self.sfr.get("point_cloud")
        points = np.array(points)[:100000]
        print(points.shape)
        print(points)
        # colors = np.zeros((len(points), 3))
        # Clear previous frame (I think (?))
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glClearColor(1.0, 1.0, 1.0, 1.0)
        self.dcam.Activate(self.scam)

        # Get point cloud from sfr, and construct colors
        # colors[:, 1] = 1 - points[:, 0] / 10.
        # colors[:, 2] = 1 - points[:, 1] / 10.
        # colors[:, 0] = 1 - points[:, 2] / 10.

        # Define point size and color space
        gl.glPointSize(2)
        gl.glColor3f(1.0, 0.0, 0.0)

        # Draw points
        pangolin.DrawPoints(points)  # , colors
        # Finish frame
        pangolin.FinishFrame()

