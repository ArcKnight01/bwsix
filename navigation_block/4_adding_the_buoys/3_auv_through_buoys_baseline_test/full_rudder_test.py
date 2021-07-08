# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 20:49:23 2021

@author: JO20993
"""
from BWSI_AUV import AUV

import numpy as np
import matplotlib.pyplot as plt

import hashlib
            
def corridor_check(A, G, R):
    GR = np.array((R[0]-G[0], R[1]-G[1]))
    GA = np.array((A[0]-G[0], A[1]-G[1]))
    RA = np.array((A[0]-R[0], A[1]-R[1]))
    
    GRGA = np.dot(GR, GA)
    GRRA = np.dot(GR, RA)

    return (GRGA*GRRA < 0)

def gate_check(B, A, G, R):
    
    if not (corridor_check(A, G, R) and corridor_check(B, G, R) ):
        return False
    
    GR = np.array((R[0]-G[0], R[1]-G[1], 0))
    GA = np.array((A[0]-G[0], A[1]-G[1], 0))
    GB = np.array((B[0]-G[0], B[1]-G[1], 0))
    
    GRGA = np.cross(GR, GA)
    GRGB = np.cross(GR, GB)
    
    return (GRGA[2]*GRGB[2] < 0)

final_heading_all = np.arange(30, 60, 0.25)
passed_flag = np.zeros((final_heading_all.shape), dtype=bool)

dt = .1
count = 0
good_angles = list()

for final_heading in final_heading_all:
    
    hdg = 90
    myAUV = AUV(latlon=(42.4, -171.3), heading=hdg, datum=(42.5,-171.5))

    x = [myAUV._AUV__position[0]]
    y = [myAUV._AUV__position[1]]
    t = [0]

    # place the buoys
    green_buoy = (myAUV._AUV__position[0] + 265, myAUV._AUV__position[1] + 175 )
    red_buoy = (myAUV._AUV__position[0] + 275, myAUV._AUV__position[1] + 165 )

    cmd = "ENGINE HALF AHEAD"
    reply = myAUV.engine_command(cmd)
    print(f"{cmd} : {reply}")
    
    done = False
    started_turn = finished_turn = False
    passed_gate = False
    while not done:
        
        prev_position = myAUV._AUV__position
        myAUV.update_state(dt)
        new_position = myAUV._AUV__position
        x.append( myAUV._AUV__position[0] )
        y.append(myAUV._AUV__position[1] )
        t.append(t[-1]+dt)

        passed_gate = gate_check(new_position,
                                 prev_position,
                                 green_buoy,
                                 red_buoy)
        
        done = (passed_gate or new_position[0]>(red_buoy[0]+10))
    
        if (not started_turn and myAUV._AUV__position[0] - x[0] >= 100):
            cmd = "LEFT FULL RUDDER"
            reply = myAUV.helm_command(cmd)
            print(f"{cmd} : {reply}")
            started_turn = True

        cmd = "MARK YOUR HEAD"
        reply = myAUV.helm_command(cmd)
        heading = float(reply.split()[1])
        print(f"{cmd} : {reply}")
    
        if (not finished_turn and heading <= final_heading):
            cmd = "RUDDER AMIDSHIPS"
            reply = myAUV.helm_command(cmd)
            print(f"{cmd} : {reply}")
            finished_turn = True
    
    passed_flag[count] = passed_gate
    if (passed_gate == True):
        good_angles.append(final_heading)
    count = count + 1

    if final_heading == 45.0:
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
        ax3.plot(green_buoy[0], green_buoy[1], 'go')
        ax3.plot(red_buoy[0], red_buoy[1], 'ro')
        ax3.set_xlabel('Relative Easting (m)')
        ax3.set_ylabel('Relative Northing (m)')

print(f"good angles = {good_angles}")