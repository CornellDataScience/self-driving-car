import numpy as np
import cv2
import depthai as dai
import math
import g2o

from threading import Lock, Thread
from queue import Queue

from enum import Enum
from collections import defaultdict

from covisibility import GraphKeyFrame
from covisibility import GraphMapPoint
from covisibility import GraphMeasurement




class Camera(object):
    def __init__(self, fx, fy, cx, cy, width, height, 
            frustum_near, frustum_far, baseline=75):

        self.fx = fx
        self.fy = fy
        self.cx = cx
        self.cy = cy
        self.baseline = baseline

        self.intrinsic = np.array([
            [fx, 0, cx], 
            [0, fy, cy], 
            [0, 0, 1]])

        self.frustum_near = frustum_near
        self.frustum_far = frustum_far

        self.width = width
        self.height = height


        pipeline = dai.Pipeline()

        camLeft = pipeline.create(dai.node.MonoCamera)
        camRight = pipeline.create(dai.node.MonoCamera)
        stereo = pipeline.create(dai.node.StereoDepth)
        xoutLeft = pipeline.create(dai.node.XLinkOut)
        xoutRight = pipeline.create(dai.node.XLinkOut)
        xoutDisparity = pipeline.create(dai.node.XLinkOut)
        xoutDepth = pipeline.create(dai.node.XLinkOut)
        xoutRectifLeft = pipeline.create(dai.node.XLinkOut)
        xoutRectifRight = pipeline.create(dai.node.XLinkOut)

        camLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
        camRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)

        camLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_800_P)
        camRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_800_P)


        stereo.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
        stereo.initialConfig.setMedianFilter(dai.StereoDepthProperties.MedianFilter.KERNEL_7x7)  # KERNEL_7x7 default
        stereo.setRectifyEdgeFillColor(0)  # Black, to better see the cutout
        stereo.setLeftRightCheck(False)
        stereo.setExtendedDisparity(False)
        stereo.setSubpixel(False)

        xoutLeft.setStreamName("left")
        xoutRight.setStreamName("right")
        xoutDisparity.setStreamName("disparity")
        xoutDepth.setStreamName("depth")
        xoutRectifLeft.setStreamName("rectifiedLeft")
        xoutRectifRight.setStreamName("rectifiedRight")

        camLeft.out.link(stereo.left)
        camRight.out.link(stereo.right)
        stereo.syncedLeft.link(xoutLeft.input)
        stereo.syncedRight.link(xoutRight.input)
        stereo.disparity.link(xoutDisparity.input)
        if True:
            stereo.depth.link(xoutDepth.input)
        if True:
            stereo.rectifiedLeft.link(xoutRectifLeft.input)
            stereo.rectifiedRight.link(xoutRectifRight.input)

        streams = ["left", "right"]
        if True:
            streams.extend(["rectifiedLeft", "rectifiedRight"])
        streams.append("disparity")
        if True:
            streams.append("depth")



        baseline = 75
        fov = 71.86
        width = 1280
        focal = width/(2*math.tan(fov/2/180*math.pi))

        self.device = dai.Device(pipeline)

        #  cv2.imshow("left", self.left())
        #  cv2.imshow("right", self.right())

    def left(self):
       #  print("Called left...")
       q = self.device.getOutputQueue('left', 8, blocking=False) 
       data = q.get()
       frame = data.getCvFrame()
       return frame

    def right(self):
       q = self.device.getOutputQueue('right', 8, blocking=False) 
       data = q.get()
       frame = data.getCvFrame()
       return frame

    def get_pair(self):
        #  leftq = self.device.getOutputQueue("left", 8, blocking=False)
        #  rightq = self.device.getOutputQueue("right", 8, blocking=False)
        #  lframe = leftq.get().getCvFrame()
        #  rframe = rightq.get().getCvFrame()
        #  cv2.imshow("pair left", lframe)
        #  cv2.imshow("pair right", rframe)

       streams = ["left", "right", "depth"]
       qList = [self.device.getOutputQueue(stream, 8, blocking=False) for stream in streams]
       for _ in range(5):
           for q in qList:
               name = q.getName()
               frame = q.get().getCvFrame()
               if name == "depth":
                   frame = frame.astype(np.uint16)
               elif name == "disparity":
                   frame = getDisparityFrame(frame)

               cv2.imshow(name, frame)
           if cv2.waitKey(1) == ord("q"):
               break
       lframe = self.device.getOutputQueue("left", 8, blocking=False).get().getCvFrame()
       rframe = self.device.getOutputQueue("right", 8, blocking=False).get().getCvFrame()
       return lframe, rframe

    def loop_display(self):
       streams = ["left", "right", "depth"]
       qList = [self.device.getOutputQueue(stream, 8, blocking=False) for stream in streams]
       while True:
            for q in qList:
                name = q.getName()
                frame = q.get().getCvFrame()
                if name == "depth":
                    frame = frame.astype(np.uint16)
                elif name == "disparity":
                    frame = getDisparityFrame(frame)

                cv2.imshow(name, frame)
            if cv2.waitKey(1) == ord("q"):
                break

        # Uses g2o        
    #  def compute_right_camera_pose(self, pose):
        #  pos = pose * np.array([self.baseline, 0, 0])
        #  return g2o.Isometry3d(pose.orientation(), pos)



