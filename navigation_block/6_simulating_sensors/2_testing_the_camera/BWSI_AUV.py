# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 20:23:11 2021

@author: JO20993
"""
import numpy as np
import utm

from BWSI_Laser import Laser
from BWSI_Camera import Camera

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
        if ( ( engine_speed != "STOP") and (engine_speed != "SLOW") 
            and (engine_speed != "HALF") and (engine_speed != "FULL") ):
            raise ValueError
        if ( (engine_direction != "AHEAD") and (engine_direction != "ASTERN") ):
            raise ValueError

        self.__engine_state = (engine_speed, engine_direction)
        
        # helm command, conning order
        self.__rudder_position = rudder_position
        
        ######
        ## state components that we observe but don't directly control
        self.__latlon = latlon
        self.__depth = depth
        self.__speed_knots = speed_knots
        self.__speed_mps = speed_knots * 0.514444
        self.__heading = heading
        
        ######
        ## sensors
        self.__laser = Laser()
        self.__camera = Camera()
        
        ######################################
        ## external information and parameters
        self.__datum = datum
        self.__datum_position = utm.from_latlon(self.__datum[0], self.__datum[1])
        self.__position = self.__get_local_position()

        ## characteristic of vehicle; should be overwritten by a subclass
        self.__MAX_SPEED_KNOTS = 10
        self.__HARD_RUDDER_DEG = 35
        self.__FULL_RUDDER_DEG = 30
        self.__STANDARD_RUDDER_DEG = 15
        self.__MAX_TURNING_RATE = 11.67

    ##############################################################
    ## User request functions
    # update the vehicle state, dt seconds have passed since last update
    def update_state(self, dt):
        delta_heading = self.__MAX_TURNING_RATE * (self.__rudder_position / self.__HARD_RUDDER_DEG) * (self.__speed_knots / self.__MAX_SPEED_KNOTS) * dt
        final_heading = np.mod(self.__heading + delta_heading + 360.0, 360.0)
        avg_heading = np.mod( self.__heading + delta_heading/2.0 + 360.0, 360.0)
        
        # just march forward
        x = self.__position[0] + self.__speed_mps * dt * np.sin( np.radians(avg_heading) )
        y = self.__position[1] + self.__speed_mps * dt * np.cos( np.radians(avg_heading) )
        self.__position = (x,y)
        self.__latlon = utm.to_latlon(self.__position[0] + self.__datum_position[0],
                                      self.__position[1] + self.__datum_position[1],
                                      self.__datum_position[2],
                                      self.__datum_position[3])
        
        self.__heading = final_heading
                        
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
            speed_knots = 0.25 * self.__MAX_SPEED_KNOTS
        elif (words[1] == "HALF"):
            speed_knots = 0.5 * self.__MAX_SPEED_KNOTS
        elif (words[1] == "FULL"):
            speed_knots = self.__MAX_SPEED_KNOTS
        else:
            return "COMMAND"
        
        # interpret the engine direction term
        new_engine_direction = words[2]
        if ( (words[2] != "AHEAD") and (words[2] != "ASTERN") ):
            return "COMMAND"
        
        if (words[2] != self.__engine_state[1]):
            self.__heading = np.mod(self.__heading + 180, 360)
            
        self.__engine_state = (new_engine_speed, new_engine_direction)
        self.__speed_knots = speed_knots
        self.__speed_mps = self.__speed_knots * 0.514444
        
        return command
    
    def helm_command(self, command):
        ### Available commands:
        ## Helm commands
        # {RIGHT, LEFT} {#} DEGREES RUDDER
        # {RIGHT, LEFT} STANDARD RUDDER (standard = 15 degrees)
        # {RIGHT, LEFT} FULL RUDDER (full = 30 degrees)
        # HARD {RIGHT, LEFT} RUDDER (= 35 degrees)
        # INCREASE YOUR RUDDER TO {#} DEGREES
        # RUDDER AMIDSHIPS (= 0 degrees)
        # SHIFT YOUR RUDDER
        # MARK YOUR HEAD
        # HOW IS YOUR RUDDER
        # KEEP HER SO
        command = command.upper()
        cmd = command.split()

        if (len(cmd) < 2):
            # invalid command, request a new one
            return "COMMAND"

        if (command == "KEEP HER SO"):
            # do nothing
            return self.__reply_success(command)
        elif (command == "HOW IS YOUR RUDDER"):
            if (self.__rudder_position == 0):
                reply = "RUDDER AMIDSHIPS"
            else:
                direction = "RIGHT"
                if (self.__rudder_position < 0):
                    direction = "LEFT"
                reply = f"RUDDER {direction} {np.abs(self.__rudder_position):.1f} DEGREES"
            return reply
        elif (command == "MARK YOUR HEAD"):
            reply = f"HEADING {self.__heading:.1f} DEGREES"
            return reply
        elif (command == "SHIFT YOUR RUDDER"):
            self.__rudder_position = -self.__rudder_position
            return self.__reply_success(command)
        elif (command == "RUDDER AMIDSHIPS"):
            self.__rudder_position = 0
            return self.__reply_success(command)
        elif (cmd[0] == "INCREASE"):
            return self.__parse_increase_command(command)
        elif (cmd[0] == "HARD"):
            return self.__parse_hard_command(command)
        else:
            return self.__parse_turn_command(command)
        
        
    ## accessor functions
    def get_position(self):
        return self.__position
            
    ## sensors    
    def read_laser(self):
        g, r = self.__laser.get_visible_buoys(self.__position, self.__heading)
        
        return g, r
    
    def read_camera(self):
        g, r = self.__camera.get_visible_buoys(self.__position, self.__heading)

        return g, r

    #
    ## done user requests
    ################################################################        

    ##################################################################
    ## private "helper" functions
    #
    def __parse_turn_command(self, command):
        cmd = command.split()
        
        if (len(cmd)<3):
            return "COMMAND"
        
        if (cmd[0] == "RIGHT"):
            mult = 1
        elif (cmd[0] == "LEFT"):
            mult = -1
        else:
            return "COMMAND"
        
        if (cmd[1] == "FULL"):
            if (cmd[2] == "RUDDER"):
                deg = self.__FULL_RUDDER_DEG
            else:
                return "COMMAND"
        elif (cmd[1] == "STANDARD"):
            if (cmd[2] == "RUDDER"):
                deg = self.__STANDARD_RUDDER_DEG
            else:
                return "COMMAND"
        else:
            if (len(cmd) != 4):
                return "COMMAND"
            
            if (cmd[2]=="DEGREES" and cmd[3]=="RUDDER"):
                deg = int(cmd[1])
            else:
                return "COMMAND"
            
            if (deg > self.__FULL_RUDDER_DEG):
                return "COMMAND"
        
        #made it through
        self.__rudder_position = mult*deg
        return self.__reply_success(command)
        
        
    def __parse_increase_command(self, command):
        cmd = command.split()

        if not (cmd[1]=="YOUR" and cmd[2]=="RUDDER" and cmd[3]=="TO"):
            # improper command format
            return "COMMAND"
        
        if (self.__rudder_position == 0):
            # ambiguous which direction to turn
            return "COMMAND"
        
        deg = int(cmd[4])
        
        if (deg > self.__FULL_RUDDER_DEG):
            # increasing too much
            return "COMMAND"
        
        if (deg < np.abs(self.__rudder_position)):
            # this is not increasing the rudder
            return "COMMAND"
        
        # looks like a valid command
        self.__rudder_position = np.sign(self.__rudder_position)*deg
        return self.__reply_success(command)
    
    def __parse_hard_command(self, command):
        cmd = command.split()
        
        if (len(cmd)<3):
            return "COMMAND"
        
        if not (cmd[2] == "RUDDER"):
            return "COMMAND"
        
        if (cmd[1] == "RIGHT"):
            self.__rudder_position = self.__HARD_RUDDER_DEG
            return self.__reply_success(command)
        elif (cmd[1] == "LEFT"):
            self.__rudder_position = -self.__HARD_RUDDER_DEG
            return self.__reply_success(command)
        else:
            return "COMMAND"
        
    def __reply_success(self, cmd):
        reply_string = cmd + " AYE AYE"
        return reply_string
    
    def __get_local_position(self):
        # check that datum is in the same UTM zone, if not, shift datum
        local_pos = utm.from_latlon(self.__latlon[0],
                                    self.__latlon[1],
                                    force_zone_number=self.__datum_position[2],
                                    force_zone_letter=self.__datum_position[3])
        
        return (local_pos[0]-self.__datum_position[0], local_pos[1]-self.__datum_position[1])
    
    def __update_latlon(self):
        self.__latlon = utm.to_latlon(self.__position + self.__datum_position)
                
    #    
    ## done private helpers
    ##################################