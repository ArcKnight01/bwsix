# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 20:47:22 2021

@author: JO20993
"""
from BWSI_AUV import AUV

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
    
hdglist = (0, 90, 64)
hashes = ("4f34f47e44205463dd42d6108b3bf9da", "fa71ee3508d722fc96ace5843107afe1", "?")
latlon_hashes = ("62e8c79734829ac93feb7d0495f0ac91", "9a14c9be13ff2467e5e62b7c0054fbb3", "?")
count = 0
for hdg in hdglist:
    print(f"\nCreating AUV instance at heading = {hdg}")
    myAUV = AUV(latlon=(42.4, -171.3), heading=hdg, datum=(42.5,-171.5))
    start_x = myAUV._AUV__position[0]
    start_y = myAUV._AUV__position[1]
    x = [0]
    y = [0]
    t = [0]
        
    dt = 1
    positions = list()
    
    cmd = "ENGINE HALF AHEAD"
    reply = myAUV.engine_command(cmd)
    print(f"{cmd} : {reply}")
    cmd = "RIGHT 10 DEGREES RUDDER"
    reply = myAUV.helm_command(cmd)
    print(f"{cmd} : {reply}")
    for i in range(300):
        myAUV.update_state(dt)
        
        positions.append(myAUV._AUV__position[0])
        positions.append(myAUV._AUV__position[1])
        x.append(myAUV._AUV__position[0] - start_x)
        y.append(myAUV._AUV__position[1] - start_y)
        t.append(t[-1]+dt)
                
    this_hash = round_and_report(np.array(positions), 3)
    print(f"TEST {count+1} HASH: {this_hash}")
    print(f"TEST {count+1} LATLON HASH: {round_and_report( np.array(myAUV._AUV__latlon), 3)}")
    
    if (hashes[count] != "?"):
        assert (this_hash == hashes[count]), f"Failed with heading = {hdg}"
    if (latlon_hashes[count] != "?"):
        assert (this_hash == hashes[count]), f"Failed with heading = {hdg}"

    count = count + 1

    fig = plt.figure()
    ax1 = fig.add_subplot(2,2,1)
    ax1.plot(t, x)
    ax1.set_xlabel('Time (sec)')
    ax1.set_ylabel('Relative Easting (m)')
    ax2 = fig.add_subplot(2,2,3)
    ax2.plot(t, y)
    ax2.set_xlabel('Time (sec)')
    ax2.set_ylabel('Relative Northing (m)')
    ax3 = fig.add_subplot(2,2,(2,4))
    ax3.plot(x, y)
    ax3.set_xlabel('Relative Easting (m)')
    ax3.set_ylabel('Relative Northing (m)')
    plt.show()