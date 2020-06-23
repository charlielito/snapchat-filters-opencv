import cv2
import numpy as np
from concurrent_videocapture import ConcurrentVideoCapture

import dlib
from imutils import face_utils
from video_loop import run_video_capture_pipeline


# Taken from https://www.pyimagesearch.com/2020/04/06/blur-and-anonymize-faces-with-opencv-and-python/
def anonymize_face_pixelate(image, blocks=3):
    # divide the input image into NxN blocks
    (h, w) = image.shape[:2]
    xSteps = np.linspace(0, w, blocks + 1, dtype="int")
    ySteps = np.linspace(0, h, blocks + 1, dtype="int")
    # loop over the blocks in both the x and y direction
    for i in range(1, len(ySteps)):
        for j in range(1, len(xSteps)):
            # compute the starting and ending (x, y)-coordinates
            # for the current block
            startX = xSteps[j - 1]
            startY = ySteps[i - 1]
            endX = xSteps[j]
            endY = ySteps[i]
            # extract the ROI using NumPy array slicing, compute the
            # mean of the ROI, and then draw a rectangle with the
            # mean RGB values over the ROI in the original image
            roi = image[startY:endY, startX:endX]
            (B, G, R) = [int(x) for x in cv2.mean(roi)[:3]]
            cv2.rectangle(image, (startX, startY), (endX, endY), (B, G, R), -1)
    # return the pixelated blurred image
    return image


# Filters path
detector = dlib.get_frontal_face_detector()

# Facial landmarks
print("[INFO] loading facial landmark predictor...")
model = "filters/shape_predictor_68_face_landmarks.dat"
predictor = dlib.shape_predictor(
    model
)  # link to model: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2


def blur(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray, 0)

    mask = np.zeros(image.shape[:2], np.uint8)
    blurred_image = image.copy()
    for face in faces:  # if there are faces
        (x, y, w, h) = (face.left(), face.top(), face.width(), face.height())
        blurred_image[y : y + h, x : x + w, :] = anonymize_face_pixelate(
            blurred_image[y : y + h, x : x + w, :], blocks=10
        )
        # *** Facial Landmarks detection
        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)
        # Get mask with only face shape
        shape = cv2.convexHull(shape)
        cv2.drawContours(mask, [shape], -1, 255, -1)

        # Replace blurred image only in mask
        mask = mask / 255.0
        mask = np.expand_dims(mask, axis=-1)
        image = (1.0 - mask) * image + mask * blurred_image
        image = image.astype(np.uint8)

    return image


run_video_capture_pipeline(transform_fn=blur)
