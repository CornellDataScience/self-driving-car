#!/usr/bin/env python3

import cv2
import process_frame
# from IPython.display import display


class GetFeed():
    W, H = 1280, 720
    # disp = display(W, H)

    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)

    print("Initiated")

    if vc.isOpened():
        # try to get the first frame
        rval, frame = vc.read()
        prev_frame = None
    else:
        rval = False

    while rval:
        prev_frame = frame
        rval, frame = vc.read()
        frame = process_frame.display_frame(frame, prev_frame)
        cv2.imshow("preview", frame)
        # print(features)
        key = cv2.waitKey(20)
        if key == 27:
            # exit on ESC
            break

    cv2.destroyWindow("preview")
    vc.release()
