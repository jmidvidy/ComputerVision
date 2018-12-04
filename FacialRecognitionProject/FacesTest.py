# -*- coding: utf-8 -*-
"""
EECS 332: Computer Vision, Fall 2018
Final Project: A Simple Facial Recognition System 

@author: Jeremy Midvidy, jam658
@about: A Facial Recognition system implemented in Python 3.7 and OpenCV.
"""

import cv2
import matplotlib.image as mpimg
import os

def main(img_path):
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainner.yml")
    images = os.listdir(img_path)
    
    confs = []
    for image in images:
        curr_path = img_path + "/" + image
        A = mpimg.imread(curr_path)
        predict_id, conf = recognizer.predict(A)
        confs.append(conf)
        
    avg_conf = sum(confs) / len(confs)
    
    #print("\t Confidence:", conf)
    
    if avg_conf > 50:
        return "REJECT"
    else:
        return "ACCEPT"

    return

if __name__ == "__main__":
    main()

