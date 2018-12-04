# -*- coding: utf-8 -*-
"""
EECS 332: Computer Vision, Fall 2018
Final Project: A Simple Facial Recognition System 

@author: Jeremy Midvidy, jam658
@about: A Facial Recognition system implemented in Python 3.7 and OpenCV.
"""
    
import FaceCapture
import FacesTrain
import FacesTest
import time
import os
import shutil
import warnings

def main():
    
    # disable warning flags printed to command line
    warnings.filterwarnings("ignore")
    
    # first clean the database directory from previous files
    for file in os.listdir("database/"):
        cp = "database/" + file
        shutil.rmtree(cp)
        
    # second clean the testing directory
    for file in os.listdir("testing/"):
        cp = "testing/" + file
        os.remove(cp)

    print("\n")
    print("--------------------------------------------------------------------------------------------")
    print("--------------------------------------------------------------------------------------------")
    print("--------------------------------------------------------------------------------------------")
    print("\t~~~~~ Hello! Welcome to a simple Facial Recognition System! ~~~~~")
    print("\n")
    print("\t The first step of our Facial Recognition System is enrollment.")
    print("\t Are you ready to add a face to the database?")
    print("\n")
    response1 = input("\t[Y/N]? ").upper()
    print("\n")
    if response1 == "Y":
        print("\tGreat! Lets begin.")
    else:
        print("\tOk. Goodbye!")
        return
    
    print("\n")
    
    # ------------------------------------ ENROLLMENT ----------------------------------------- #
    
    # keep enrolling faces until terminal input says stop
    faces = []
    keep_adding = True
    while keep_adding:
        
        # disable warning flags printed to command line
        warnings.filterwarnings("ignore")
        print("\t------------------------------------------------------------------")
        print("\t Adding a face! Please enter the name of the person to be added.")
        
        # collect new input from command line
        newFaceName = input("\t  Name:  ")
        
        if newFaceName in faces:
            print("Woops! That name is already in the Database! Please enter a different name!")
            continue
        
        faces.append(newFaceName)
        
        # make directory with name as label for training
        os.mkdir("database/" + newFaceName)
        
        # launch camera applet
        print("\t  Launching Camera! Please look directly at the camera!")
        t0 = time.time()
        t1 = time.time()
        while abs(t1 - t0) < 1:
            t1 = time.time()
        
        # grab face
        FaceCapture.main("database/" + newFaceName)
        
        print("\t", newFaceName, "added to database!")
        print("\t------------------------------------------------------------------")
        print("\t Would you like to add another?")
        response2 = input("\t  [Y/N]? ").upper()
        if response2 != "Y":
            keep_adding = False
            
    print("\t------------------------------------------------------------------")
    print("\t Faces in Database:")
    count = 1
    for name in faces:
        print("\t\t", "(" + str(count) + "/" + str(len(faces)) + ")", name)
        count += 1
    print("\t------------------------------------------------------------------")
    print("\n")
    print("\t Enrollment Done!")
    
    # --------------------------------- TRAINING ---------------------------------------------#
    
    print("\t Now training recognizer on Face Database!")
    FacesTrain.main("database/")
    print("\t Training Done!")
    print("\n")
    
    # --------------------------------- TESTING ---------------------------------------------#
    
    print("\t The Simple Facial Recognition System can now classify input!")
    print("\t Do you want to try and fool me?")
    print("\n")
    response = input("\t [Y/N]? ").upper()
    play = True
    if response != "Y":
        play = False
    print("\n")
    # if the person wants to play
    if play:
        print("\t Ok then. Good luck!")
        print("\n")
        keep_testing = True
        while keep_testing:
            # disable warning flags printed to command line
            warnings.filterwarnings("ignore")
            print("\t------------------------------------------------------------------")
            print("\t Testing a face! Who do you claim to be?")
            
            # collect new input from command line
            newTestName = input("\t  Name: ")
            if newTestName not in faces:
                while True:
                    print("\t  Woops! The name you entered is not in the database. Please enter a different name!")
                    newTestName = input("\t  Name: ")
                    if newTestName in faces:
                        break
                
            # launch camera applet
            print("\t  Launching Camera! Please look directly at the camera!")
            t0 = time.time()
            t1 = time.time()
            while abs(t1 - t0) < 1:
                t1 = time.time()
            
            # grab face
            FaceCapture.main("testing/")
            
            # classify the input from the recognizer
            result = FacesTest.main("testing")
            
            if result == "REJECT":
                print("\t NO, you are NOT", newTestName, "!")
            else:
                print("\t YES, you ARE", newTestName, "!")
                
            print("\t------------------------------------------------------------------")
            print("\t Would you like to test another?")
            response2 = input("\t  [Y/N]? ").upper()
            if response2 != "Y":                      
                keep_testing = False
            else:
                #clean testing folder
                for file in os.listdir("testing/"):
                    cp = "testing/" + file
                    os.remove(cp) 
            
    print("\t------------------------------------------------------------------")
    print("\t Thanks for playing! Peace!")
    return

if __name__ == "__main__":
    main()
