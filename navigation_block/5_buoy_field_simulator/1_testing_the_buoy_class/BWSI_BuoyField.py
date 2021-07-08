# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 12:39:28 2021

@author: JO20993
"""

import sys

import numpy as np
import matplotlib.pyplot as plt

import utm

## Utility functions
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

class Buoy(object):
    def __init__(self,
                 datum,
                 position=[],
                 latlon=[]):
                
        assert (latlon or position) and not (latlon and position), "Buoy.__init__: Must define either latlon or position!"

        self.__datum = datum
        # returns easting, northing, section #, section letter
        self.__datum_position = utm.from_latlon(self.__datum[0], self.__datum[1])
        
        
        if not latlon:
            self.__position = position
            
            # calculate its latlon
            self.__latlon = utm.to_latlon(self.__position[0] + self.__datum_position[0],
                                          self.__position[1] + self.__datum_position[1],
                                          self.__datum_position[2],
                                          self.__datum_position[3])

        else:
            self.__latlon = latlon
            position = utm.from_latlon(self.__latlon[0],
                                       self.__latlon[1],
                                       force_zone_number=self.__datum_position[2],
                                       force_zone_letter=self.__datum_position[3])
            self.__position = (position[0]-self.__datum_position[0],
                               position[1]-self.__datum_position[1])
                    
        
    def update_position(self, newpos):
        postn = (newpos[0], newpos[1], self.__position[2], self.__position[3])
        self.__position = postn
        self.__latlon = utm.to_latlon(self.__position[0] + self.__datum_position[0],
                                      self.__position[1] + self.__datum_position[1],
                                      self.__datum_position[2],
                                      self.__datum_position[3])
                 
    def update_latlon(self, newlatlon):
        self.__latlon = newlatlon
        self.__position = utm.from_latlon(self.__latlon[0],
                                          self.__latlon[1],
                                          force_zone_numer=self.__datum_position[2],
                                          force_zone_letter=self.__datum_position[3])
            
    # accessor functions
    def get_position(self):
        return self.__position
    
    def get_latlon(self):
        return self.__latlon
        

## Buoy field class
class BuoyField(object):
    def __init__(self,
                 datum,
                 green_buoys = [],
                 red_buoys = [],
                 position_style='P'):
        
        # position_style = 'P' for position, 'L' for latlon
        self.__datum = datum
        self.__datum_position = utm.from_latlon(self.__datum[0], self.__datum[1])

        self.add_buoy_gates(green_buoys, red_buoys, position_style)
    
    def add_buoy_gates(self, green, red, position_style='P'):
        
        assert len(green) == len(red), "Should be equal number of green and red buoys"
        assert position_style=='P' or position_style=='L', f"Unknown position style {position_style}"
        self.__green_buoys = list()
        self.__red_buoys = list()
        for i in range(len(green)):
            if position_style == 'P':
                self.__green_buoys.append(Buoy(self.__datum, position=green[i]))
                self.__red_buoys.append(Buoy(self.__datum, position=red[i]))
            else:
                self.__green_buoys.append(Buoy(self.__datum, latlon=green[i]))
                self.__red_buoys.append(Buoy(self.__datum, latlon=red[i]))

        self.gates_passed = np.zeros( (len(red),), dtype=bool)
        
    def get_buoy_positions(self):
        G = list()
        R = list()
        for green in self.__green_buoys:
            G.append(green.get_position())
        for red in self.__red_buoys:
            R.append(red.get_position())
        return (G,R)
    
    def get_buoy_latlon(self):
        G = list()
        R = list()
        for green in self.__green_buoys:
            G.append(green.get_latlon())
        for red in self.__red_buoys:
            R.append(red.get_latlon())
        return (G,R)
        
        
    def check_buoy_gates(self, prev_pos, new_pos):
        
        for i in range(self.gates_passed.size):
            if (self.gates_passed[i] == False):
                self.gates_passed[i] = gate_check(new_pos, 
                                                  prev_pos, 
                                                  self.__green_buoys[i].get_position(),
                                                  self.__red_buoys[i].get_position())
                            
    def clearedBuoys(self):
        return np.count_nonzero(self.gates_passed)
    
    def isClear(self):
        return (np.count_nonzero(self.gates_passed) == self.gates_passed.size)
        
    # return all the buoys in the field that are within max_range of the platform,
    # and between angle_left and angle_right (in absolute bearing)
    def detectable_buoys(self, position, max_range, angle_left, angle_right):
        # note: angle_left and angle_right are mod 360
        G = list()
        for green in self.green_buoys:
            rng = np.sqrt( (position[0]-green[0])**2 + (position[1]-green[1])**2 )
            if rng < max_range:
                # now check if it's within the angle range atan2 returns -pi:pi
                angl = np.mod(np.degrees(np.arctan2(green[0]-position[0], green[1]-position[1]) ), 360)
                if (angle_left < angle_right):
                    if ( angl >= angle_left and angl <= angle_right ):
                        G.append(green)
                else:
                    if ( angl >= angle_left or angl <= angle_right):
                        G.append(green)
                    
        R = list()
        for red in self.red_buoys:
            rng = np.sqrt( (position[0]-red[0])**2 + (position[1]-red[1])**2 )
            if rng < max_range:
                # now check if it's within the angle range atan2 returns -pi:pi
                angl = np.mod(np.degrees(np.arctan2(red[0]-position[0], red[1]-position[1]) ), 360)
                if (angle_left < angle_right):
                    if ( angl >= angle_left and angl <= angle_right ):
                        R.append(red)
                else:
                    if ( angl >= angle_left or angl <= angle_right):
                        R.append(red)
        
        return G, R
        
    def show_field(self):
        for i in range(len(self.__green_buoys)):
            Gpos = self.__green_buoys[i].get_position()
            plt.plot( Gpos[0], Gpos[1], 'go')
            Rpos = self.__red_buoys[i].get_position()
            plt.plot( Rpos[0], Rpos[1], 'ro')

        plt.show()

    ## return if all the gates are cleared        
    def all_gates_cleared(self):
        if all(self.gates_passed == True):
            return True
        else:
            return False