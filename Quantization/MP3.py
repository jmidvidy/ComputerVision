# -*- coding: utf-8 -*-
"""
EECS 332, Fall 2018
MP3: Histogram Equalization

@author: Jeremy Midvidy, jam658
"""

import sys
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

# return grey-level image
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

# given a grey-level image, return RGB (for output)
def to_rgb(im):
    w, h = im.shape
    ret = np.empty((w, h, 3), dtype=np.uint8)
    ret[:, :, 2] =  ret[:, :, 1] =  ret[:, :, 0] =  im
    return ret

# iterate through a matrix and make a count
# also keep track of total number of pixels
def makeBins(A):
    bins = {}
    count = 0
    for row in A:
        for elem in row:
            if elem in bins:
                bins[elem] += 1
            else:
                bins[elem] = 1
            count += 1
    return bins, count

# given a dictionary, write
# it to histogram with appropriate title
def makeHistogram(d,p,tag):
    l = path
    if tag == 'b':
        l += " histogram before equaliztion"
    else:
        l += " histogram after equaliztion"
    plt.bar(list(d.keys()), d.values(), color='g', label=l)
    plt.title(l)
    plt.xlabel("pixel intensity value")
    plt.ylabel("number of occurences of each pixel intensity")
    plt.savefig("results//" + l + ".png")
    return

# --------------------------------------- #
# ----------- implementation ------------ #
# --------------------------------------- #
    
def histogramEqualiztion(A):  
    
    # grab bins and count
    bins, count = makeBins(A)

    # get max_val for later use
    max_val = max(bins.keys())
    print(max_val)
    
    # construct probability bins
    prob = {}
    for key in bins:
        prob[key] = bins[key] / count
        
    # quantize probability bins according to: 
    # q(pixel intensity x) = number of pixels of pixel intensity x / total number of pixels
    total = 0
    quant = {}
    for key in list(sorted(prob.keys())):
        total += prob[key]
        quant[key] = total
    
    # adjust bins to quant(x) = quant(x) * max_val
    # normalize to largest possible pixel instensity
    for key in quant:
        quant[key] = int(quant[key] * max_val)
        
    # construct final matrix according to quantized-pixel pair
    # by getting correct assignment from input matrix
    M = []
    for row in A:
        curr = []
        for elem in row:
            curr.append(quant[elem])
        M.append(curr)
        
    return bins, M

def main(p):
    # read image and convert it from RGB to greyscale
    # then floor float values to int
    img = mpimg.imread(p)     
    A = rgb2gray(img).tolist()
    for i in range(0, len(A)):
        A[i] = list(map(int, A[i]))
    
    # get final image, M, from histEqualiztion function on input image A       
    bins, M = histogramEqualiztion(A)
    
    # convert to numpy array and change
    # from greyscale to rgb array
    ret = to_rgb(np.array(M))
    path = p[:len(p) - 4]
    
    # consturct histogram comparison
    makeHistogram(bins, path, 'b')
    B, dis = makeBins(M)
    makeHistogram(B, path, 'a')
    
    # send output to working directory
    end_path = "results//" + path + "_result"
    mpimg.imsave(end_path, ret.astype(np.uint8))
    return

if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except:
        path = "moon.bmp"
    main(path)