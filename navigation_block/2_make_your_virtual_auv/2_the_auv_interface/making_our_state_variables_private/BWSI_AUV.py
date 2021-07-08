# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 20:23:11 2021

@author: JO20993
"""
import numpy as np

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

        ####
        ## state components that we control
        # engine orders
        #sanity check
        self.__engine_state = (engine_speed, engine_direction)
        
        # helm command, conning order
        self.__rudder_position = rudder_position
        
        ######
        ## state components that we observe but don't directly control
        self.__latlon = latlon
        self.__depth = depth
        self.__speed_knots = speed_knots
        self.__heading = heading
        
        ######################################
        ## external information and parameters
        self.__datum = datum        

        ## should be overwritten by a subclass
        self.__MAX_SPEED_KNOTS = 10
        self.__MAX_RUDDER_DEG = 30
                        
    def engine_command(self, command):
        # break into words & force upper case
        words = command.upper().split()
        
        # sanity check on input
        if ( (len(words)<2) or 
            ( words[0] != "ENGINE") ):
            return "COMMAND"
                   
        # interpret the engine speed term
        new_engine_speed = words[1]
        if (words[1] == "STOP"):
            self.__speed_knots = 0
            new_engine_direction = self.__engine_state[1]
            self.__engine_state = (new_engine_speed, new_engine_direction)
            return command
        elif (words[1] == "SLOW"):
            self.__speed_knots = 0.25 * self.__MAX_SPEED_KNOTS
        elif (words[1] == "HALF"):
            self.__speed_knots = 0.5 * self.__MAX_SPEED_KNOTS
        elif (words[1] == "FULL"):
            self.__speed_knots = self.__MAX_SPEED_KNOTS
        else:
            return "COMMAND"
        
        # interpret the engine direction term
        new_engine_direction = words[2]
        if (words[2] != self.__engine_state[1]):
            self.__heading = np.mod(self.__heading + 180, 360)
            
        self.__engine_state = (new_engine_speed, new_engine_direction)
        
        return command