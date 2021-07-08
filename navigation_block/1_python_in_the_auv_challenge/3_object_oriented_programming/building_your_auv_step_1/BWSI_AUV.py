# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 20:23:11 2021

@author: JO20993
"""
class AUV(object):
    def __init__(self,                  
                 latlon=(0.0,0.0),
                 depth=0.0,
                 speed_knots=0.0,
                 heading=0.0,
                 rudder_position=0.0,
                 engine_speed='STOP',
                 engine_direction='AHEAD',
                 datum=(0.0,0.0)):

        self.latlon = latlon
        self.depth = depth
        self.speed_knots = speed_knots
        self.heading = heading
        self.rudder_position = rudder_position
        self.engine_state = (engine_speed, engine_direction)

        self.__datum = datum
                
    def set_rudder(self, rudder):
        self.rudder_position = rudder