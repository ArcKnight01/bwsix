# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 22:43:53 2021

@author: JO20993
"""
from BWSI_BuoyField import BuoyField
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

# main
nbuoys = 10
datum = (38.40752369, -62.84727789)
R = list()
G = list()
for i in range(nbuoys):
    G.append((1000*(i+1), 2000+100*(i+1)+10))
    R.append((1000*(i+1), 2000+100*(i+1)-10))

buoyField = BuoyField(datum, green_buoys=G, red_buoys=R, position_style='P')

gp, rp = buoyField.get_buoy_positions()
green_lat, red_lat = buoyField.get_buoy_latlon()

alllist=list(green_lat)
alllist+=list(red_lat)

test = np.array(alllist).flatten()
print(f"Buoy field latlon hash is {round_and_report(np.asarray(test),4)}")

G = [(38.42475141773541, -62.85869787040542),(38.423863448475636, -62.87015571348847),
     (38.42297435839218, -62.8816132789996),(38.42208414759089, -62.8930705663209),
     (38.42119281617776, -62.90452757483449),(38.42030036425898, -62.91598430392266),
     (38.41940679194095, -62.92744075296788),(38.41851209933023, -62.938896921352665),
     (38.417616286533544, -62.95035280845964),(38.416719353657854, -62.96180841367159)]

R = [(38.42457117335597, -62.85869822158408),(38.423683203983295, -62.87015603618071),
     (38.42279411379416, -62.88161357320791),(38.42190390289436, -62.89307083204772),
     (38.42101257138991, -62.90452781208234),(38.42012011938702, -62.915984512694045),
     (38.41922654699208, -62.92744093326528),(38.418331854311596, -62.93889707317855),
     (38.417436041452376, -62.95035293181659),(38.41653910852133, -62.96180850856207)]

buoyField = BuoyField(datum, green_buoys=G, red_buoys=R, position_style='L')

green_pos, red_pos = buoyField.get_buoy_positions()
gl, rl = buoyField.get_buoy_latlon()

alllist=list(green_pos)
alllist+=list(red_pos)

test = np.array(alllist).flatten()
print(f"Buoy field position hash is {round_and_report(np.asarray(test),4)}")