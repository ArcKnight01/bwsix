# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 22:38:04 2021

@author: JO20993
"""
from BWSI_BuoyField import Buoy
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
datum = (38.40752369, -62.84727789)
G = Buoy(datum, position=(1000, 2000))
test = list(G.get_latlon())
R = Buoy(datum, position=(2000, 1000))
test += list(R.get_latlon())

G2 = Buoy(datum, latlon=(38.40932463999526, -62.846128718171144))
test += list(G2.get_position())
R2 = Buoy(datum, latlon=(38.40842190695568, -62.84498526510086))
test += list(R2.get_position())

print(f"Buoy test hash is {round_and_report(np.asarray(test),4)}")