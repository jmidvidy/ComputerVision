# -*- coding: utf-8 -*-
"""
EECS 332, Fall 2018
MP6: Hough Transformation
    
@author Jeremy Midvidy, jam658
"""

import sys
import numpy as np
import matplotlib.image as mpimg
import scipy.ndimage as ndimage
import CannyEdge # my canny edge detector from MP5
import math
import copy
import matplotlib.pyplot as plt
import cv2

def gray2rgb(I):
    I = I.tolist()
    out = []
    for row in I:
        curr = []
        for col in row:
            curr.append([col, col, col])
        out.append(curr)
    return np.array(out)

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

def saveImage(img, title):
    img = gray2rgb(img)
    mpimg.imsave(title, img.astype(np.uint8))
    return

def show_hough_line(img, accumulator, Dmax, save_path=None):
    
    thetas = list(range(-90, 90))
    rhos = list(range(-1*Dmax, Dmax + 2))
    accumulator = np.transpose(accumulator)
    
    fig, ax = plt.subplots(1, 2, figsize=(10, 10))
    ax[0].imshow(img, cmap=plt.cm.gray)
    ax[0].set_title('Edges')
    ax[0].axis('image')
    ax[1].imshow(
        accumulator, cmap='jet',
        extent=[thetas[-1], thetas[0], rhos[-1], rhos[0]])
    ax[1].set_aspect('equal', adjustable='box')
    ax[1].set_title('Hough transform')
    ax[1].set_xlabel('Angles (degrees)')
    ax[1].set_ylabel('Distance (pixels)')
    ax[1].axis('image')

    # plt.axis('off')
    if save_path is not None:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()
    return
    
def isLocalMax(r,c,A, dist):
    # form distxdist mask
    start_r = r - dist
    end_r = r + dist
    start_c = c - dist
    end_c = c + dist    
    mask = []
    for i in range(start_r, end_r+1):
        curr = []
        for j in range(start_c, end_c+1):
            try:
                val = A[i][j]
            except:
                val = 0
            curr.append(val)
        mask.append(curr)
    
    val = A[r][c]
    # if val is largest in mask
    # if >= for now
    for row in mask:
        for elem in row:
            if elem > val:
                return False
    
    #print(np.array(mask))
    return True

def houghTransform(A):
    
    """
    PARAM SPACE:
    
    THETA: 0, 1, 2, 3,......... 179  RHO
       [[                        ]   0
        [                        ]   1
        [                        ]   2
        [                        ]   3
        [                        ]   4
        [                        ]   5
                    .                .
                    .                .
                    .                .
        [                        ]   2Dmax + 1
        [                        ]]
    
    
        Each [theta][row] == theta - 90
                             row - Dmax
    """
    
    # --------------- INIT PARAM SPACE -------------- #
    # init Param Space
    # P[theta][p] = # votes in cache
    P = []
    thetas = list(range(-90, 90))
    R = len(A)
    C = len(A[0])
    Dmax = int(math.sqrt(R**2 + C**2))
    D = list(range(0, 2*Dmax + 2))
    for t in thetas:
        curr = []
        for d in D:
            curr.append(0)
        P.append(curr)
        
    #print(len(P[0]))
    #print(len(D))
    
    #print(thetas)
    #return 1,1,1,1
            
    # ------------- COUNT VOTES FOR EDGES ------------- #
    for x in range(0, C):
        for y in range(0, R):
            # if not an edge, continue
            if A[y][x] != 255:
                continue
            # is an edge, gather vote
            else:
                # for every possible value of theta [-90, 90]
                for theta in thetas:
                    # convert to radians
                    trad = (theta)*(math.pi / 180.0)
                    # gather rho
                    p = int(x*math.cos(trad) + y*math.sin(trad))
                    # increment corresponding bin
                    #print("theta:", theta + 90, "| p:", p+Dmax)
                    P[theta+90][p+Dmax] += 1
                    
    #print(P)
                
    # ------------- FIND LOCAL MAXIMA ------------- #
   # lm = [[39, 290], [56, 361], [57, 361], [110, 571], [114, 454], [114, 455], [177, 407]]

    lm = []
    lm_vals = {}
    global_max = [-1,-1]
    use_global_max = False
    max_tr1 = []
    max_tr2 = []

    threshold = 30
    for r in range(0, len(P)):
        for c in range(0, len(P[0])):
            # For each non-zero point in p,
            # See if it is the local max in a mask of size
            # THRESHOLDxTHRESHOLD
            if P[r][c] == 0:
                continue
            else:
                if use_global_max:
                    val = P[r][c]
                    if val > global_max[0]:
                        global_max[0] = val
                        max_tr1 = [r,c]
                    elif val > global_max[1]:
                        global_max[1] = val
                        max_tr2 = [r,c]
                else:
                    if isLocalMax(r,c, P, threshold):
                        lm.append([r,c])
                        if P[r][c] in lm_vals:
                            lm_vals[P[r][c]].append([r,c])
                        else:
                            lm_vals[P[r][c]] = [[r,c]]
         
    print("------------------------------------ LM ------------------------------------")
    for key in list(sorted(lm_vals.keys())):
        tt = lm_vals[key]
        print("\tVal:", key, "| [theta, rho]:", [tt])
    print("----------------------------------------------------------------------------")
        
    if use_global_max:
        lm = [max_tr1, max_tr2]
    
    # hardcode for now
    return np.array(P), Dmax, lm, lm_vals


    
    
