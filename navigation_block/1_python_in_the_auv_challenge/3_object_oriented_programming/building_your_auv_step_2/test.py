# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 19:53:09 2021

@author: JO20993
"""
from BWSI_AUV import AUV

import numpy as np

import hashlib
    
def my_hash(data):
    if not isinstance(data, str):
        d2 = data.tobytes()
    return hashlib.md5(d2).hexdigest()

def round_and_report(data, n):
    d2 = np.rint(data * 10**n).astype(np.int32)
    return my_hash(d2)


myAUV = AUV(latlon=(42.4, -171.3),
            depth=113.1,
            heading=64,
            rudder_position=12,
            speed_knots=3,
            engine_speed='FULL',
            engine_direction='ASTERN',
            datum=(42.5,-171.5))

data_array = np.array( [myAUV.latlon[0],
                        myAUV.latlon[1],
                        myAUV.depth,
                        myAUV.heading,
                        myAUV.rudder_position,
                        myAUV.speed_knots,
                        myAUV._AUV__datum[0],
                        myAUV._AUV__datum[1] ] )

print(f"MD5 hash: {round_and_report(data_array,3)}")