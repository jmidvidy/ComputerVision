# -*- coding: utf-8 -*-
"""
EECS 332, MP1
Fall 2018
    
@author Jeremy Midvidy, jam658

"""

import sys
import imageio
import collections
import numpy as np
import matplotlib.image


# ----- union find IMPLEMENTATION ------- #
def indices_dict(lis):
    d = collections.defaultdict(list)
    for i,(a,b) in enumerate(lis):
        d[a].append(i)
        d[b].append(i)
    return d

def disjoint_indices(lis):
    d = indices_dict(lis)
    sets = []
    while len(d):
        que = set(d.popitem()[1])
        ind = set()
        while len(que):
            ind |= que 
            que = set([y for i in que 
                         for x in lis[i] 
                         for y in d.pop(x, [])]) - ind
        sets += [ind]
    return sets

def union(lis):
    return [set([x for i in s for x in lis[i]]) for s in disjoint_indices(lis)]

# --------- Labeling Algorithm ----------------- #
    
def main(p):
    #read image to rgb matrix
    A = imageio.imread(p).tolist()
    
    # Preprocces matrix
    for r in range(0, len(A)):
        for c in range(0, len(A[0])):
            if A[r][c] == 255:
                A[r][c] = -1
    
    # -------------- First Pass - Gather Connected Components ----------------- #
    
    # initialie label counter, count, and equivalence matrix, E
    count = 1
    E = []
    
    # small helper used for maintaining E
    def eHelper(a):
        for elem in E:
            if a in elem:
                return True
        return False
    
    for r in range(0, len(A)):
        for c in range(0, len(A[0])):
            curr = A[r][c]
            if curr == -1: # not background
                
                # ---- gather up and right values ---- #
                up = None
                left = None
                # use try and except for out of bounds errors
                try:
                    if A[r-1][c] != 0:
                        up = A[r-1][c]
                except:
                    pass
                try:
                    if A[r][c-1] != 0:
                        left = A[r][c-1]
                except:
                    pass
                
                # ----- Add sequential labeling technique --- #
                # - curr cell has cell-up and cell-left:
                #       - label curr cell min(up,left)
                #       - if [min(up,left),max(up,left)] is not in E, add it
                if up and left:
                    A[r][c] = min(up,left)
                    if left != up: #add equivalence
                        update = [min(left,up), max(left,up)]
                        if update not in E:
                            E.append(update)
                
                # Only up 
                elif up:
                    A[r][c] = up
                            
                # Only left
                elif left:
                    A[r][c] = left
                    
                # No up or left, so increase labels
                else:
                    A[r][c] = count
                    # potential for isolated pixel
                    if [count] not in E and eHelper(count):
                        E.append([count,count])
                    count += 1
                        
                    
    #np.savetxt("result", A,fmt='%s', delimiter=' ')
    
    # ------------ Second Pass - Renumbering tables using the E-table ----------- #
    #   - Relabel cell with lowest equivalent label
    
    
    # use UNION-FIND to resolve equivalences
    labels_set = union(E)
        
    # map sets to min labels
    mins = []
    for elem in labels_set:
        mins.append(min(elem))  
    mins = list(sorted(mins))
    
    # map labels set to min_value per each label
    labels = {}
    for i in range(0, len(mins)):
        for elem in labels_set:
            if mins[i] in elem:
               labels[i+1] = elem
               break
           
    # small helper to PULL the correct label from a given
    # cell value --> use for making second pass
    def getLabel(p):
        for key in labels:
            if p in labels[key]:
                return key
            
    # map labels to unique colors
    diff = (255//max(labels.keys()))
    
    labels_map = {}
    val = diff
    for key in labels:
        labels_map[key] = [val]
        val += diff
        
    print(labels_map)
    
    # make second pass through array to re-label image
    for r in range(0, len(A)):
        for c in range(0, len(A[0])):
            if A[r][c] != 0:
                A[r][c] = labels_map[getLabel(A[r][c])][0]
                
    res = np.array(A)
    matplotlib.image.imsave("results//"  + str(p)[:len(p)-4] + "_result", res.astype(np.uint8))
    
    
    #np.savetxt("result", A,fmt='%s', delimiter=' ')
    res = np.array(A)
    matplotlib.image.imsave("results//"  + str(p)[:len(p)-4] + "_result", res.astype(np.uint8))
    
    num = max(labels.keys())

    # save image
    
    # Command line output
    print("\nMy Program identified " + str(num) + " labels.")
    print("Classification Image is stored in the results folder as " + str(p)[:len(p)-4] + "_TextResult.txt\n")
    print("Here are the equivalnces found on the first pass:")
    print(E)
    print("\n")
    print("Here is the union-find of equivalnces organized by labels in ascending order:")
    print(labels)
    print("\n")
    print("Here are the RGB colors assigned to each label in the result image:")
    print(labels_map)
    
    return

if __name__ == '__main__':
    #path = sys.argv[1]  # <-- change back before submitting
    path = "test.bmp"
    main(path)


