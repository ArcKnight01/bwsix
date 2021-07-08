# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 20:49:23 2021

@author: JO20993
"""
from BWSI_AUV import AUV
from BWSI_BuoyField import BuoyField

import numpy as np
import matplotlib.pyplot as plt

import hashlib

def my_hash(data):
    if not isinstance(data, str):
        d2 = data.tobytes()
    else:
        d2 = data.encode("UTF-8")
        
    return hashlib.md5(d2).hexdigest()

def round_and_report(data, n):
    d2 = np.rint(data * 10**n).astype(np.int32)
    return my_hash(d2)

datum = (42.5, -171.5)
myAUV = AUV(latlon=(42.4, -171.3), heading=90, datum=datum)

# place the buoys
green_buoy = []
red_buoy = []
nGates = 10

random_samples = [0.60597828, 0.73336936, 0.13894716, 0.31267308, 0.99724328,
                  0.12816238, 0.17899311, 0.75292543, 0.66216051, 0.78431013]
for i in range(nGates):
    xdist = (i+1)*50
    ydist = (random_samples[i] - 0.5) * 20.0
    green_buoy.append((myAUV._AUV__position[0] + xdist, myAUV._AUV__position[1] + ydist + 5 ))
    red_buoy.append((myAUV._AUV__position[0] + xdist, myAUV._AUV__position[1] + ydist - 5 ))

buoyField = BuoyField(datum,
                      green_buoys=green_buoy,
                      red_buoys=red_buoy,
                      position_style='P')

pos_G, pos_R = myAUV.read_laser()
p = np.concatenate((pos_G, pos_R))
p = p.reshape((p.size,))
print(f"LASER TEST HASH is {round_and_report(p,5)}")
              