class Frame(object):
    def __init__(self, idx, pose, feature, cam, timestamp=None, 
            pose_covariance=np.identity(6)):
        self.idx = idx
        self.pose = pose    # g2o.Isometry3d
        self.feature = feature
        self.cam = cam
        self.timestamp = timestamp
        self.image = feature.image
        
        self.orientation = pose.orientation()
        self.position = pose.position()
        self.pose_covariance = pose_covariance

        print("inverse: ", pose.inverse().matrix())
        self.transform_matrix = pose.inverse().matrix()[:3] # shape: (3, 4)
        print("transform matrix: ", self.transform_matrix)
        self.projection_matrix =(self.cam.intrinsic.dot(self.transform_matrix))  # from world frame to image
        print("projection matrix: ", self.projection_matrix)

    # batch version
    def can_view(self, points, ground=False, margin=20):    # Frustum Culling
        points = np.transpose(points)
        #  print("view points transposed: ", points)
        (u, v), depth = self.project(self.transform(points))

        #  print("Depth: ", depth)
        #  print("u: ", u)
        #  print("v: ", v)

        if ground:
            return np.logical_and.reduce([
                depth >= self.cam.frustum_near,
                depth <= self.cam.frustum_far,
                u >= - margin,
                u <= self.cam.width + margin])
        else:
            return np.logical_and.reduce([
                depth >= self.cam.frustum_near,
                depth <= self.cam.frustum_far,
                u >= - margin,
                u <= self.cam.width + margin,
                v >= - margin,
                v <= self.cam.height + margin])

        
    def update_pose(self, pose):
        if isinstance(pose, g2o.SE3Quat):
            self.pose = g2o.Isometry3d(pose.orientation(), pose.position())
        else:
            self.pose = pose   
        self.orientation = self.pose.orientation()  
        self.position = self.pose.position()

        self.transform_matrix = self.pose.inverse().matrix()[:3]
        self.projection_matrix = (
            self.cam.intrinsic.dot(self.transform_matrix))

    def transform(self, points):    # from world coordinates
        '''
        Transform points from world coordinates frame to camera frame.
        Args:
            points: a point or an array of points, of shape (3,) or (3, N).
        '''
        print("transform points: ", points)
        R = self.transform_matrix[:3, :3]
        if points.ndim == 1:
            t = self.transform_matrix[:3, 3]
        else:
            t = self.transform_matrix[:3, 3:]
        #  print("R: ", R)
        #  print("R . points: ", R.dot(points))
        return R.dot(points) + t

    def project(self, points): 
        '''
        Project points from camera frame to image's pixel coordinates.
        Args:
            points: a point or an array of points, of shape (3,) or (3, N).
        Returns:
            Projected pixel coordinates, and respective depth.
        '''
        #  print("points in project: ", points)
        print("intrinsic: ", self.cam.intrinsic)
        projection = self.cam.intrinsic.dot(points / points[-1:])
        #  print("projection: ", projection)
        return projection[:2], points[-1]

    def find_matches(self, points, descriptors):
        '''
        Match to points from world frame.
        Args:
            points: a list/array of points. shape: (N, 3)
            descriptors: a list of feature descriptors. length: N
        Returns:
            List of successfully matched (queryIdx, trainIdx) pairs.
        '''
        points = np.transpose(points)
        proj, _ = self.project(self.transform(points))
        proj = proj.transpose()
        return self.feature.find_matches(proj, descriptors)

    def get_keypoint(self, i):
        return self.feature.get_keypoint(i)
    def get_descriptor(self, i):
        return self.feature.get_descriptor(i)
    def get_color(self, pt):
        return self.feature.get_color(pt)
    def set_matched(self, i):
        self.feature.set_matched(i)
    def get_unmatched_keypoints(self):
        return self.feature.get_unmatched_keypoints()



