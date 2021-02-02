# import the opencv library
import cv2
import time
import pyautogui
import numpy as np

def webcam():
    vid = cv2.VideoCapture(0)

    i = 0
    while i < 3:
        i += 1
        ret, frame = vid.read()
        time.sleep(1.2)

        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        result, code = cv2.imencode('.jpg', frame, encode_param)
        cv2.imwrite('camera{}.jpg'.format(i), frame)

    vid.release()
    cv2.destroyAllWindows()


def screenshot():
    ss = pyautogui.screenshot()
    ss = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
    cv2.imwrite("screenshot1.png", ss)
    time.sleep(5.0)
    ss = pyautogui.screenshot()
    ss = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
    cv2.imwrite("screenshot2.png", ss)
