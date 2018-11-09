# -*- coding: utf-8 -*-
"""
EECS 332, Fall 2018
MP5: Canny Edge Detector

@author: Jeremy Midvidy, jam658
"""
import sys
import numpy as np
import matplotlib.image as mpimg
import scipy.ndimage as ndimage
from skimage import filters
import copy
import os

def to_31Array(A):
    B = []
    for row in A:
        curr = []
        for elem in row:
            curr.append(elem[0])
        B.append(curr)
    return B

def to_13Array(A):
    ret = []
    for row in A:
        curr = []
        for elem in row:
            curr.append([elem,elem,elem])
        ret.append(curr)
    return ret

# save an image to a directory
# process from [cell] to [cell,cell,cell] for each cell
def saveImage(I, path):
    mpimg.imsave(path, I.astype(np.uint8))
    return

# implement GaussianSmoothing with built in ndimage function
# allowed because can use built in MatLab function
def GaussSmoothing(I, sigma):
    return ndimage.filters.gaussian_filter(I, sigma)

# magnitude and direction of edge map
def ImageGradient(A):    
    # implements Robert Cross filters
    # flatten from [cell,cell,cell] to [cell]
    #A = np.array(to_31Array(A.tolist()))
    rc_v = np.array([[0, 0, 0],[ 0, 1, 0],[ 0, 0, -1]])
    rc_h = np.array([[0, 0, 0],[ 0, 0, 1],[ 0, -1, 0]])
    
    # apply roberts cross convolution
    Gy = ndimage.convolve(A, rc_v)
    Gx = ndimage.convolve(A, rc_h)
    
    # resolve final image
    out = np.sqrt(np.square(Gy) + np.square(Gx))
    
    # transform from [cell] to [cell,cell,cell]
    out = np.array(to_13Array(out.tolist()))
    
    # extract magnitude and theta
    mag = np.power(np.power(Gy, 2.0) + np.power(Gx, 2.0), 0.5)
    theta = np.arctan2(Gy, Gx)

    return out, mag, theta

# Select high and low thresholds for later processing
def FindThreshold(A): #mag, percentageOfNoneEdge
    A = np.array(to_31Array(A.tolist()))
    v = filters.threshold_otsu(A)   
    # HAVE TO FIX THIS PART LATER
    
    return .5*v, v

# supress pixels that are not local maxima
def NonmaximaSuppress(mag, theta, A):
    out = copy.deepcopy(mag)
    R = A.shape[0]
    C = A.shape[1]
    
    def isSmallest(nums):
        min_val = min(nums)
        if min_val == nums[0]:
            return True
        return False
        
    for r in range(0, R):
        for c in range(0, C):
            # at image edge
            if (r == 0 or r == R - 1) or (c == 0 or c == C - 1):
                out[r, c] = 0
                continue
            # gather direction via theta vector
            line =int(theta[r, c] % 4)
            #print(theta[r,c],line)
            val = mag[r,c]
            
            # 0 HORIZONTAL
            if line == 0 and isSmallest([val, mag[r, c-1], mag[r, c+1]]):
                    out[r, c] = 0
            # 1 UPLEFT-DOWNRIGHT DIAGONAL
            elif line == 1 and isSmallest([val, mag[r-1, c+1], mag[r+1, c-1]]):
                    out[r, c] = 0
            # 2 VERTICAL
            elif line == 2 and isSmallest([val, mag[r-1, c], mag[r+1, c]]):
                    out[r, c] = 0
            # 3 UPRIGHT-DOWNLEFT DIAGONAL
            else:
                if isSmallest([val, mag[r-1, c-1], mag[r+1, c+1]]):
                    out[r, c] = 0
    return out

def EdgeLinking(A, T_low, T_high, flag):
    R = A.shape[0]
    C = A.shape[1]
    out = []
    for i in range(0, R):
        out.append([0]*C)
    for r in range(0, R):
        for c in range(0, C):
            val = A[r][c]
            if val >= T_high:
                out[r][c] = 255
                # Consider neighbors in 8 directions
                # UP
                if flag == "TLOW":
                    try:
                        if A[r-1][c] > T_low:
                            out[r-1][c] = 255
                    except:
                        pass
                    # UP-RIGHT
                    try:
                        if A[r-1][c+1] > T_low:
                            out[r-1][c+1] = 255
                    except:
                        pass
                    # UP-LEFT
                    try:
                        if A[r-1][c-1] > T_low:
                            out[r-1][c-1] = 255
                    except:
                        pass
                    # LEFT
                    try:
                        if A[r][c-1] > T_low:
                            out[r][c-1] = 255
                    except:
                        pass
                    # RIGHT
                    try:
                        if A[r][c+1] > T_low:
                            out[r][c+1] = 255
                    except:
                        pass
                    # DOWN
                    try:
                        if A[r+1][c] > T_low:
                            out[r+1][c] = 255
                    except:
                        pass
                    # DOWN-LEFT
                    try:
                        if A[r+1][c-1] > T_low:
                            out[r+1][c-1] = 255
                    except:
                        pass
                    # DOWN-RIGHT
                    try:
                        if A[r+1][c+1] > T_low:
                            out[r+1][c+1] = 255
                    except:
                        pass
              
    return np.array(out)

def gray2rgb(I):
    I = I.tolist()
    out = []
    for row in I:
        curr = []
        for col in row:
            curr.append([col, col, col])
        out.append(curr)
    return np.array(out)
  
# Main logic of program
def main(A):
    
    B = copy.deepcopy(A)
        
    # (2) Calculating Image Gradient
    A, mag, theta = ImageGradient(A)
    
    # (3) Selecting High and Low Thresholds
    T_low, T_high = FindThreshold(A) # need to change this
    
    # (4) Supressing Nonmaxima
    mag = NonmaximaSuppress(mag, theta, B)
        
    E = EdgeLinking(mag, T_low, T_high, "THIGH")
    
    return E
