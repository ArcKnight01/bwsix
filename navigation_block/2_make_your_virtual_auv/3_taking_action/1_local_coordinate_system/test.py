# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 20:11:23 2021

@author: JO20993
"""
from BWSI_AUV import AUV

import sys
import numpy as np

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

def get_data_array(auv):
    ret = np.array( [auv._AUV__latlon[0],
                     auv._AUV__latlon[1],
                     auv._AUV__depth,
                     auv._AUV__heading,
                     auv._AUV__rudder_position,
                     auv._AUV__speed_knots,
                     auv._AUV__datum[0],
                     auv._AUV__datum[1],
                     auv._AUV__datum_position[0],
                     auv._AUV__datum_position[1],
                     auv._AUV__position[0],
                     auv._AUV__position[1],
                     auv._AUV__MAX_SPEED_KNOTS] )
    return ret

def get_engine_state(auv):
    return auv._AUV__engine_state[0] + auv._AUV__engine_state[1]    

myAUV = AUV(latlon=(42.4, -171.3), datum=(42.4, -171.3))
assert (myAUV._AUV__position[0]==0 and myAUV._AUV__position[1]==0 ), "ERROR when latlon == datum"

myAUV = AUV(latlon=(42.4, -171.3), datum=(42.5,-171.5))
data = get_data_array(myAUV)
print(f"TEST 1 DATA: {round_and_report(data, 3)}")

myAUV = AUV(latlon=(1.4, 12.3), datum=(42.5,-171.5))
data = get_data_array(myAUV)
print(f"TEST 2 DATA: {round_and_report(data, 3)}")