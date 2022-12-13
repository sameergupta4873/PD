import cv2
import time
import autopy
import HandTrackingModule as hmt
import numpy as np
import random
import math

wScr, hScr = autopy.screen.size()

wCam, hCam = 640, 480

plocX , plocY = 0,0
clocX, clocY = 0, 0

smoothening = 2


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    detector = hmt.handleDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        
        
        
        
        
        if len(lmList) != 0:
            # print(lmList[4])
            x = np.interp(lmList[4][1], (0, wCam), (0, wScr)) 
            y = np.interp(lmList[4][2], (0, hCam), (0, hScr))
            
            fingers = detector.fingersUp()
            
            print(fingers)
            
            
            clockX = plocX + (x - plocX) / smoothening
            clockY = plocY + (y - plocY) / smoothening
            
            if fingers[1] == 1 and fingers[2] == 0:
                autopy.mouse.move(wScr - clockX, clockY)
            if fingers[1] == 1 and fingers[2] == 1:
            # 9. Find distance between fingers
                length, img, lineInfo = detector.findDistance(8, 12, img)
                print(length)
            # 10. Click mouse if distance short
                if length < 40:
                    cv2.circle(img, (lineInfo[4], lineInfo[5]),15, (0, 255, 0), cv2.FILLED)
                    autopy.mouse.click()
            
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Img", img)
        cv2.waitKey(1)

if __name__ == '__main__' :
    main()
