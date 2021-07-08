# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 20:49:23 2021

@author: JO20993
"""
from BWSI_AUV import AUV

import numpy as np
import matplotlib.pyplot as plt

speed_list = ("SLOW", "HALF", "FULL")
rudder_list = ("RIGHT STANDARD RUDDER", "RIGHT FULL RUDDER", "HARD RIGHT RUDDER")
hdg = 0
for speed in speed_list:
    for rudder_cmd in rudder_list:
        print(f"\nCreating AUV instance at heading = {hdg}")
        myAUV = AUV(latlon=(42.4, -171.3), heading=hdg, datum=(42.5,-171.5))
        start_x = myAUV._AUV__position[0]
        start_y = myAUV._AUV__position[1]
        x = [0]
        y = [0]
        t = [0]
            
        dt = 1
        positions = list()
        
        cmd = f"ENGINE {speed} AHEAD"
        reply = myAUV.engine_command(cmd)
        print(f"{cmd} : {reply}")

        cmd = rudder_cmd
        reply = myAUV.helm_command(cmd)
        print(f"{cmd} : {reply}")
        for i in range(300):
            myAUV.update_state(dt)
            
            positions.append(myAUV._AUV__position[0])
            positions.append(myAUV._AUV__position[1])
            x.append(myAUV._AUV__position[0] - start_x)
            y.append(myAUV._AUV__position[1] - start_y)
            t.append(t[-1]+dt)
         
        print(f"TURNING DIAMETER: {np.max(np.array(x))}")    
    
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
    