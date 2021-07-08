# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 19:49:45 2021

@author: JO20993
"""
import numpy as np
import BWSI_BuoyField

class Laser(object):
    def __init__(self):
        self.__MAX_RANGE = 200.0 # maximum range camera can see
        self.__MAX_ANGLE = 60.0 # field of view of camera (+/- MAX_ANGLE degrees)
                        
    def get_visible_buoys(self, pos, hdg, buoys):
        green_positions = []
        for G in self.green_buoys:
            rng = np.sqrt( (pos[0] - G[0])**2 +
                          (pos[1] - G[1])**2 )
            #print(f"rng = {rng}")
            if rng <= self.__MAX_RANGE:
                angle = np.degrees(np.arctan2(G[0]-pos[0], G[1]-pos[1])) - hdg
                if (np.abs(angle) < self.__MAX_ANGLE):
                    green_positions.append(G)
                
        red_positions = []
        for R in self.red_buoys:
            rng = np.sqrt( (pos[0] - R[0])**2 +
                          (pos[1] - R[1])**2 )
            if rng <= self.__MAX_RANGE:
                angle = np.degrees(np.arctan2(R[0]-pos[0], R[1]-pos[1])) - hdg
                if (np.abs(angle) < self.__MAX_ANGLE):
                    red_positions.append(R)
        
        return green_positions, red_positions