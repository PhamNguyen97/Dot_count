import cv2
import numpy as np
 
min_threshold = 10                      # these values are used to filter our detector.
max_threshold = 200                     # they can be tweaked depending on the camera distance, camera angle, ...
min_area = 100                          # ... focus, brightness, etc.
min_circularity = .3
min_inertia_ratio = .5
 

def count(org_img,img,pos_x,pos_y):
    counter = 0                             # script will use a counter to handle FPS.
    readings = [0, 0]                       # lists are used to track the number of pips.
    display = [0, 0]
    text_mask = np.zeros((img.shape[0],img.shape[1],3),np.uint8)
     
    while True:
        if counter >= 90000:                # set maximum sizes for variables and lists to save memory.
            counter = 0
            readings = [0, 0]
            display = [0, 0]

     
        params = cv2.SimpleBlobDetector_Params()                # declare filter parameters.
        params.filterByArea = True
        params.filterByCircularity = True
        params.filterByInertia = True
        params.minThreshold = min_threshold
        params.maxThreshold = max_threshold
        params.minArea = min_area
        params.minCircularity = min_circularity
        params.minInertiaRatio = min_inertia_ratio
     
        detector = cv2.SimpleBlobDetector_create(params)        # create a blob detector object.
     
        
        keypoints = detector.detect(img)   


        org_img = cv2.drawKeypoints(org_img, keypoints, np.array([]), (0, 0, 255),
                                              cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        reading = len(keypoints)                                # 'reading' counts the number of keypoints (pips).
     
        if counter % 10 == 0:                                   # enter this block every X frames.
            readings.append(reading)                            # note the reading from this frame.
     
            if readings[-1] == readings[-2] == readings[-3]:    # if the last 3 readings are the same...
                display.append(readings[-1])                    # ... then we have a valid reading.

            if display[-1] != display[-2] and display[-1] != 0:
                msg = "num:" + str(display[-1]) 

                cv2.putText(org_img,msg,(pos_y,pos_x),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2,cv2.LINE_AA)
     
        counter += 1

        if counter == 60:
            break

    return org_img
