# -*- coding: utf-8 -*-
"""
EECS 332, Fall 2018
MP4: Histogram-based skin color detection

@author: Jeremy Midvidy, jam658
"""
import sys
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import math

prec_h = 0
prec_s = 0
################################################################
# ---- Off the Shelf hsv2rgb and rgb2hsv converters ---------- #
################################################################

def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b
    
def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v

#####################################################################
#####################################################################
# -------------------- MAIN IMPLEMENTATION ------------------------ #
#####################################################################
#####################################################################   

# read an Input image, and convert it to hsv matrix of pixels
def readImagetoHSVMatrix(p):
    A = mpimg.imread(p).tolist()
    for r in range(0, len(A)):
        for c in range(0, len(A[0])):
            A[r][c] = [int(A[r][c][0]), int(A[r][c][1]), int(A[r][c][2])] 
    B = []
    for row in A:
        curr = []
        for line in row:
            h,s,v = rgb2hsv(line[0], line[1], line[2])
            h = round(h,prec_h) # round h and s values for smoothing
            s = round(s,prec_s) # see if this works correctly
            curr.append([h,s,v])
        B.append(curr)
    return B

# train the histogram off the files in train folder
def train2DHist(p):
    # build 2D histogram of dictionary of dictionaries
    # { h1 : {s1 : val1, s2: val2, s3:val3}, h2 : {s1 : val1, s2: val2, s3:val3} etc...}
    files = os.listdir(p)
    hist = {}
    print("Training!")
    for elem in files:
        #print("Training on: " + elem)
        A = mpimg.imread(p+elem).tolist()
        # floor all values <-- might want to reconsider after testing
        for r in range(0, len(A)):
            for c in range(0, len(A[0])):
                A[r][c] = [int(A[r][c][0]), int(A[r][c][1]), int(A[r][c][2])] 
        for row in A:
            for line in row:
                h,s,v = rgb2hsv(line[0], line[1], line[2])
                h = round(h,prec_h) # round h and s values for smoothing
                s = round(s,prec_s) # see if this works correctly
                if h in hist:
                    if s in hist[h]:
                        hist[h][s] += 1
                    else:
                        hist[h][s] = 1
                else:
                    hist[h] = {s: 1}
    return hist

# Normalize and quantize the trained histogram
def process2DHist(h):
    # first get count of number of elements
    count = 0
    for key in h:
        for e in h[key]:
            count += h[key][e]
            
    # divide each bin-value by count
    quant = {}
    for key in h:
        curr = {}
        temp = h[key]
        for e in temp:
            curr[e] = temp[e] / count
        quant[key] = curr
        
    total = 0
    for key in sorted(quant.keys()):
        temp = quant[key]
        for e in temp:
            total += temp[e]
            quant[key][e] = total
            
    max_val = max(quant.keys())
    for key in quant:
        for e in quant[key]:
            quant[key][e] = quant[key][e] * max_val
    
    return quant

# Classify a given input against trained histogram 
def testInput(p, hist):
    threshold = 20 # <-- threshold for now
    out = []
    A = readImagetoHSVMatrix(p)
    for r in range(0, len(A)):
        curr = []
        for c in range(0, len(A[0])):
            cell = A[r][c]
            h = cell[0]
            s = cell[1]
            try:
                temp = hist[h]
                val  = temp[s]
                if val > threshold:
                    curr.append(A[r][c])
                else:
                    curr.append([0,0,0])
            except:
                curr.append([0,0,0])
        out.append(curr)
    return out

# When no command line input, run all tests in "testimages//" directory
def mainRunAll():
    tests = os.listdir("testimages//")
    for elem in tests:
        print("Processing on: " + elem)
        main("testimages//" + elem)
        print("Done\n")
    return

# Main logic of program
def main(p):
    train_path = "skinimages//"
    hist = train2DHist(train_path)
    hist = process2DHist(hist)
    result = testInput(p, hist)
    #print(result)
    # use original colors because I lost a lot of accuracy
    A = mpimg.imread(p).tolist()
    I = []
    for r in range(0, len(result)):
        curr = []
        for c in range(0, len(result[0])):
            if result[r][c] == [0,0,0]:
                curr.append([0,0,0])
            else:
                curr.append(A[r][c])
        I.append(curr)
    ret = np.array(I)
    if "testimages//" in p:
        p = p[11:]
    end_path = "results//" + p + "_result.jpeg" 
    mpimg.imsave(end_path, ret.astype(np.uint8))
    
    for key in sorted(hist.keys()):
        print(str(key) + " : " + str(hist[key])) 
    
    return

# Call main
if __name__ == "__main__":
    try:
        p = sys.argv[1]
    except:
        p = "runall"
    if p == "runall":
        mainRunAll()
    else:
        main(p)