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

    # Read images will swap image1 into image2
    filename1 = 'ted_cruz.jpg'
    filename1 = 'brad.jpg'
    #filename1 = 'hillary_clinton.jpg'

    img1 = cv2.imread(filename1);
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    # detect faces in the grayscale frame
    rects1 = detector(gray1, 0)
    shape1 = predictor(gray1, rects1[0])
    points1 = face_utils.shape_to_np(shape1) #type is a array of arrays (list of lists)
    #need to convert to a list of tuples
    points1 = list(map(tuple, points1))

    video_capture = cv2.VideoCapture(0)

    while (True):
        print "what"

        ret, img2 = video_capture.read()
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        # detect faces in the grayscale frame
        rects2 = detector(gray2, 0)
        if (len(rects2) != 0 ):
            img1Warped = np.copy(img2);
            shape2 = predictor(gray2, rects2[0])
            points2 = face_utils.shape_to_np(shape2)
            points2 = list(map(tuple, points2))

            # Find convex hull
            hull1 = []
            hull2 = []

            hullIndex = cv2.convexHull(np.array(points2), returnPoints = False)

            for i in xrange(0, len(hullIndex)):
                hull1.append(points1[ int(hullIndex[i]) ])
                hull2.append(points2[ int(hullIndex[i]) ])


            # Find delanauy traingulation for convex hull points
            sizeImg2 = img2.shape
            rect = (0, 0, sizeImg2[1], sizeImg2[0])

            dt = calculateDelaunayTriangles(rect, hull2)

            if len(dt) == 0:
                continue

            # Apply affine transformation to Delaunay triangles
            for i in xrange(0, len(dt)):
                t1 = []
                t2 = []

                #get points for img1, img2 corresponding to the triangles
                for j in xrange(0, 3):
                    t1.append(hull1[dt[i][j]])
                    t2.append(hull2[dt[i][j]])

                warpTriangle(img1, img1Warped, t1, t2)


            # Calculate Mask
            hull8U = []
            for i in xrange(0, len(hull2)):
                hull8U.append((hull2[i][0], hull2[i][1]))

            mask = np.zeros(img2.shape, dtype = img2.dtype)

            cv2.fillConvexPoly(mask, np.int32(hull8U), (255, 255, 255))

            r = cv2.boundingRect(np.float32([hull2]))

            center = ((r[0]+int(r[2]/2), r[1]+int(r[3]/2)))

            # Clone seamlessly.
            output = cv2.seamlessClone(np.uint8(img1Warped), img2, mask, center, cv2.NORMAL_CLONE)

            cv2.imshow("Face Swapped", output)
            print "done"
            key = cv2.waitKey(1) & 0xFF
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
            	break

    cv2.destroyAllWindows()
    video_capture.release()
