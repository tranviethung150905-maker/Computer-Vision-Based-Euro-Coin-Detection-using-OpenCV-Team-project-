import cv2
import numpy as np
import math

def resize(img):
    if(img.shape[1]>img.shape[0]):
        scale = 1280 / img.shape[1]
        new_width  = int(img.shape[1] * scale)
        new_height = int(img.shape[0] * scale)
        img = cv2.resize(img, (new_width, new_height))

    else:
        scale = 1280 / img.shape[0]
        new_height  = int(img.shape[0] * scale)
        new_width = int(img.shape[1] * scale)
        img = cv2.resize(img, (new_width, new_height))
    return img