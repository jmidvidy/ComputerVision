# -*- coding: utf-8 -*-
"""
EECS 332, MP2
Fall 2018
    
@author Jeremy Midvidy, jam658
"""

import sys
import imageio
import numpy as np
import matplotlib.image
import copy

def Erosion(A, SE, org):
    # go through image and use 'e' command to
    # recieve label from the inputted Structure Element
    out = []
    count = 0
    for r in range(0, len(A)):
        curr = []
        for c in range(0, len(A[0])):
            label = getCellLabel(A, r, c, SE, org, 'e')
            if label == 0 and A[r][c] == 1:
                count += 1
            curr.append(label)
        out.append(curr)
    return out, count

def Dilation(A, SE, org):
    # go through image and use 'd' command to
    # recieve label from the inputted Structure Element
    out = []
    count = 0
    for r in range(0, len(A)):
        curr = []
        for c in range(0, len(A[0])):
            label = getCellLabel(A, r, c, SE, org, 'd')
            if label == 1 and A[r][c] == 0:
                count += 1
            curr.append(label)
        out.append(curr)
    return out, count

def Opening(e, SE, org):
    return Dilation(e, SE, org)

def Closing(d, SE, org):
    return Erosion(d, SE, org)

def Boundary(A, e):
    # boundry = A - Erosion
    count = 0
    for r in range(0, len(A)):
        for c in range(0, len(A[0])):
            if A[r][c] == 1 and e[r][c] == 1:
                A[r][c] = 0
                count += 1
    return A, count


def getCellLabel(A, r, c, SE, og, func):

    # use extract rather than found as to enable better debugging
    # and appply same functin to dilation, erosion, boundry
    
    extract = []
    start_row = r - og[0]
    start_col = c - og[1]
    
    # extract MASK area from the image
    sr = copy.deepcopy(start_row)
    sc = copy.deepcopy(start_col)
    i = 0
    while i < len(SE):
        sc = copy.deepcopy(start_col)
        j = 0
        curr = []
        while j < len(SE[0]):
            if (sr < len(A) and sr > -1) and (sc < len(A[0]) and sc > -1):
                curr.append(A[sr][sc])
            else:
                curr.append(-1)
            j += 1
            sc += 1
        extract.append(curr)
        sr += 1
        i += 1
          
    # ----- process EROSION or DILATION ------ #
    # if func is EROSION; 1 for perfect match
    if func == 'e':
        for i in range(0, len(SE)):
            for j in range(0, len(SE[0])):
                if SE[i][j] == 1 and extract[i][j] == 1:
                    continue
                else:
                    return 0
        return 1
    # if func is DILATION; 1 for some match
    else:
        for i in range(0, len(SE)):
            for j in range(0, len(SE[0])):
                if SE[i][j] == 1 and extract[i][j] == 1:
                    return 1
        return 0    
    return


def writeProcess(h):
    for r in range(0, len(h)):
        for c in range(0, len(h[0])):
            if h[r][c] == 1:
                h[r][c] = 255
    return h
    

def writeImage(I,p, ind):
    I = writeProcess(I)
    d = {0:'erosion_image', 1:'dilaiton_image',2:'opening_image', 3:'closing_image', 4:'boundary_image'}
    ret = np.array(I)
    #np.savetxt("result", I,fmt='%s', delimiter=' ')
    end_path = "_" + d[ind] + "_result"
    end_path = "results//" + str(p)[:len(p)-4] + end_path
    matplotlib.image.imsave(end_path, ret.astype(np.uint8))
    return


def main(p):
    
    #read image, preprocess, and init SE
    A = imageio.imread(p).tolist()
    for r in range(0, len(A)):
        for c in range(0, len(A[0])):
            if A[r][c] == 255:
                A[r][c] = 1
                
    SE = [[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]]
    org = [1,2]
    
    # main func calls to gather each desired morphological image translation
    erosion_image, e_count = Erosion(copy.deepcopy(A), SE, org)
    dilaiton_image, d_count = Dilation(copy.deepcopy(A), SE, org)
    opening_image, o_count = Opening(copy.deepcopy(erosion_image), SE, org)
    closing_image, c_count = Closing(copy.deepcopy(dilaiton_image), SE, org)
    boundary_image, b_count = Boundary(copy.deepcopy(A), copy.deepcopy(erosion_image))
        
    # adjust opening and closing counts
    o_count = o_count + e_count
    c_count = c_count + d_count
    
    # print counts to commnad line
    print("----------------------------------------------------------------------------")
    print("Running erosion, dilation, opening, closing, and boundary on " + str(p) + ".")
    print("----------------------------------------------------------------------------")
    print("During erosion : " + str(e_count) + " total changes were made.")
    print("During dilation: " + str(d_count) + " total changes were made.")
    print("During opening : " + str(o_count) + " total changes were made.")
    print("During closing : " + str(c_count) + " total changes were made.")
    print("During boundary: " + str(b_count) + " total changes were made.")
    print("----------------------------------------------------------------------------")
    
    # write each image to picture file stored in "\\results
    res = [erosion_image, dilaiton_image, opening_image, closing_image, boundary_image]
    i = 0
    for elem in res:
        writeImage(elem,p, i)
        i += 1
    
    return


if __name__ == '__main__':
    #path = "gun.bmp"
    path = sys.argv[1]
    main(path)
    
    
"""
    DILATION TEST:
     
    INPUT:
    
    A = [
       # 0  1  2  3  4  5  6  7  8  9  10    
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #0
        [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0], #1
        [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0], #2
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], #3
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], #4
        [0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], #5
        [0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], #6
        [0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], #7
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0], #8
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0], #9
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #10
    ]
    
    OUTPUT:
        
        [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]]
        
    ---------------------------------------------------
    
    EROSION TEST
    
    INPUT:
        
    A = [
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    
    OUTPUT:
        
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        
        
"""