class StereoFrame(Frame):
    def __init__(self, idx, pose, feature, right_feature, cam, 
            right_cam=None, timestamp=None, pose_covariance=np.identity(6)):

        super().__init__(idx, pose, feature, cam, timestamp, pose_covariance)
        self.left  = Frame(idx, pose, feature, cam, timestamp, pose_covariance)
        self.right = Frame(idx, pose, right_feature, right_cam or cam, timestamp, pose_covariance)

    def find_matches(self, source, points, descriptors):
        
        q2 = Queue()
        def find_right(points, descriptors, q):
            m = dict(self.right.find_matches(points, descriptors))
            q.put(m)
        t2 = Thread(target=find_right, args=(points, descriptors, q2))
        t2.start()
        matches_left = dict(self.left.find_matches(points, descriptors))
        t2.join()
        matches_right = q2.get()

        measurements = []
        for i, j in matches_left.items():
            if i in matches_right:
                j2 = matches_right[i]

                y1 = self.left.get_keypoint(j).pt[1]
                y2 = self.right.get_keypoint(j2).pt[1]
                if abs(y1 - y2) > 2.5:    # epipolar constraint
                    continue   # TODO: choose one

                meas = Measurement(
                    Measurement.Type.STEREO,
                    source,
                    [self.left.get_keypoint(j), 
                        self.right.get_keypoint(j2)],
                    [self.left.get_descriptor(j),
                        self.right.get_descriptor(j2)])
                measurements.append((i, meas))
                self.left.set_matched(j)
                self.right.set_matched(j2)
            else:
                meas = Measurement(
                    Measurement.Type.LEFT,
                    source,
                    [self.left.get_keypoint(j)],
                    [self.left.get_descriptor(j)])
                measurements.append((i, meas))
                self.left.set_matched(j)

        for i, j in matches_right.items():
            if i not in matches_left:
                meas = Measurement(
                    Measurement.Type.RIGHT,
                    source,
                    [self.right.get_keypoint(j)],
                    [self.right.get_descriptor(j)])
                measurements.append((i, meas))
                self.right.set_matched(j)

        return measurements

    def match_mappoints(self, mappoints, source):
        points = []
        descriptors = []
        for mappoint in mappoints:
            points.append(mappoint.position)
            descriptors.append(mappoint.descriptor)
        matched_measurements = self.find_matches(source, points, descriptors)

        measurements = []
        for i, meas in matched_measurements:
            meas.mappoint = mappoints[i]
            measurements.append(meas)
        return measurements

    def triangulate(self):
        kps_left, desps_left, idx_left = self.left.get_unmatched_keypoints()
        kps_right, desps_right, idx_right = self.right.get_unmatched_keypoints()

        mappoints, matches = self.triangulate_points(
            kps_left, desps_left, kps_right, desps_right)

        measurements = []
        for mappoint, (i, j) in zip(mappoints, matches):
            meas = Measurement(
                Measurement.Type.STEREO,
                Measurement.Source.TRIANGULATION,
                [kps_left[i], kps_right[j]],
                [desps_left[i], desps_right[j]])
            meas.mappoint = mappoint
            #  meas.view = self.transform(mappoint.position) #Uses Pose, which is g2o isometry
            measurements.append(meas)

            self.left.set_matched(idx_left[i])
            self.right.set_matched(idx_right[j])

        return mappoints, measurements

    def triangulate_points(self, kps_left, desps_left, kps_right, desps_right):
        #  print("kps_left: ", kps_left)
        #  print("desps_left: ", desps_left)
        #  print("kps_right: ", kps_right)
        #  print("desps_right: ", desps_right)
        matches = self.feature.row_match(
            kps_left, desps_left, kps_right, desps_right)
        assert len(matches) > 0
        print("Row match completed")
        px_left = np.array([kps_left[m.queryIdx].pt for m in matches])
        px_right = np.array([kps_right[m.trainIdx].pt for m in matches])

        self.right.projection_matrix = np.array([[718., 0., 0., 1.],[0., 817., 0., 1.],[607., 185., 1., 1.]])
            
        print("px_left: ", px_left[:, :2].transpose())
        print("px_right: ", px_right[:, :2].transpose())
        print("left proj: ", self.left.projection_matrix)
        print("right proj: ", self.right.projection_matrix)

        points = cv2.triangulatePoints(
            self.left.projection_matrix, 
            self.right.projection_matrix, 
            px_left[:, :2].transpose(), 
            px_right[:, :2].transpose() 
            ).transpose()  # shape: (N, 4)

        print("points: ", points)

        points = points[:, :3] / points[:, 3:] # Not sure what this is doing
        #  print("normalized points: ", points)


        can_view = np.logical_and(
            self.left.can_view(points, ground=True), 
            self.right.can_view(points, ground=True))

        #  print("left can_view: ", self.right.can_view(points, ground=True))
        #  print("right can_view: ", self.left.can_view(points, ground=True))
        print("joint can_view: ", can_view)

        mappoints = []
        matchs = []
        for i, point in enumerate(points):
            #  if not can_view[i]:
                #  print("continuing...")
                #  continue
            #  print("Making Mappoint")
            normal = point - self.position
            normal = normal / np.linalg.norm(normal)

            color = self.left.get_color(px_left[i])
    
            
            mappoint = MapPoint(
                point, normal, desps_left[matches[i].queryIdx], color)
            mappoints.append(mappoint)
            matchs.append((matches[i].queryIdx, matches[i].trainIdx))

        print("# mappoints: ", len(mappoints))
        return mappoints, matchs

    def update_pose(self, pose):
        super().update_pose(pose)
        self.right.update_pose(pose)
        self.left.update_pose(
            self.cam.compute_right_camera_pose(pose))

    # batch version
    def can_view(self, mappoints):
        points = []
        point_normals = []
        for i, p in enumerate(mappoints):
            points.append(p.position)
            point_normals.append(p.normal)
        points = np.asarray(points)
        point_normals = np.asarray(point_normals)

        normals = points - self.position
        normals /= np.linalg.norm(normals, axis=-1, keepdims=True)
        cos = np.clip(np.sum(point_normals * normals, axis=1), -1, 1)
        parallel = np.arccos(cos) < (np.pi / 4)

        can_view = np.logical_or(
            self.left.can_view(points), 
            self.right.can_view(points))

        return np.logical_and(parallel, can_view)

    def to_keyframe(self):
        return KeyFrame(
            self.idx, self.pose, 
            self.left.feature, self.right.feature, 
            self.cam, self.right.cam, 
            self.pose_covariance)



