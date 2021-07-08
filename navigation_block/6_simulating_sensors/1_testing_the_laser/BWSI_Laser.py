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
        self.__MAX_ANGLE = 85.0 # field of view of camera (+/- MAX_ANGLE degrees)
        self.__SENSOR_TYPE = 'RANGE_ANGLE'
        
    def get_visible_buoys(self, pos, hdg, buoy_field):
        angle_left = np.mod(hdg-self.__MAX_ANGLE+360, 360)
        angle_right = np.mod(hdg+self.__MAX_ANGLE, 360)
        G, R = buoy_field.detectable_buoys(pos, 
                                           self.__MAX_RANGE, 
                                           angle_left,
                                           angle_right,
                                           self.__SENSOR_TYPE)
                
        return G, R