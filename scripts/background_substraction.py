import argparse
import time

import cv2
import numpy as np
import pyfakewebcam

# Parser
parser = argparse.ArgumentParser()
parser.add_argument("--read_camera", type=int, default=0, help="Id to read camera from")
parser.add_argument(
    "--virtual_camera",
    type=int,
    default=0,
    help="If different from 0, creates a virtual camera with results on that id (linux only)",
)
args = parser.parse_args()

video_capture = cv2.VideoCapture(args.read_camera)
stream_camera = None


kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
fgbg = cv2.createBackgroundSubtractorMOG2()


while True:
    init = time.time()

    ret, image = video_capture.read()
    if not ret:
        print("Error reading camera, exiting")
        break

    ######## Whatever processing of the image
    image = fgbg.apply(image)
    image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    # Transform again to BGR
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
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
    print("Fps: {}".format(fps))

video_capture.release()
cv2.destroyAllWindows()
