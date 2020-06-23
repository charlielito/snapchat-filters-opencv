import cv2

from video_loop import run_video_capture_pipeline


kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
fgbg = cv2.createBackgroundSubtractorMOG2()


def bg_substraction(image):
    image = fgbg.apply(image)
    image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    # Transform again to BGR
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    return image


run_video_capture_pipeline(transform_fn=bg_substraction)
