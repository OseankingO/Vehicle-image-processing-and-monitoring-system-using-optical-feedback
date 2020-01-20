import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time

camera = PiCamera()
camera.resolution = (480, 480)  
camera.framerate = 32  
rawCapture = PiRGBArray(camera, size=(480, 480))

car_cascade = cv2.CascadeClassifier('cars.xml')
num = 1

time.sleep(2)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):  

    img = frame.array
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cars = car_cascade.detectMultiScale(gray, 1.4, 1)
    for (x,y,w,h) in cars:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0,0,255), 2)
  
    cv2.imshow("Frame", img)
    key = cv2.waitKey(1) & 0xFF  
 
    rawCapture.truncate(0)  

    if key == ord("q"):  
        break
    if key == ord('p'):
        cv2.imwrite('car'+str(num)+'.jpg',img)
        num=num+1

cv2.destroyAllWindows()


