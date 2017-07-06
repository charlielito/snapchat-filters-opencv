import cv2
import sys
import numpy as np

def apply_Haar_filter(img, haar_cascade,scaleFact = 1.1, minNeigh = 5, minSizeW = 30):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    features = haar_cascade.detectMultiScale(
        gray,
        scaleFactor=scaleFact,
        minNeighbors=minNeigh,
        minSize=(minSizeW, minSizeW),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    return features


BLUE = (255,0,0)
GREEN = (0,255,0)
RED = (0,0,255)
YELL = (0,255,255)

#Filters path
haar_faces = cv2.CascadeClassifier('./filters/haarcascade_frontalface_default.xml')
haar_eyes = cv2.CascadeClassifier('./filters/haarcascade_eye.xml')
haar_mouth = cv2.CascadeClassifier('./filters/Mouth.xml')
haar_nose = cv2.CascadeClassifier('./filters/Nose.xml')


#config WebCam
video_capture = cv2.VideoCapture(0)
cv2.imshow('Video', np.empty((5,5),dtype=float))


while cv2.getWindowProperty('Video', 0) >= 0:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    #frame = cv2.imread('faceswap/lol2.jpg')

    faces = apply_Haar_filter(frame, haar_faces, 1.3 , 5, 30)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), BLUE, 2) #blue

        sub_img = frame[y:y+h,x:x+w,:]
        eyes = apply_Haar_filter(sub_img, haar_eyes, 1.3 , 10, 10)
        for (x2, y2, w2, h2) in eyes:
            cv2.rectangle(frame, (x+x2, y+y2), (x + x2+w2, y + y2+h2), YELL, 2)

        nose = apply_Haar_filter(sub_img, haar_nose, 1.3 , 8, 10)
        for (x2, y2, w2, h2) in nose:
            cv2.rectangle(frame, (x+x2, y+y2), (x + x2+w2, y + y2+h2), RED, 2) #red

        sub_img2 = frame[y + h/2:y+h,x:x+w,:] #only analize half of face for mouth
        mouth = apply_Haar_filter(sub_img2, haar_mouth, 1.3 , 10, 10)
        for (x2, y2, w2, h2) in mouth:
            cv2.rectangle(frame, (x+x2, y+h/2+y2), (x + x2+w2, y+h/2+y2+h2), GREEN, 2) #green
        #cv2.imshow('Face', sub_img)
        #cv2.imshow('Face/2', sub_img2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
    	break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
