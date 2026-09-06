import cv2
import numpy as np
import math
import statistics

def param2_cal(median_radius):
    a = 2.5
    b = 66.6326539
    c = 70.40334904
    d = 47.5
    if(median_radius == 0):
        return 45
    else:
        return round(a*math.tanh(b*(median_radius - c)) + d)



def minRadius_cal(median_radius):
    if(median_radius == 0):
        return 20
    else:
        return math.floor(0.5879*median_radius - 2.731 -1)



def maxRadius_cal(median_radius):
    if(median_radius == 0):
        return 100
    else:
        return math.ceil(1.060*median_radius + 2.409)



def blur_size_cal(median_radius):
    a = 36.78748
    b = -0.7294149
    c = 0.005024835
    if(median_radius==0):
        print("\nBlur size faild to calculate (median_radius = 0)")
        return 11
    if(median_radius<52.5):
        return 13
    if(median_radius>100):
        return 18
    else:
        return 11