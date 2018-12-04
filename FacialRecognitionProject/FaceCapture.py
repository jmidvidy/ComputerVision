# -*- coding: utf-8 -*-
"""
EECS 332: Computer Vision, Fall 2018
Final Project: A Simple Facial Recognition System 

@author: Jeremy Midvidy, jam658
@about: A Facial Recognition system implemented in Python 3.7 and OpenCV.
"""
import cv2

def main(out_path):
    # play with these --> currently FRONTAL_FACE
    face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
    
    # open image capture
    cap = cv2.VideoCapture(0)
    count = 0
    while count < 100:
        # capture frame by frame
        ret, frame = cap.read()
        
        # need to convert to gray
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # get all faces from the given frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        
        for (x,y,w,h) in faces:
            #print(x,y,w,h)
            # know that x,y,w,h is the ROI
            roi_gray = gray[y:y+h, x:x+w]
            
            # want to recognize frame and reigons of interest
            # deep learned model to predict things
            # Keras, TensorFlow, PyTorch, Scikit-learn
            out_file = out_path + "/" + str(count) + ".png"
            cv2.imwrite(out_file, roi_gray)
            
            # draw a rectangle
            color = (255, 0, 0) # BGR 0 -255
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
            cv2.rectangle(frame, (x,y), (end_cord_x, end_cord_y), color, stroke)
            count += 1
            
        
        # Display the resulting frame
        cv2.imshow('frame', frame)
        
        if (cv2.waitKey(10) and 0xFF == ord('q')):
            break
        
    # when everything is done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    
    return

if __name__ == "__main__":
    main("")






