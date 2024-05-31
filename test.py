import time
import cv2
import background

# Use 40 background threads.
background.n = 40


@background.task
def work():
    img = cv2.imread("Screenshot.png")
    print(img)

@background.callback
def work_callback(future):
    print(future.result())


for _ in range(100):
    work()