class KeyFrame(StereoFrame):
    _id = 0
    _id_lock = Lock()

    def __init__(self, *args, **kwargs):
        GraphKeyFrame.__init__(self)
        StereoFrame.__init__(self, *args, **kwargs)

        with KeyFrame._id_lock:
            self.id = KeyFrame._id
            KeyFrame._id += 1

        self.reference_keyframe = None
        self.reference_constraint = None
        self.preceding_keyframe = None
        self.preceding_constraint = None
        self.loop_keyframe = None
        self.loop_constraint = None
        self.fixed = False

    def update_reference(self, reference=None):
        if reference is not None:
            self.reference_keyframe = reference
        self.reference_constraint = (
            self.reference_keyframe.pose.inverse() * self.pose)

    def update_preceding(self, preceding=None):
        if preceding is not None:
            self.preceding_keyframe = preceding
        self.preceding_constraint = (
            self.preceding_keyframe.pose.inverse() * self.pose)

    def set_loop(self, keyframe, constraint):
        self.loop_keyframe = keyframe
        self.loop_constraint = constraint

    def is_fixed(self):
        return self.fixed

    def set_fixed(self, fixed=True):
        self.fixed = fixed



class MapPoint(GraphMapPoint):
    _id = 0
    _id_lock = Lock()

    def __init__(self, position, normal, descriptor,
            color=np.zeros(3),
            covariance=np.identity(3) * 1e-4):
        super().__init__()

        with MapPoint._id_lock:
            self.id = MapPoint._id
            MapPoint._id += 1

        self.position = position
        self.normal = normal
        self.descriptor = descriptor
        self.covariance = covariance
        self.color = color
        self.owner = None

        self.count = defaultdict(int)

    def update_position(self, position):
        self.position = position
    def update_normal(self, normal):
        self.normal = normal
    def update_descriptor(self, descriptor):
        self.descriptor = descriptor
    def set_color(self, color):
        self.color = color

    def is_bad(self):
        with self._lock:
            status =  (
                self.count['meas'] == 0
                or (self.count['outlier'] > 20
                    and self.count['outlier'] > self.count['inlier'])
                or (self.count['proj'] > 20
                    and self.count['proj'] > self.count['meas'] * 10))
            return status

    def increase_outlier_count(self):
        with self._lock:
            self.count['outlier'] += 1
    def increase_inlier_count(self):
        with self._lock:
            self.count['inlier'] += 1
    def increase_projection_count(self):
        with self._lock:
            self.count['proj'] += 1
    def increase_measurement_count(self):
        with self._lock:
            self.count['meas'] += 1
