    
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import copy
import time
from ControllerPong import *

ctrl = ControllerPong(800,600,50,20)
    

# define the lower and upper boundaries of the "green"
# ball in the HSV color space   
greenLower = (65,60,60)
greenUpper = (80,255,255)

blueLower = (100,100,100)
blueUpper = (180,255,255)

singlePlayer = True

# initialize the list of tracked points, the frame counterR,
# and the coordinate deltas
ptsR = deque(maxlen=20)
ptsL = deque(maxlen=20)
counterR, counterL = 0, 0
dYR, dYL = 0, 0 
directionR, directionL = "", ""

vs = VideoStream(src=0).start()

# allow the camera or video file to warm up
time.sleep(2.0)

def drawLine(frame):
    for i in range(10,600,60):
        cv2.line(frame,(390,i),(390,i+30),(80,80,80),20)
    cv2.rectangle(frame,(10,10),(790,590),(0,0,0),20)


def updateM(frame):
    global ctrl

    ctrl.update()

    posL = ctrl.getPadPosL()
    posR = ctrl.getPadPosR()
    posB = ctrl.getBallPos()
        
    cv2.circle(frame, (int(posB[0]), int(posB[1])), 5, (0,0,0),20)
    cv2.line(frame,(posL[0],posL[1]),(posL[0], posL[1]+50),(0,255,0),20)
    cv2.line(frame,(posR[0],posR[1]),(posR[0], posR[1]+50),(0,0,255),20)


jp = 0
# keep looping
while True:
    # grab the current frame
    frame = vs.read()
    frame = cv2.flip(frame,1)

    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=800)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    

    # construct a maskR for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the maskR
    maskR = cv2.inRange(hsv, greenLower, greenUpper)
    maskR = cv2.erode(maskR, None, iterations=2)
    maskR = cv2.dilate(maskR, None, iterations=2)

    maskL = cv2.inRange(hsv, blueLower, blueUpper)
    maskL = cv2.erode(maskL, None, iterations=2)
    maskL = cv2.dilate(maskL, None, iterations=2)
    
    # find contours in the maskR and initialize the current
    # (x, y) centerR of the ball
    cntsR = cv2.findContours(maskR.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntsR = imutils.grab_contours(cntsR)
    centerR = None

    cntsL = cv2.findContours(maskL.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntsL = imutils.grab_contours(cntsL)
    centerL = None
    
    # only proceed if at least one contour was found
    if len(cntsR) > 0:
        # find the largest contour in the maskR, then use
        # it to compute the minimum enclosing circle and
        # centroid
        cR = max(cntsR, key=cv2.contourArea)
        ((xR, yR), radiusR) = cv2.minEnclosingCircle(cR)
        MR = cv2.moments(cR)
        centerR = (int(MR["m10"] / MR["m00"]), int(MR["m01"] / MR["m00"]))

        # only proceed if the radius meets a minimum size
        if radiusR > 10:
            ptsR.appendleft(centerR)
            
    # only proceed if at least one contour was found
    if len(cntsL) > 0:
        # find the largest contour in the maskR, then use
        # it to compute the minimum enclosing circle and
        # centroid
        cL = max(cntsL, key=cv2.contourArea)
        ((xL, yL), radiusL) = cv2.minEnclosingCircle(cL)
        ML = cv2.moments(cL)
        centerL = (int(ML["m10"] / ML["m00"]), int(ML["m01"] / ML["m00"]))

        # only proceed if the radius meets a minimum size
        if radiusL > 10:
            ptsL.appendleft(centerL)
            #print(len(ptsL))
    
    # loop over the set of tracked points
    for i in np.arange(1, len(ptsR)):
        # if either of the tracked points are None, ignore
        # them
        if ptsR[i - 1] is None or ptsR[i] is None:
            continue

        # check to see if enough points have been accumulated in
        # the buffer
        try:
            if counterR > 10 and i == 1 and ptsR[-10] is not None:
            # compute the difference between the x and y
                # coordinates and re-initialize the directionR
                # text variables
                dYR = ptsR[-10][1] - ptsR[i][1]
                dirYR = " "

                # ensure there is significant movement in the
                # y-directionR
                if np.abs(dYR) > 10:
                    dirYR = "N" if np.sign(dYR) == 1 else "S"

                # handle when both directionRs are non-empty
                if dirYR != "":
                    directionR = "{}".format(dirYR)
        except:
            pass
        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(10 / float(i + 1)) * 2.5)
        cv2.line(frame, ptsR[i - 1], ptsR[i], (152,251,152), thickness)

    # loop over the set of tracked points
    for i in np.arange(1, len(ptsL)):
        # if either of the tracked points are None, ignore
        # them
        if ptsL[i - 1] is None or ptsL[i] is None:
            continue

        # check to see if enough points have been accumulated in
        # the buffer
        try:
            if counterL > 10 and i == 1 and ptsL[-10] is not None:
                # compute the difference between the x and y
                # coordinates and re-initialize the directionR
                # text variables
                dYL = ptsL[-10][1] - ptsL[i][1]
               # print(ptsL[-10][1] - ptsL[i][1])
                dirYL = " "

                # ensure there is significant movement in the
                # y-directionR
                if np.abs(dYL) > 10:
                    dirYL = "N" if np.sign(dYL) == 1 else "S"

                # handle when both directionRs are non-empty
                if dirYL != "":
                    directionL = "{}".format(dirYL)
        except:
            pass
        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(10 / float(i + 1)) * 2.5)
        cv2.line(frame, ptsL[i - 1], ptsL[i], (240,128,128), thickness)  
        #if dYL !=0 or dYR !=0:     
        # show the movement deltas and the directionR of movement on
	#print("dirL:  " + directionL + "     dYL:  " + str(dYL) +  "     dirR:  " +  directionR + "     " +   "     dYR:  " + str(dYR))
        
        # show the frame to our screen and increment the frame counterR
    blank_image = np.zeros((600,800,3), np.uint8)
    blank_image[:,:] = (255,255,255)

    frame = cv2.addWeighted(frame, 0.4, blank_image, 0.4, 0)
        
    if singlePlayer == False:
            ctrl.moveL(dYL)
    else:
        if ctrl.getBallPos()[0] > 400:
            ctrl.learnL(dYR)
        ctrl.moveAiL()
        
    ctrl.moveR(dYR)

    drawLine(frame)     
    updateM(frame)
    #cv2.imwrite(str(jp)+".jpg",frame)

    cv2.putText(frame,str(ctrl.getScore()[0]), (300,80), cv2.FONT_HERSHEY_DUPLEX, 2, (255,255,255))
    cv2.putText(frame,str(ctrl.getScore()[1]), (450,80), cv2.FONT_HERSHEY_DUPLEX, 2, (255,255,255))
    cv2.imshow("Pong", frame)
    key = cv2.waitKey(1) & 0xFF
    counterR += 1
    counterL += 1
    jp+=1

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break


# close all windows
cv2.destroyAllWindows()
