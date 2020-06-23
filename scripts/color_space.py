
import cv2

from video_loop import run_video_capture_pipeline


def color(image):
    # kernel_size = 5
    # image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return image


run_video_capture_pipeline(transform_fn=color)
