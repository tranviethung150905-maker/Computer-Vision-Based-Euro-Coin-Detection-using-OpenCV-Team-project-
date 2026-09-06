import cv2
import numpy as np
import math


def calibration_mode(img, gray):

    # radius for return later:
    float_radius = 0

    output = img.copy()  #if do output = img then output is alias of img instead
    blur = cv2.medianBlur(gray, 19)

    thresh = cv2.adaptiveThreshold(
    blur, 255, 
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV, 11,2
    )
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    kernel_1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=7)
    eroded = cv2.erode(closed, kernel_1, iterations=2)


    contours, _= cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    out = cv2.drawContours(img, contours, -1, (0,0,255), 3)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        peri = cv2.arcLength(cnt, True)
    
        # small noise filter
        if area < 500:
                continue
    
        # Circularity_calculate
        if peri == 0: 
            continue
        circularity = (4 * math.pi * area) / (peri ** 2)
    
        # if circularity satisfied
        if 0.62 < circularity < 1:
            # Extract radius and ceter
            x, y, w, h = cv2.boundingRect(cnt)
            (cx, cy), radius = cv2.minEnclosingCircle(cnt)
            print('Radius', radius)
            x, y, w, h = int(x), int(y), int(w), int(h)
            center = (int(cx), int(cy))
            float_radius = radius
            radius = int(radius)
        
            # Draw result
            cv2.rectangle(output, (x,y), (x+w, y+h), (255, 0, 0), 2)
            cv2.circle(output, center, radius, (0, 255, 0), 2)



    resized_img = cv2.resize(output, (1080, 720))
    threshold = cv2.resize(closed, (1080, 720))
    threshold_eroded = cv2.resize(eroded, (1080, 720))
    img_contours = cv2.resize(out, (1080, 720))

    #cv2.imshow('Contours', img_contours)
    #cv2.imshow('Threshold closed', threshold)
    #cv2.imshow('Threshold eroded', threshold_eroded)
    cv2.imshow('Detected Circles', resized_img)

    return float_radius