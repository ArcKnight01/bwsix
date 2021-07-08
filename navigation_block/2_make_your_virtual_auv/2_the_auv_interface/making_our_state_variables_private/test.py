# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 20:00:35 2021

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
    ret = np.array( [auv._AUV__latlon[0],
                     auv._AUV__latlon[1],
                     auv._AUV__depth,
                     auv._AUV__heading,
                     auv._AUV__rudder_position,
                     auv._AUV__speed_knots,
                     auv._AUV__datum[0],
                     auv._AUV__datum[1],
                     auv._AUV__MAX_SPEED_KNOTS] )
    return ret

def get_engine_state(auv):
    ret = auv._AUV__engine_state[0] + auv._AUV__engine_state[1]
    
    return ret
    

myAUV = AUV(latlon=(42.4, -171.3),
            depth=113.1,
            heading=64,
            rudder_position=12,
            speed_knots=3,
            engine_speed='FULL',
            engine_direction='REVERSE',
            datum=(42.5,-171.5))

cmd = "ENGINE HALF ASTERN"
reply = myAUV.engine_command(cmd)
data = get_data_array(myAUV)
engine_state = get_engine_state(myAUV)
print(f"{cmd} : {reply}")
# check the reply
print(f"TEST 6 REPLY: {my_hash(reply)}")
print(f"TEST 6 DATA: {round_and_report(data, 3)}")
print(f"TEST 6 ENGINE: {my_hash(engine_state)}\n")      