def drawLines(lines, Dmax, img, vals):
        
    # gather top 10 row and thetas
    # input rows: 0 = -90
    # input cols: 0 = -Dmax
    
    #lines = [[-51+90, -71+Dmax]]
    
    # global max
    glob_max = True
    if glob_max:
        max_vals = list(sorted(vals.keys()))
        print(max_vals)
        
        lines = []
        max_vals_keys = max_vals[-4:]
        try:
            for key in max_vals_keys:
                lines.extend(vals[key])
        except: #only1 glob 
            lines = (vals[max_vals_keys])
            
    print(lines)
    
        
    for elem in lines:
        # update params to correct formatting from input matrix
        theta = elem[0] # need to convert from deg to radians
        theta = theta - 90
            
        #print(Dmax)
        rho   = elem[1] - (Dmax)  # <-- error here
                
        # y = mx + b
        def point(t, r, x):
            t = (t)*(math.pi / 180.0)
            t2 = r / math.sin(t)
            try:
                t1 = -1 * (1 / math.tan(t))
            except:
                return int(t2)
            #print("t1", t1, "t2", t2)                
            return int((x)*(t1) + t2)
        
        x1 = 1
        x2 = 1000
        y1 = point(theta, rho, x1)
        y2 = point(theta, rho, x2)
        cv2.line(img,(x1, y1),(x2,y2),(255,0,0),3)
    
    
    
    return img
    
    

def main(path):
    
    if "." in path:
        opath = path[:len(path)-4]
    
    out_path = "results/" + opath + "_"
    
    # (1) Read Image and convert it to Greyscale
    A = mpimg.imread(path)
    B = copy.deepcopy(A) # copy of RGB image
    A = rgb2gray(A)
    C = copy.deepcopy(A) # copy of Greyscale image
    #print(A)
    saveImage(A, out_path + "grey")
    
    # (2) Apply Gaussian Blur
    G = ndimage.filters.gaussian_filter(A, 1.2)
    saveImage(G, out_path + "Gauss_Blur")
    
    # (3) Get CannyEdge - used my CannyEdge detector from MP5
    E = CannyEdge.main(G)
    saveImage(E, out_path + "Canny_Edge")
    #print(grad)
    
    #print(E.tolist())
    #return
    
    # (4) Line Detection
    H, Dmax, lines, vals = houghTransform(E)
    show_hough_line(E, H, Dmax, save_path=out_path+'output.png')
    
    # (5) Draw Lines on Images
    L = drawLines(lines, Dmax, B, vals)
    #Out = gray2rgb(L)
    mpimg.imsave(out_path+"Lines", L.astype(np.uint8))
    return


if __name__ == '__main__':
    try:
        path = sys.argv[1]
    except:
        path1 = "input.bmp"
        path2 = "test.bmp"
        path3 = "test2.bmp"
    main(path1)
