# break up into smaller control tasks as needed
# from ..vision.process_frame_util import process_frame
from .control_task_base import ControlTaskBase

import numpy as np
import cv2
import math
import time

def get_features(frame):

    orb = cv2.ORB_create()

    # Replacement for orb.detect(frame, None) Gives many more points
    pts = cv2.goodFeaturesToTrack(np.mean(frame, axis=2).astype(np.uint8), 1000, qualityLevel=0.01, minDistance=7)

    # print("pts: ", alt_pts)

    kps = [cv2.KeyPoint(x=f[0][0], y=f[0][1], size=20) for f in pts]
    kps, des = orb.compute(frame, kps)

    # print("kps: ", kps)

    # return np.array([(kp.pt[0], kp.pt[1]) for kp in kps]), des
    return kps, des


# def get_features2(frame):

#     orb = cv2.ORB_create()


def match_frames(des1, des2):
    # print(des1, des2)
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    # matches = matcher.knnMatch(des1, des2, k=1)
    matches = matcher.match(des1, des2)

    # print(matches)
    matches = [m for m in matches if m.distance <= 24]  # Previous Default: 32
    matches = sorted(matches, key=lambda x: x.distance)
    return matches


def process_frame(frame, prev_frame):
    # orb = cv2.ORB_create()
    start_time = time.time()
    prev_kps, prev_des = get_features(prev_frame)
    kps, des = get_features(frame)
    feature_time = time.time()
    print("Getting features: ", feature_time-start_time)
    # print(kps)

    cv2.drawKeypoints(frame, kps, frame, color=(0, 255, 0), flags=0)
    draw_points_time = time.time()
    print("Drawing Points: ", draw_points_time-feature_time)
    # for p in kps:
    #     cv2.circle(frame, (int(p[0]), int(p[1])), color=(0, 255, 0), radius=3)

    matches = match_frames(prev_des, des)
    match_time = time.time()
    print("Matching Time: ", match_time-draw_points_time)
    # if matches:
    #     print("", len(matches), " matches found")
    #     frame = cv2.drawMatches(frame, kps, prev_frame, prev_kps, matches[:10], None, 2, flags=2)

    transitory_vec = 0
    stationary_left_vec = 0
    left_count = 0
    stationary_right_vec = 0
    right_count = 0

    for m in matches:
        idx1 = kps[m.trainIdx]
        idx2 = prev_kps[m.queryIdx]

        pt1 = (int(idx1.pt[0]), int(idx1.pt[1]))
        pt2 = (int(idx2.pt[0]), int(idx2.pt[1]))

        x1 = pt1[0]
        x2 = pt2[0]

        transitory_vec += x2 - x1
        if x2 > frame.shape[1]/2:
            stationary_right_vec += x2-x1
            right_count += 1
        else:
            stationary_left_vec += x2-x1
            left_count += 1

        if math.hypot(pt1[0]-pt2[0], pt1[1]-pt2[1]) <= 100:
            cv2.line(frame, pt1, pt2, (int(255*(1-m.distance/32)), 0, 0), 2)

    vect = str((stationary_left_vec, stationary_right_vec))
    adj_vect = str((round(stationary_left_vec/max(1, left_count), 2), round(stationary_right_vec/max(1, right_count), 2)))
    phrase = "Vectors: " + vect + "Adjusted: " + adj_vect + "Count: " + str((left_count, right_count)) + "=" + str(left_count+right_count)

    # TODO: Possible improvements to direction estimation
    # - Check ratio of matches between left and right
    #   (if turning left, there will be more matches on the right)
    # - Use previous (1 or more) estimation data as well
    #   (if turning left more likely to be turning left)
    # - Look at up/down movement for better differentiating FORWARD/BACKWARD
    # - Give different weightings to vectors depending on match distance
    # - If average pixel difference is increasing then FORWARD
    #   If decreasing then BACKWARD (change in pixel distance increases/decreases)

    if stationary_left_vec < 0 and stationary_right_vec > 0:
        phrase = "FORWARD  " + phrase
    elif stationary_left_vec > 0 and stationary_right_vec < 0:
        phrase = "BACKWARD " + phrase
    elif stationary_left_vec < 0 and stationary_right_vec < 0:
        phrase = "RIGHT    " + phrase
    elif stationary_left_vec > 0 and stationary_right_vec > 0:
        phrase = "LEFT    " + phrase

    # print(phrase)
    sf = 2
    loc = (10*sf, 20*sf)
    frame = cv2.putText(frame, phrase, loc, cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

    end_time = time.time()
    print("Drawing remaining features time: ", end_time-match_time)

    return frame


class ProcessFrame(ControlTaskBase):    
    def setup(self):
        pass
     
    def default(self):
        curr_frame = self.sfr.get('curr_frame')
        self.sfr.set('processed_frame', curr_frame)

    def execute(self):
        prev_frame = self.sfr.get('prev_frame')
        curr_frame = self.sfr.get('curr_frame')
        self.sfr.set('processed_frame', process_frame(prev_frame, curr_frame))
