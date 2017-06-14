#! /usr/bin/env python

import sys
import numpy as np
import cv2
from imutils import face_utils
import datetime
import imutils
import time
import dlib
from utils import applyAffineTransform, rectContains, calculateDelaunayTriangles, warpTriangle

#put face in img_ref into face of img_mount_face
def face_swap(img_ref, img_mount_face, detector, predictor):

    gray2 = cv2.cvtColor(img_mount_face, cv2.COLOR_BGR2GRAY)
    # detect faces in the grayscale frame
    rects2 = detector(gray2, 0)


    gray1 = cv2.cvtColor(img_ref, cv2.COLOR_BGR2GRAY)
    # detect faces in the grayscale frame
    rects1 = detector(gray1, 0)
    print len(rects2)
    if (len(rects2) == 0 or len(rects1) == 0): #if not found faces in images return error
        return None

    img1Warped = np.copy(img_mount_face);

    shape1 = predictor(gray1, rects1[0])
    points1 = face_utils.shape_to_np(shape1) #type is a array of arrays (list of lists)
    #need to convert to a list of tuples
    points1 = list(map(tuple, points1))
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
    sizeImg2 = img_mount_face.shape
    rect = (0, 0, sizeImg2[1], sizeImg2[0])

    dt = calculateDelaunayTriangles(rect, hull2)

    if len(dt) == 0:
        return None

    # Apply affine transformation to Delaunay triangles
    for i in xrange(0, len(dt)):
        t1 = []
        t2 = []

        #get points for img1, img2 corresponding to the triangles
        for j in xrange(0, 3):
            t1.append(hull1[dt[i][j]])
            t2.append(hull2[dt[i][j]])

        warpTriangle(img_ref, img1Warped, t1, t2)


    # Calculate Mask
    hull8U = []
    for i in xrange(0, len(hull2)):
        hull8U.append((hull2[i][0], hull2[i][1]))

    mask = np.zeros(img_mount_face.shape, dtype = img_mount_face.dtype)

    cv2.fillConvexPoly(mask, np.int32(hull8U), (255, 255, 255))

    r = cv2.boundingRect(np.float32([hull2]))

    center = ((r[0]+int(r[2]/2), r[1]+int(r[3]/2)))


    # Clone seamlessly.
    output = cv2.seamlessClone(np.uint8(img1Warped), img_mount_face, mask, center, cv2.NORMAL_CLONE)

    return output

#swaps faces in img_ref and img_mount_face (two separate files)
def face_swap2(img_ref, img_mount_face, detector, predictor):

    gray2 = cv2.cvtColor(img_mount_face, cv2.COLOR_BGR2GRAY)
    # detect faces in the grayscale frame
    rects2 = detector(gray2, 0)


    gray1 = cv2.cvtColor(img_ref, cv2.COLOR_BGR2GRAY)
    # detect faces in the grayscale frame
    rects1 = detector(gray1, 0)
    print len(rects2)
    if (len(rects2) == 0 or len(rects1) == 0): #if not found faces in images return error
        return None

    img1Warped = np.copy(img_mount_face);
    img2Warped = np.copy(img_ref);

    shape1 = predictor(gray1, rects1[0])
    points1 = face_utils.shape_to_np(shape1) #type is a array of arrays (list of lists)
    #need to convert to a list of tuples
    points1 = list(map(tuple, points1))
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
    sizeImg2 = img_mount_face.shape
    rect = (0, 0, sizeImg2[1], sizeImg2[0])

    dt = calculateDelaunayTriangles(rect, hull2)

    if len(dt) == 0:
        return None

    # Apply affine transformation to Delaunay triangles
    for i in xrange(0, len(dt)):
        t1 = []
        t2 = []

        #get points for img1, img2 corresponding to the triangles
        for j in xrange(0, 3):
            t1.append(hull1[dt[i][j]])
            t2.append(hull2[dt[i][j]])

        warpTriangle(img_ref, img1Warped, t1, t2)

    # Calculate Mask
    hull8U = []
    for i in xrange(0, len(hull2)):
        hull8U.append((hull2[i][0], hull2[i][1]))

    mask = np.zeros(img_mount_face.shape, dtype = img_mount_face.dtype)

    cv2.fillConvexPoly(mask, np.int32(hull8U), (255, 255, 255))

    r = cv2.boundingRect(np.float32([hull2]))

    center = ((r[0]+int(r[2]/2), r[1]+int(r[3]/2)))


    # Clone seamlessly.
    output = cv2.seamlessClone(np.uint8(img1Warped), img_mount_face, mask, center, cv2.NORMAL_CLONE)


    # Find delanauy traingulation for convex hull points
    sizeImg1 = img_ref.shape
    rect = (0, 0, sizeImg1[1], sizeImg1[0])
    dt = calculateDelaunayTriangles(rect, hull1)

    if len(dt) == 0:
        return None

    # Apply affine transformation to Delaunay triangles
    for i in xrange(0, len(dt)):
        t1 = []
        t2 = []

        #get points for img1, img2 corresponding to the triangles
        for j in xrange(0, 3):
            t1.append(hull2[dt[i][j]])
            t2.append(hull1[dt[i][j]])

        warpTriangle(img_mount_face, img2Warped, t1, t2)

    # Calculate Mask
    hull8U = []
    for i in xrange(0, len(hull1)):
        hull8U.append((hull1[i][0], hull1[i][1]))

    mask = np.zeros(img_ref.shape, dtype = img_ref.dtype)

    cv2.fillConvexPoly(mask, np.int32(hull8U), (255, 255, 255))

    r = cv2.boundingRect(np.float32([hull1]))

    center = ((r[0]+int(r[2]/2), r[1]+int(r[3]/2)))

    # Clone seamlessly.
    output2 = cv2.seamlessClone(np.uint8(img2Warped), img_ref, mask, center, cv2.NORMAL_CLONE)

    return output, output2

