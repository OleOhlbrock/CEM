"""
Assign bounds to deviation forces
    Inputs:
        boundDevID: (integer) The deviation edges ID that are allowed to change their force magnitude
        boundUpDev: (float) The upper bound of allowable change of force magnitudes [kN]
        boundLowDev: (float) The lower bound of allowable change of force magnitudes [kN]
    Outputs:
        BD: (Bounds Deviation Edges) The bounds for the deviation edges force magnitudes
    Remarks:
        This generates a new instance of bounds for the deviation edges for the optimization
"""

import Rhino


class BoundDev(object):
    def __repr__(self):
        return self.ToString()
        
    def __str__(self):
        return self.ToString()
        
    def ToString(self):
        return "Bound Deviations"


BD = BoundDev()
BD.ID = []
BD.Up = []
BD.Low = []

if boundDevID:
    if len(boundDevID) == len(boundUpDev) and len(boundDevID) == len(boundLowDev):
        BD.ID = boundDevID
        BD.Up = [abs(boundUpDev_i) for boundUpDev_i in boundUpDev]
        BD.Low = [-abs(boundLowDev_i) for boundLowDev_i in boundLowDev]
    elif len(boundUpDev) == 1 and len(boundLowDev) == 1:
        boundUpDevC = []
        for i in range(len(boundDevID)):
            boundUpDevC.append(abs(boundUpDev[0]))
        boundLowDevC = []
        for i in range(len(boundDevID)):
            boundLowDevC.append(-abs(boundLowDev[0]))
        BD.ID = boundDevID
        BD.Up = boundUpDevC
        BD.Low = boundLowDevC
    else:
        boundUpDevC = []
        for i in range(len(boundDevID)):
            boundUpDevC.append(0.0)
        boundLowDevC = []
        for i in range(len(boundDevID)):
            boundLowDevC.append(0.0)
        BD.ID = boundDevID
        BD.Up = boundUpDevC
        BD.Low = boundLowDevC
else:
    boundUpDevC = []
    for i in range(len(boundDevID)):
        boundUpDevC.append(0.0)
    boundLowDevC = []
    for i in range(len(boundDevID)):
        boundLowDevC.append(0.0)
    BD.ID = boundDevID
    BD.Up = boundUpDevC
    BD.Low = boundLowDevC