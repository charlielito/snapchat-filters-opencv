from imutils import face_utils
import datetime
import imutils
import time
import dlib
import cv2
import numpy as np


# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
model = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(model) # link to model: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2

video_capture = cv2.VideoCapture(0)
cv2.imshow('Video', np.empty((5,5),dtype=float))

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