#
#
#
class Measurement(GraphMeasurement):

    Source = Enum('Measurement.Source', ['TRIANGULATION', 'TRACKING', 'REFIND'])
    Type = Enum('Measurement.Type', ['STEREO', 'LEFT', 'RIGHT'])

    def __init__(self, type, source, keypoints, descriptors):
        super().__init__()

        self.type = type
        self.source = source
        self.keypoints = keypoints
        self.descriptors = descriptors
        self.view = None    # mappoint's position in current coordinates frame

        self.xy = np.array(self.keypoints[0].pt)
        if self.is_stereo():
            self.xyx = np.array([
                *keypoints[0].pt, keypoints[1].pt[0]])

        self.triangulation = (source == self.Source.TRIANGULATION)

    def get_descriptor(self, i=0):
        return self.descriptors[i]
    def get_keypoint(self, i=0):
        return self.keypoints[i]

    def get_descriptors(self):
        return self.descriptors
    def get_keypoints(self):
        return self.keypoints

    def is_stereo(self):
        return self.type == Measurement.Type.STEREO
    def is_left(self):
        return self.type == Measurement.Type.LEFT
    def is_right(self):
        return self.type == Measurement.Type.RIGHT

    def from_triangulation(self):
        return self.triangulation
    def from_tracking(self):
        return self.source == Measurement.Source.TRACKING
    def from_refind(self):
        return self.source == Measurement.Source.REFIND
