# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 19:57:30 2021

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

def get_data_array(auv):
    ret = np.array( [auv.latlon[0],
                     auv.latlon[1],
                     auv.depth,
                     auv.heading,
                     auv.rudder_position,
                     auv.speed_knots,
                     auv._AUV__datum[0],
                     auv._AUV__datum[1],
                     auv._AUV__MAX_SPEED_KNOTS] )
    return ret

def get_engine_state(auv):
    ret = auv.engine_state[0] + auv.engine_state[1]
    
    return ret
    

myAUV = AUV(latlon=(42.4, -171.3),
            depth=113.1,
            heading=64,
            rudder_position=12,
            speed_knots=3,
            engine_speed='FULL',
            engine_direction='AHEAD',
            datum=(42.5,-171.5))

# Test the engine commands
# TEST 1: BAD COMMAND
cmd = "AHEAD WARP FACTOR 9"
reply = myAUV.engine_command(cmd)
data = get_data_array(myAUV)
engine_state = get_engine_state(myAUV)
print(f"{cmd} : {reply}")
# check the reply
print(f"TEST 1 REPLY: {my_hash(reply)}")
print(f"data = {data}")
print(f"TEST 1 DATA: {round_and_report(data, 3)}")
print(f"TEST 1 ENGINE: {my_hash(engine_state)}\n")

cmd = "ENGINE SLOW ASTERN"
reply = myAUV.engine_command(cmd)
data = get_data_array(myAUV)
engine_state = get_engine_state(myAUV)
print(f"{cmd} : {reply}")
# check the reply
print(f"TEST 2 REPLY: {my_hash(reply)}")
print(f"data = {data}")
print(f"TEST 2 DATA: {round_and_report(data, 3)}")
print(f"TEST 2 ENGINE: {my_hash(engine_state)}\n")

cmd = "ENGINE HALF AHEAD"
reply = myAUV.engine_command(cmd)
data = get_data_array(myAUV)
engine_state = get_engine_state(myAUV)
print(f"{cmd} : {reply}")
# check the reply
print(f"TEST 3 REPLY: {my_hash(reply)}")
print(f"data = {data}")
print(f"TEST 3 DATA: {round_and_report(data, 3)}")
print(f"TEST 3 ENGINE: {my_hash(engine_state)}\n")

cmd = "ENGINE FULL AHEAD"
reply = myAUV.engine_command(cmd)
data = get_data_array(myAUV)
engine_state = get_engine_state(myAUV)
print(f"{cmd} : {reply}")
# check the reply
print(f"TEST 4 REPLY: {my_hash(reply)}")
print(f"data = {data}")
print(f"TEST 4 DATA: {round_and_report(data, 3)}")
print(f"TEST 4 ENGINE: {my_hash(engine_state)}\n")

cmd = "ENGINE STOP"
reply = myAUV.engine_command(cmd)
data = get_data_array(myAUV)
engine_state = get_engine_state(myAUV)
print(f"{cmd} : {reply}")
# check the reply
print(f"TEST 5 REPLY: {my_hash(reply)}")
print(f"data = {data}")
print(f"TEST 5 DATA: {round_and_report(data, 3)}")
print(f"TEST 5 ENGINE: {my_hash(engine_state)}\n")