# swaps 2 faces in a image
def face_swap3(img_ref, detector, predictor):

    gray1 = cv2.cvtColor(img_ref, cv2.COLOR_BGR2GRAY)
    # detect faces in the grayscale frame
    rects1 = detector(gray1, 0)

    if (len(rects1) < 2): #at least 2 faces in image need to be found
        return None

    img1Warped = np.copy(img_ref);

    shape1 = predictor(gray1, rects1[0])
    points1 = face_utils.shape_to_np(shape1) #type is a array of arrays (list of lists)
    #need to convert to a list of tuples
    points1 = list(map(tuple, points1))

    shape2 = predictor(gray1, rects1[1])
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
    sizeImg2 = img_ref.shape
    rect = (0, 0, sizeImg2[1], sizeImg2[0])

    dt = calculateDelaunayTriangles(rect, hull2)

    if len(dt) == 0:
        return None

    # Apply affine transformation to Delaunay triangles
    for i in xrange(0, len(dt)):
        t1 = []
        t2 = []

        #get points for img1, img2 corresponding to the triangles
        for j in xrange(0, 3):
            t1.append(hull1[dt[i][j]])
            t2.append(hull2[dt[i][j]])

        warpTriangle(img_ref, img1Warped, t1, t2)


    # Calculate Mask
    hull8U = []
    for i in xrange(0, len(hull2)):
        hull8U.append((hull2[i][0], hull2[i][1]))

    mask = np.zeros(img_ref.shape, dtype = img_ref.dtype)

    cv2.fillConvexPoly(mask, np.int32(hull8U), (255, 255, 255))

    r = cv2.boundingRect(np.float32([hull2]))

    center = ((r[0]+int(r[2]/2), r[1]+int(r[3]/2)))


    # Clone seamlessly.
    output = cv2.seamlessClone(np.uint8(img1Warped), img_ref, mask, center, cv2.NORMAL_CLONE)


    img1Warped = np.copy(img_ref);
    dt = calculateDelaunayTriangles(rect, hull1)

    if len(dt) == 0:
        return None

    # Apply affine transformation to Delaunay triangles
    for i in xrange(0, len(dt)):
        t1 = []
        t2 = []

        #get points for img1, img2 corresponding to the triangles
        for j in xrange(0, 3):
            t1.append(hull2[dt[i][j]])
            t2.append(hull1[dt[i][j]])

        warpTriangle(img_ref, img1Warped, t1, t2)


    # Calculate Mask
    hull8U = []
    for i in xrange(0, len(hull2)):
        hull8U.append((hull1[i][0], hull1[i][1]))

    mask = np.zeros(img_ref.shape, dtype = img_ref.dtype)

    cv2.fillConvexPoly(mask, np.int32(hull8U), (255, 255, 255))

    r = cv2.boundingRect(np.float32([hull1]))

    center = ((r[0]+int(r[2]/2), r[1]+int(r[3]/2)))

    # Clone seamlessly.
    output = cv2.seamlessClone(np.uint8(img1Warped), output, mask, center, cv2.NORMAL_CLONE)

    return output

if __name__ == '__main__' :

    # Make sure OpenCV is version 3.0 or above
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    if int(major_ver) < 3 :
        print >>sys.stderr, 'ERROR: Script needs OpenCV 3.0 or higher'
        sys.exit(1)

    # Read images will swap image1 into image2
    filename1 = 'ted_cruz.jpg'
    #filename1 = 'donald_trump.jpg'
    filename1 = 'hillary_clinton.jpg'

    img1 = cv2.imread(filename1);
    #img2 = cv2.imread(filename2);


    print("[INFO] loading facial landmark predictor...")
    model = "shape_predictor_68_face_landmarks.dat"
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(model)


    video_capture = cv2.VideoCapture(0)

    while (True):

        ret, img2 = video_capture.read()
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        # detect faces in the grayscale frame
        rects2 = detector(gray2, 0)
        if (len(rects2) != 0 ):
            break

    img2 = cv2.imread('brad.jpg');
    img1 = cv2.imread('angelina.jpg');
    output, output2 = face_swap2(img2,img1, detector, predictor)
    img2 = cv2.imread('pitts.jpg');
    output = face_swap3(img2, detector, predictor)

    cv2.imshow("Face Swapped", output)
    cv2.waitKey(0)
    cv2.imshow("Face Swapped", output2)
    cv2.waitKey(0)

    cv2.destroyAllWindows()
    video_capture.release()
