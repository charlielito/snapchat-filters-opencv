#! /usr/bin/env python

import sys
import numpy as np
import cv2
from imutils import face_utils
import datetime
import imutils
import time
import dlib
from utils import applyAffineTransform, rectContains, calculateDelaunayTriangles, warpTriangle, face_swap3

if __name__ == '__main__' :

    # Make sure OpenCV is version 3.0 or above
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    if int(major_ver) < 3 :
        print >>sys.stderr, 'ERROR: Script needs OpenCV 3.0 or higher'
        sys.exit(1)

    print("[INFO] loading facial landmark predictor...")
    model = "shape_predictor_68_face_landmarks.dat"
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(model)

    video_capture = cv2.VideoCapture(0)
    ret, img = video_capture.read()
    cv2.imshow("Face Swapped", img)

    while (True):
        print "what"

        ret, img = video_capture.read()

        output = face_swap3(img, detector, predictor)
        if (output != None):
            cv2.imshow("Face Swapped", output)
        else:
            cv2.imshow("Face Swapped", img)
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
        	break

    cv2.destroyAllWindows()
    video_capture.release()
