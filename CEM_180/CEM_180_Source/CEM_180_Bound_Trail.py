"""
Assign bounds to trail lengths
    Inputs:
        boundTrailID: (integer) The trail edges ID that are allowed to change their length
        boundUpTrail: (float) The upper bound of allowable change of lengths for trail edges [m]
        boundLowTrail: (float) The lower bound of allowable change of lengths for trail edges [m]
    Outputs:
        BT: (Bounds Trail Lengths) The bounds for the trail edges lengths
    Remarks:
        This generates a new instance of bounds for the trail edges for the optimization
"""


import Rhino


class BoundTrail(object):
    def __repr__(self):
        return self.ToString()
        
    def __str__(self):
        return self.ToString()
        
    def ToString(self):
        return "Bound Trails"


BT = BoundTrail()
BT.ID = []
BT.Up = []
BT.Low = []


if boundTrailID:
    if len(boundTrailID) == len(boundUpTrail) and len(boundTrailID) == len(boundLowTrail):
        BT.ID = boundTrailID
        BT.Up = [abs(boundUpTrail_i) for boundUpTrail_i in boundUpTrail]
        BT.Low = [-abs(boundLowTrail_i) for boundLowTrail_i in boundLowTrail]
    elif len(boundUpTrail) == 1 and len(boundLowTrail) == 1:
        boundUpTrailC = []
        for i in range(len(boundTrailID)):
            boundUpTrailC.append(abs(boundUpTrail[0]))
        boundLowTrailC = []
        for i in range(len(boundTrailID)):
            boundLowTrailC.append(-abs(boundLowTrail[0]))
        BT.ID = boundTrailID
        BT.Up = boundUpTrailC
        BT.Low = boundLowTrailC
    else:
        boundUpTrailC = []
        for i in range(len(boundTrailID)):
            boundUpTrailC.append(0.0)
        boundLowTrailC = []
        for i in range(len(boundTrailID)):
            boundLowTrailC.append(0.0)
        BT.ID = boundTrailID
        BT.Up = boundUpTrailC
        BT.Low = boundLowTrailC
else:
    boundUpTrailC = []
    for i in range(len(boundTrailID)):
        boundUpTrailC.append(0.0)
    boundLowTrailC = []
    for i in range(len(boundTrailID)):
        boundLowTrailC.append(0.0)
    BT.ID = boundTrailID
    BT.Up = boundUpTrailC
    BT.Low = boundLowTrailC