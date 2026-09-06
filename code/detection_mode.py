import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import time

def detection_mode(img, gray, param2, minRadius, maxRadius, blur_size, pixel_ratio):
# Increase contrast
    clahe = cv2.createCLAHE(clipLimit=7.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)

        # Median blur
    blur = cv2.medianBlur(gray, blur_size)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #Hung
    h = hsv[:,:,0]
    s = hsv[:,:,1]
    #Hung

        # Hough circle
    circles = cv2.HoughCircles(
        blur,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=minRadius*2,
        param1=100,
        param2=param2,
        minRadius=minRadius,
        maxRadius=maxRadius)

    #for analyze only v
    coin_id = 0         
    # Lists for plotting
    hue_values = []
    sat_values = []
    hue_inner = []
    sat_inner = []
    #for analyze only ^

        # Draw overlaid circle
    if circles is not None:

        circles = np.uint16(np.around(circles))

        for (x, y, r) in circles[0]:
            coin_mask = np.zeros(gray.shape, dtype=np.uint8)
            cv2.circle(coin_mask, (x,y), r, 255, -1)

            h_pixels = h[coin_mask > 0]          
            s_pixels = s[coin_mask > 0]


            med_hue = np.median(h_pixels)
            med_sat = np.median(s_pixels)

            hue_values.append(med_hue)
            sat_values.append(med_sat)

            real_rad = r / pixel_ratio
            diameter_real = real_rad *2 

            coin_name = "None-euro coin"



            #classification
            if med_hue > 90:
                coin_name = "Not coin"
            

            if 24.5 <= diameter_real <= 26.8:
                if 15 <= med_hue <= 30 and 37 <= med_sat <= 85:
                    coin_name = "2 Euro"

            if 22.3 <= diameter_real <= 24.4:
                if 15 <= med_hue <= 30 and 25 <= med_sat <= 55:
                    coin_name = "1 Euro"

            if 23 <= diameter_real <= 25.5:
                if 16 <= med_hue <= 30 and 80 <= med_sat <= 130:
                    coin_name = "50 Cent"

            if 21 <= diameter_real <= 23:
                if 16 <= med_hue <= 30 and 80 <= med_sat <= 130:
                    coin_name = "20 Cent"

            if 19 <= diameter_real <= 20.5:
                if 16 <= med_hue <= 30 and 80 <= med_sat <= 130:
                    coin_name = "10 Cent"

            if 19.7 <= diameter_real <= 21.8:
                if 0 <= med_hue <= 14 and 70 <= med_sat <= 140:
                    coin_name = "5 Cent"

            if 17.7 <= diameter_real <= 19.5:
                if 0 <= med_hue <= 14 and 70 <= med_sat <= 140:
                    coin_name = "2 Cent"

            if 15.2 <= diameter_real <= 17.5:
                if 0 <= med_hue <= 14 and 70 <= med_sat <= 140:
                    coin_name = "1 Cent"

            #DECTECT IF THERE IS HOLES INSIDE THE COIN, CIRCULAR OBJECT
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
            mask = np.zeros(img.shape[:2], dtype=np.uint8)

            cv2.circle(
                mask,
                (x, y),
                r,
                255,
                -1
            )

            # Extract coin only
            coin_only = cv2.bitwise_and(
                img,
                img,
                mask=mask
            )


            # Crop coin region
            x1 = max(x - r, 0)
            y1 = max(y - r, 0)

            x2 = min(x + r, img.shape[1])
            y2 = min(y + r, img.shape[0])

            coin_crop = coin_only[y1:y2, x1:x2]

            if coin_crop.size == 0:
                print("empty")
            else:
                # Show extracted coin
                gray_coin_crop = cv2.cvtColor(coin_crop, cv2.COLOR_BGR2GRAY)

                inner_circles = None

                inner_circles = cv2.HoughCircles(
                gray_coin_crop,
                cv2.HOUGH_GRADIENT,
                dp=1,
                minDist=r,
                param1=100,
                param2=param2-10,
                minRadius=int(0.1*r),
                maxRadius=int(0.8*r))

                

                if inner_circles is not None:
                    inner_circles = np.uint16(np.around(inner_circles))
                    for(x1, y1, r1) in inner_circles[0]:
                        cv2.circle( coin_crop, (x1, y1), r1, (0,255,0), 2)
                        # cv2.imshow(f"Coin {coin_id}", coin_crop)

                        coin_mask_inner = np.zeros(gray.shape, dtype=np.uint8)
                        cv2.circle(coin_mask_inner, (x,y), r, 255, -1)

                        h_pixels_in = h[coin_mask > 0]          
                        s_pixels_in = s[coin_mask > 0]


                        med_hue_in = np.median(h_pixels_in)
                        med_sat_in = np.median(s_pixels_in)
                        print(med_hue_in)
                        print(med_hue_in)
                        print(med_hue_in)
                        print(med_hue_in)

                        hue_inner.append(med_hue_in)
                        sat_inner.append(med_sat_in)
                    if med_sat_in < 20:
                        coin_name = "Not coin"
            

            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            #DECTECT IF THERE IS HOLES INSIDE THE COIN, CIRCULAR OBJECT

            # Draw outer circle & its information
            cv2.circle( img, (x, y), r, (0,255,0), 2)
            cv2.putText(img, f"{coin_name}",
                        (x-r, y-r), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            
            # Draw center
            cv2.circle( img, (x, y), 2, (0,0,255), 3)

            # Print radius
            print("Radius =", r)
            print("Pixel ratio =", pixel_ratio)
            coin_id += 1

       
    #Canny (not used, for debug only)
    edges = cv2.Canny(blur, 50, 150)

    # Result
    cv2.imshow("Detected Circles", img)
    #cv2.imshow("Blur", blur)
    #cv2.imshow("Canny", edges)

    