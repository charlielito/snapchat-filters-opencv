import argparse
import time

import cv2
import numpy as np
import pyfakewebcam
from concurrent_videocapture import ConcurrentVideoCapture


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

ret, frame1 = video_capture.read()
prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[..., 1] = 255

while True:
    init = time.time()

    ret, image = video_capture.read()
    if not ret:
        print("Error reading camera, exiting")
        break

    ######## Whatever processing of the image
    next = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    hsv[..., 0] = ang * 180 / np.pi / 2
    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    prvs = next
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

    if args.virtual_camera:
        stream_camera.schedule_frame(image[..., ::-1])

    fps = 1 / (time.time() - init)
    if verbose:
        print("Fps: {}".format(fps))

video_capture.release()
cv2.destroyAllWindows()
