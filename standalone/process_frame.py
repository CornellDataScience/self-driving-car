import numpy as np
import cv2
import math


def get_features(frame):

    orb = cv2.ORB_create()

    # Replacement for orb.detect(frame, None) Gives many more points
    pts = cv2.goodFeaturesToTrack(np.mean(frame, axis=2).astype(np.uint8), 3000, qualityLevel=0.01, minDistance=7)

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
    matches = [m for m in matches if m.distance <= 32]
    matches = sorted(matches, key=lambda x: x.distance)
    return matches


def display_frame(frame, prev_frame):
    # orb = cv2.ORB_create()
    prev_kps, prev_des = get_features(prev_frame)
    kps, des = get_features(frame)
    # print(kps)

    cv2.drawKeypoints(frame, kps, frame, color=(0, 255, 0), flags=0)
    # for p in kps:
    #     cv2.circle(frame, (int(p[0]), int(p[1])), color=(0, 255, 0), radius=3)

    matches = match_frames(prev_des, des)
    # if matches:
    #     print("", len(matches), " matches found")
    #     frame = cv2.drawMatches(frame, kps, prev_frame, prev_kps, matches[:10], None, 2, flags=2)

    for m in matches:
        idx1 = kps[m.trainIdx]
        idx2 = prev_kps[m.queryIdx]

        pt1 = (int(idx1.pt[0]), int(idx1.pt[1]))
        pt2 = (int(idx2.pt[0]), int(idx2.pt[1]))
        if math.hypot(pt1[0]-pt2[0], pt1[1]-pt2[1]) <= 100:
            cv2.line(frame, pt1, pt2, (int(255*(1-m.distance/32)), 0, 0), 2)

    return frame