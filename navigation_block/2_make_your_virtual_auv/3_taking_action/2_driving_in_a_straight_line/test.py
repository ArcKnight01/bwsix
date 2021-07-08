# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 20:14:57 2021

@author: JO20993
"""
from BWSI_AUV import AUV

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
    
hdglist = (0, 90, 64)
hashes = ("0da1e9ce98f9f97bca03bb4b89d366da", "30f099a58eab414a4a83e893b0077d02", "?")
latlon_hashes = ("825933fddd6074af55e8077b76e73231", "936290882160b242611ccc5e76569771", "?")
count = 0
for hdg in hdglist:
    myAUV = AUV(latlon=(42.4, -171.3), heading=hdg, datum=(42.5,-171.5))
    
    dt = 60
    positions = list()
    cmd = "ENGINE HALF AHEAD"
    reply = myAUV.engine_command(cmd)
    print(f"{cmd} : {reply}")
    for i in range(10):
        myAUV.update_state(dt)
        positions.append(myAUV._AUV__position[0])
        positions.append(myAUV._AUV__position[1])
        
    this_hash = round_and_report(np.array(positions), 3)
    print(f"TEST {count+1} HASH: {this_hash}")
    print(f"TEST {count+1} LATLON HASH: {round_and_report( np.array(myAUV._AUV__latlon), 3)}")
    
    if (hashes[count] != "?"):
        assert (this_hash == hashes[count]), f"Failed with heading = {hdg}"

    count = count + 1  