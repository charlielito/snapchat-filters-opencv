import argparse
import time

import cv2
import numpy as np
from concurrent_videocapture import ConcurrentVideoCapture
from python_path import PythonPath

with PythonPath("."):
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
parser.add_argument(
    "--verbose",
    type=bool,
    default=False,
    help="Verbose printing of current FPS of pipeline",
)
args = parser.parse_args()


def get_snap_shot():
    cap = cv2.VideoCapture(args.read_camera)
    snap = None

    # Capture initial video
    while True:
        grabbed, frame = cap.read()
        if not grabbed:
            break
        show = frame.copy()
        cv2.putText(
            show,
            "Press S to take snapshot",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (209, 80, 0),
            3,
        )

        cv2.imshow("original", show)

        key = cv2.waitKey(1)
        if key == 27:  # ESC
            break
        elif key == ord("s"):
            snap = frame.copy()
            break
    cap.release()
    cv2.destroyAllWindows()
    return snap


def run_video_capture_pipeline(
    transform_fn=None, verbose=args.verbose, concurrent_videocapture=True
):

    capture = ConcurrentVideoCapture if concurrent_videocapture else cv2.VideoCapture
    video_capture = capture(args.read_camera)
    stream_camera = None

    while True:
        init = time.time()

        ret, image = video_capture.read()
        if not ret:
            print("Error reading camera, exiting")
            break

        ######## Whatever processing of the image
        image = transform_fn(image) if transform_fn is not None else image
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


if __name__ == "__main__":
    run_video_capture_pipeline()
