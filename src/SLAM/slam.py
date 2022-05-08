#!/usr/bin/env python
# -*- coding: utf-8 -*-

print("Hello World! --SLAM")

class Tracking(object):
    pass
    #TODO

class SLAM(object):
    def __init__(self, params):
        self.params = params

        self.tracker = Tracking(params)
        self.motion_model = MotionModel()
#
        self.graph = CovisibilityGraph()
        self.mapping = MappingThread(self.graph, params)
#
        self.loop_closing = LoopClosing(self, params)
        self.loop_correction = None
        
        self.status = None # defaultdict(bool)

    def stop(self):
        self.mapping.stop()
        if self.loop_closing is not None:
            self.loop_closing.stop()

    def initialize(self, frame):
        mappoints, measurements = frame.triangulate()
        print("Need ", self.params.init_min_points, " points to initialize")
        print("Found ", len(mappoints), " map points")
        assert len(mappoints) >= self.params.init_min_points, (
            'Not enough points to initialize map.')

        keyframe = frame.to_keyframe()
        keyframe.set_fixed(True)
        self.graph.add_keyframe(keyframe)
        self.mapping.add_measurements(keyframe, mappoints, measurements)
        #  if self.loop_closing is not None:
            #  self.loop_closing.add_keyframe(keyframe)

        self.reference = keyframe
        self.preceding = keyframe
        self.current = keyframe
        self.status['initialized'] = True

        #  self.motion_model.update_pose(
            #  frame.timestamp, frame.position, frame.orientation)
