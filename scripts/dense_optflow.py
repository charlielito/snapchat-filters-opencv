import cv2
import numpy as np

from video_loop import run_video_capture_pipeline, args

cap = cv2.VideoCapture(args.read_camera)
ret, frame1 = cap.read()
prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[..., 1] = 255
cap.release()


def dense_flow(image):
    global prvs
    next = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    hsv[..., 0] = ang * 180 / np.pi / 2
    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    prvs = next
    return image


run_video_capture_pipeline(transform_fn=dense_flow)
