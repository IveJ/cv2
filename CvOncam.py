'''
Webcam Motion detect
'''
import os
import numpy as np
import cv2
import time
 
motion_detect = 0
md_switch ="OFF"
 
# check for folder
MYDIR = ("detected-images")
CHECK_FOLDER = os.path.isdir(MYDIR)
 
# If folder doesn't exist, then create it.
if not CHECK_FOLDER:
    os.makedirs(MYDIR)
 
os.chdir(MYDIR)
CURR_TIME = time.asctime()
 
# Change sdthresh to suit camera and conditions,
# 15-25 is usually within the threshold range.
sdThresh = 20
 
# Used to count individualy named frames as jpgs.
img_index = 0
 
# use this cv2 font
font = cv2.FONT_HERSHEY_SIMPLEX
 
def distMap(frame1, frame2):
    '''outputs pythagorean distance between two frames'''
    frame1_32 = np.float32(frame1)
    frame2_32 = np.float32(frame2)
    diff32 = frame1_32 - frame2_32
    norm32 = np.sqrt(diff32[:,:,0]**2 + diff32[:,:,1]**2 + diff32[:,:,2]**2)/np.sqrt(255**2 + 255**2 + 255**2)
    dist = np.uint8(norm32*255)
    return dist
 
def print_date_time():
    '''Updates current date and time on to video'''
    CURR_TIME = time.asctime()
    cv2.putText(frame2,str(CURR_TIME),(280,24),font, 0.8, (0,255,0),2, cv2.LINE_AA)
    cv2.putText(frame2,"Enter to pause. q to quit. Sensitivity = "+str(sdThresh)+". Press + and - to change." ,(10,450), font, 0.5,(255,255,255),1)
    cv2.putText(frame2,"Save detected images is: "+str(md_switch)+". press m to start auto saving. s to stop again.",(10,470), font, 0.5,(255,255,255),1)
 
# Capture video stream.
cap = cv2.VideoCapture(0)
_, frame1 = cap.read()
_, frame2 = cap.read()
 
# main loop
while(True):
 
    try:
        _, frame3 = cap.read()
        rows, cols, _ = np.shape(frame3)
        dist = distMap(frame1, frame3)
    except:
        print("Camera not found.")
        exit(0)
 
    frame1 = frame2
    frame2 = frame3
    keyPress = cv2.waitKey(20)
 
    # Apply Gaussian smoothing.
    mod = cv2.GaussianBlur(dist, (9,9), 0)
    # Apply thresholding.
    _, thresh = cv2.threshold(mod, 100, 255, 0)
    # Calculate st dev test.
    _, stDev = cv2.meanStdDev(mod)
 
    # If motion is dectected.
    if stDev > sdThresh :
            #print("Motion detected")
            cv2.putText(frame2,"MD "+str(img_index), (0,20),font, 0.8, (0,255,0),2, cv2.LINE_AA)
            print_date_time()
 
            # Save jpg.
            if motion_detect == 1:
                frame_name =(str(img_index)+str(".jpg"))
                cv2.imwrite(frame_name, frame2)
                #print("saved", frame_name)
                img_index +=1
 
    print_date_time()
    cv2.imshow('Live video', frame2)
 
    # Enter key pauses video stream.
    if keyPress & 0xFF == 13:
        cv2.putText(frame2,"PAUSED", (210,260),font, 2, (0,255,0),8, cv2.LINE_AA)
        cv2.imshow('Live video', frame2)
        cv2.waitKey(0)
 
    # Hold down Escape key to quit.
    if keyPress & 0xFF == ord('q'):
        break
 
    # motion detect off
    if keyPress & 0xFF == ord('s'):
        motion_detect = 0
        md_switch = "OFF"
 
    #motion detect on
    if keyPress & 0xFF == ord('m'):
        motion_detect = 1
        md_switch = "ON"
 
    #sensitivity +
    if keyPress & 0xFF == ord('+'):
        sdThresh +=1
T    #sensitivity -
    if keyPress & 0xFF == ord('-'):
        sdThresh -=1
 
cap.release()
cv2.destroyAllWindows()
