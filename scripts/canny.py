import cv2

from video_loop import run_video_capture_pipeline


def canny(image):
    edges = cv2.Canny(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 50, 150)
    # Transform again to BGR
    image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    return image


run_video_capture_pipeline(transform_fn=canny)
