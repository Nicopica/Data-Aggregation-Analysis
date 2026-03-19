#!/usr/bin/env python3
import sys
import math
import os

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0 # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat / 2)**2 + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

try:
    TARGET_X = float(os.environ.get('TARGET_X', 0.0))
    TARGET_Y = float(os.environ.get('TARGET_Y', 0.0))
    MAX_D = float(os.environ.get('MAX_D', 0.0))
except ValueError:
    sys.exit(1)

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split('\t')
    if len(parts) == 3:
        try:
            lat = float(parts[0])
            lon = float(parts[1])
            value = float(parts[2])
            
            dist = haversine(TARGET_X, TARGET_Y, lat, lon)
            
            if dist <= MAX_D:
                print("Aggregated_Metrics\t{}".format(value))
        except ValueError:
            pass
