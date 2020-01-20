import urllib.request
import cv2
import numpy as np
import os

def delete():
    match = False
    for file_type in ['neg']:
        for img in os.listdir(file_type):
            for error in os.listdir('errors'):
                try:
                    current_image_path = str(file_type)+'/'+str(img)
                    error = cv2.imread('errors/'+str(error))
                    question = cv2.imread(current_image_path)
                    if error.shape == question.shape and not(np.bitwise_xor(error,question).any()):
                        print('That is one error pic! Deleting!')
                        print(current_image_path)
                        os.remove(current_image_path)
                except Exception as e:
                    print(str(e))

delete()
