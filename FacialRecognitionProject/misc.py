# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 11:51:03 2018

@author: jmidv
"""

import os
import shutil

def main():
    
    # clean directory
    files = os.listdir("database/")
    for file in files:
        path = "database/" + file
        shutil.rmtree(path)
    
    return 
    names = ["JeremyMidvidy", "Grant Cohen", "Jonah Kaplan"]
    for name in names:
        os.mkdir("database/" + name)
    
    
    
    return

if __name__ == "__main__":
    main()