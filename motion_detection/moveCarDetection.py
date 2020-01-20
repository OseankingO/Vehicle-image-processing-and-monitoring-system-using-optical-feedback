import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time

camera = PiCamera()
camera.resolution = (480, 480)  
camera.framerate = 32  
rawCapture = PiRGBArray(camera, size=(480, 480))
fgbg = cv2.createBackgroundSubtractorMOG2()
kernel = np.ones((5,5), np.uint8)
num = 1
carDetecting = 0
wait = 0
carNum = -1


time.sleep(2)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):  
    
    image = frame.array
    
    fgmask = fgbg.apply(image)
    clearMask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    imgH, imgW, imgC = image.shape
    totalPixels = imgH*imgW

    white = cv2.countNonZero(clearMask)
##    white2 = cv2.countNonZero(fgmask)
    rate = white/totalPixels
##    rate2 = white2/totalPixels

    font = cv2.FONT_HERSHEY_SIMPLEX
    
##    print(rate)

    if rate >= 0.2 and  carDetecting ==0:
        carDetecting = 1
        carNum = carNum + 1
        cv2.putText(image, 'There is a new car!', (100, 200), font, 0.7, (255,0,0), 1, cv2.LINE_AA)

    if rate >= 0.2 and  carDetecting ==1:
        cv2.putText(image, 'There is a new car!', (100, 200), font, 0.7, (255,0,0), 1, cv2.LINE_AA)
    
    if rate < 0.2 and carDetecting ==1:
        carDetecting = 0

    img = cv2.bitwise_and(image, image, mask = clearMask)

    cv2.putText(image, str(carNum) + ' vehicles have been detected', (20,20), font, 0.7, (0,0,255), 1, cv2.LINE_AA)

##    cv2.imshow("fg", fgmask)
    cv2.imshow("clear", clearMask)
    cv2.imshow("processed", img)
    cv2.imshow("origial", image)


    key = cv2.waitKey(1) & 0xFF  
  
    rawCapture.truncate(0)  
  
    if key == ord('q'):  
        break

    if key == ord('a'):
        cv2.imwrite ('out_cl1'+str(num)+'.jpg',clearMask)
        cv2.imwrite ('out_or'+str(num)+'.jpg',image)
        cv2.imwrite ('out_af'+str(num)+'.jpg',img)
        num = num+1
        print (str(rate))

cv2.destroyAllWindows()



