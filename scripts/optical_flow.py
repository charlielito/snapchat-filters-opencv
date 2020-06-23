import argparse
import time

import cv2
import numpy as np
from concurrent_videocapture import ConcurrentVideoCapture
from python_path import PythonPath

with PythonPath("."):
    import pyfakewebcam


parser = argparse.ArgumentParser()
parser.add_argument("--read_camera", type=int, default=0, help="Id to read camera from")
parser.add_argument(
    "--virtual_camera",
    type=int,
    default=0,
    help="If different from 0, creates a virtual camera with results on that id (linux only)",
)
args = parser.parse_args()

video_capture = ConcurrentVideoCapture(args.read_camera)
stream_camera = None
verbose = True

# params for ShiTomasi corner detection
feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)

# Parameters for lucas kanade optical flow
lk_params = dict(
    winSize=(15, 15),
    maxLevel=2,
    criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),
)

# Create some random colors
color = np.random.randint(0, 255, (100, 3))

# Take first frame and find corners in it
ret, old_frame = video_capture.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)
reset = False

while True:
    init = time.time()

    ret, image = video_capture.read()
    if not ret:
        print("Error reading camera, exiting")
        break

    ######## Whatever processing of the image
    frame_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    # Select good points
    good_new = p1[st == 1]
    good_old = p0[st == 1]

    # draw the tracks
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new.ravel()
        c, d = old.ravel()
        mask = cv2.line(mask, (a, b), (c, d), color[i].tolist(), 2)
        image = cv2.circle(image, (a, b), 5, color[i].tolist(), -1)
    image = cv2.add(image, mask)

    # Now update the previous frame and previous points
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1, 1, 2)

    if reset:
        p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)
        mask = np.zeros_like(old_frame)
        reset = False
    #########################################

    if stream_camera is None:
        if args.virtual_camera:
            h, w = image.shape[:2]
            stream_camera = pyfakewebcam.FakeWebcam(
                "/dev/video{}".format(args.virtual_camera), w, h
            )

    cv2.imshow("video", image)
    key = cv2.waitKey(1)
    if key == 27:  # ESC
        break
    # Reset features
    if key == ord("r"):
        reset = True

    if args.virtual_camera:
        stream_camera.schedule_frame(image[..., ::-1])

    fps = 1 / (time.time() - init)
    if verbose:
        print("Fps: {}".format(fps))

video_capture.release()
cv2.destroyAllWindows()
