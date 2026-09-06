import cv2
import numpy as np
import math
import statistics
from detection_mode import detection_mode
from calibration_mode import calibration_mode
from image_modification import resize
from math_function import param2_cal, minRadius_cal, maxRadius_cal, blur_size_cal
import time

# Global variable:
radius = 0
median_radius = 1
param2 = 0
minRadius = 0
maxRadius = 0
blur_size = 0
radiuses = [] # list of radius values

cap = cv2.VideoCapture(1)   # 0 = laptop camera
                            # 1 or 2 = external USB camera


# Window setting:
cv2.namedWindow("Detected Circles", cv2.WINDOW_NORMAL)



# Empty function:
def nothing(x):
    pass


# available mode:
mode = "detection"
mode = "calibration"


while True:


    # Read the camera:
    ret, img = cap.read()       #ret: camera work successfully or not     img: a frame of the video

    if not ret:
        print("Cannot read camera")
        break


    # Resize the image:
    img = resize(img)



    # Convert to gray scale:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)



    # Run detection mode:
    if(mode == "detection"):
        param2 = param2_cal(median_radius)
        minRadius = minRadius_cal(median_radius)
        maxRadius = maxRadius_cal(median_radius)
        blur_size = blur_size_cal(median_radius)
        print("\nparam2=",param2," minrad=", minRadius,"maxrad=",maxRadius,"blur_size=",blur_size)
        if blur_size % 2 == 0:
            blur_size += 1
        pixel_ratio = (median_radius * 2) / 25.75           #25.75 mm
        detection_mode(img, gray, param2, minRadius, maxRadius, blur_size, pixel_ratio) 

    # Run calibration mode:
    if(mode == "calibration"):

        radius = calibration_mode(img, gray)
        if radius != 0:
            radiuses.append(radius)
        if len(radiuses) !=0:
            median_radius = statistics.median(radiuses)
                
    
    
    # Mode choosing:
    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):
        mode = "calibration"
        radiuses.clear()        #clear list of radius whenever switch to calibrate mode

    elif key == ord('d'):
        mode = "detection"
        

    elif key == ord('q'):
        break




# cleaning:
cap.release()
cv2.destroyAllWindows()

