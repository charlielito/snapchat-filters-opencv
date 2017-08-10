from imutils import face_utils
import datetime
import imutils
import time
import dlib
import cv2, math
import numpy as np
from imutils import face_utils, rotate_bound


# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
model = "filters/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(model) # link to model: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2

video_capture = cv2.VideoCapture(0)
cv2.imshow('Video', np.empty((5,5),dtype=float))

#points are tuples in the form (x,y)
# returns angle between points in degrees
def calculate_inclination(point1, point2):
    x1,x2,y1,y2 = point1[0], point2[0], point1[1], point2[1]
    incl = -180/math.pi*math.atan((float(y2-y1))/(x2-x1))
    return incl

def calculate_boundbox(list_coordinates):
    x = min(list_coordinates[:,0])
    y = min(list_coordinates[:,1])
    w = max(list_coordinates[:,0]) - x
    h = max(list_coordinates[:,1]) - y
    return (x,y,w,h)

def get_face_boundbox(points, face_part):
    if face_part == 1:
        (x,y,w,h) = calculate_boundbox(points[17:22]) #left eyebrow
    elif face_part == 2:
        (x,y,w,h) = calculate_boundbox(points[22:27]) #right eyebrow
    elif face_part == 3:
        (x,y,w,h) = calculate_boundbox(points[36:42]) #left eye
    elif face_part == 4:
        (x,y,w,h) = calculate_boundbox(points[42:48]) #right eye
    elif face_part == 5:
        (x,y,w,h) = calculate_boundbox(points[29:36]) #nose
    elif face_part == 6:
        (x,y,w,h) = calculate_boundbox(points[48:68]) #mouth
    return (x,y,w,h)

while cv2.getWindowProperty('Video', 0) >= 0:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # detect faces in the grayscale frame
    rects = detector(gray, 0)

    # loop over the face detections
    for rect in rects:
    	# determine the facial landmarks for the face region, then
    	# convert the facial landmark (x, y)-coordinates to a NumPy array
        shape = predictor(gray, rect)

    	shape = face_utils.shape_to_np(shape)

        for i in range(1,7):
            (x,y,w,h) = get_face_boundbox(shape, i)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 1)

        incl = calculate_inclination(shape[17], shape[26])

        img = cv2.imread("./sprites/doggy_ears.png")
        rows,cols = img.shape[0], img.shape[1]
        M = cv2.getRotationMatrix2D((cols/2,rows/2),incl,1)
        dst = cv2.warpAffine(img,M,(cols,rows))
        dst = rotate_bound(img, incl)
        cv2.imshow('sprite',dst)

        print "Pixels distance points in mouth: ", shape[66][1] - shape[62][1]

        x,y, w, h = rect.left(), rect.top(), rect.width(), rect.height()

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

        # loop over the (x, y)-coordinates for the facial landmarks
    	# and draw them on the image
        for (x, y) in shape:
            cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
    	break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
