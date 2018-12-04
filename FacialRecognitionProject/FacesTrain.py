# -*- coding: utf-8 -*-
"""
EECS 332: Computer Vision, Fall 2018
Final Project: A Simple Facial Recognition System 

@author: Jeremy Midvidy, jam658
@about: A Facial Recognition system implemented in Python 3.7 and OpenCV.
"""

import cv2
import os
import numpy as np
import matplotlib.image as mpimg

def main(image_folder_path):

    # ----------------------- Choose CV2 classifier tools --------------------- #
        
    # used for classification
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(base_dir, image_folder_path)
    
    x_train = []
    y_labels = []
    label_ids = {}
    current_id = 0
    # ----------------------- ITERATE THROUGH DATABASE AND GATHER FACES ------------------------ #
    count = 0
    train_folders = os.listdir(image_dir)    
    for folder in train_folders:
        curr_path = image_dir + "\\" + folder + "\\"
        images = os.listdir(curr_path)
        for image in images:
            image_path = curr_path + "\\" + image
            label = folder
            # EXTRACT current facial features from the GIVEN current image
            A = mpimg.imread(image_path)
            
            if label not in label_ids:
                label_ids[label] = current_id
                current_id += 1
            this_id = label_ids[label]
            x_train.append(A)
            y_labels.append(this_id)

            # debugging for now
            if count == -1:
                return
            
            count += 1
            
    # -------------------------- TRAINING CLASSIFIER FROM GATHERED DATA ------------------- #        
    # train the openCV recognizer
    recognizer.train(x_train, np.array(y_labels))
    recognizer.save("trainner.yml")
    
    return label_ids
    

if __name__ == "__main__":
    main("dabases/")












            
