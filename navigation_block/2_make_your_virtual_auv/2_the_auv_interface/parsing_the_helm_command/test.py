# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 20:07:23 2021

@author: JO20993
"""
from BWSI_AUV import AUV

import sys
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

## make a series of invalid commands to check if errors are handled correctly
bad_commands = list(("GO THAT WAY!", 
                    "UMMMMM", 
                    "RIGHT", 
                    "LEFT FULL", 
                    "RIGHT STANDARD",
                    "LEFT 10 RUDDER",
                    "HARD RIGHT",
                    "RIGHT 25 DEGREES",
                    "I SAID RIGHT 25 DEGREES RUDDER",
                    "LEFT 60 DEGREES RUDDER",
                    "INCREASE YOUR RUDDER TO 5 DEGREES"))
print("*** INVALID COMMANDS ***")
for cmd in bad_commands:
    reply = myAUV.helm_command(cmd)
    print(f"{cmd} : {reply}")
    assert reply=="COMMAND", f"Failed to handle command: {cmd}"

## now a mix of valid commands, make sure state variables are updated appropriately
cmd_list = list(( ("LEFT 10 DEGREES RUDDER", 1, -10),
                  ("INCREASE YOUR RUDDER TO 5 DEGREES", -1, -10),
                  ("INCREASE YOUR RUDDER TO 35 DEGREES", -1, -10),
                  ("INCREASE YOUR RUDDER TO 15 DEGREES", 1, -15),
                  ("SHIFT YOUR RUDDER", 1, 15),
                  ("INCREASE YOUR RUDDER TO 20 DEGREES", 1, 20),
                  ("RIGHT STANDARD RUDDER", 1, 15),
                  ("LEFT FULL RUDDER", 1, -30),
                  ("HARD RIGHT RUDDER", 1, 35),
                  ("KEEP HER SO", 1, 35),
                  ("MARK YOUR HEAD", 0, 35),
                  ("HOW IS YOUR RUDDER", 0, 35),
                  ("RUDDER AMIDSHIPS", 1, 0) ))

print("")
print("***VALID COMMANDS***")
count = 0
for cmd in cmd_list:
    reply = myAUV.helm_command(cmd[0])
    print(f"{cmd[0]} : {reply}")
    
    if (cmd[1] == 1):
        assert (reply == f"{cmd[0]} AYE AYE"), f"Failed to handle {cmd[0]}"
    elif (cmd[1] == -1):
        assert (reply == "COMMAND"), f"Failed to handle {cmd[0]}"       
    
    assert (myAUV._AUV__rudder_position == cmd[2]), f"Incorrect rudder position after {cmd[0]}"

    data = get_data_array(myAUV)
    engine_state = get_engine_state(myAUV)

    # check the reply
    print(f"TEST {count} REPLY: {my_hash(reply)}")
    print(f"TEST {count} DATA: {round_and_report(data, 3)}")
    print(f"TEST {count} ENGINE: {my_hash(engine_state)}\n")
    count = count + 1