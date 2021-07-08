# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 00:24:38 2021

@author: JO20993
"""

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(2021)

Ntest = 25
incount = 0
# make Ntest random A, G, R positions
A = 100.0*np.random.random((Ntest,2)) - 50.0
G = 100.0*np.random.random((Ntest,2)) - 50.0
R = 100.0*np.random.random((Ntest,2)) - 50.0

for i in range(Ntest):
    GR = np.array((R[i,0]-G[i,0], R[i,1]-G[i,1]))
    GA = np.array((A[i,0]-G[i,0], A[i,1]-G[i,1]))
    RA = np.array((A[i,0]-R[i,0], A[i,1]-R[i,1]))
    
    GRGA = np.dot(GR, GA)
    GRRA = np.dot(GR, RA)
    
    if (GRGA*GRRA < 0):
        print(f"{i}: in the corridor ( {GRGA}, {GRRA} )")
        incount += 1
    
    doPlot = False
    if (doPlot):
        plt.plot(R[i,0], R[i,1], 'ro')
        plt.plot(G[i,0], G[i,1], 'go')
        plt.plot(A[i,0], A[i,1], 'yo')
        plt.axis('equal')
        plt.show()
    
    x=1

print(f"{incount} of {Ntest}")