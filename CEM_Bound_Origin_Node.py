"""
Assign bounds to origin nodes
    Inputs:
        boundOriginNodeID: (integer) The origin nodes ID that are allowed to move
        boundUpOriginNodeX: (float) The upper bound distance in X-direction [m]
        boundLowOriginNodeX: (float) The lower bound distance in X-direction [m]
        boundUpOriginNodeY: (float) The upper bound distance in Y-direction [m]
        boundLowOriginNodeY: (float) The lower bound distance in Y-direction [m]
        boundUpOriginNodeZ: (float) The upper bound distance in Z-direction [m]
        boundLowOriginNodeZ: (float) The lower bound distance in Z-direction [m]
    Outputs:
        BO: (Bounds Origin Nodes) The bounds for the origin nodes.
    Remarks:
        This generates a new instance of bounds for the origin nodes for the optimization
"""


import Rhino


class BoundOriginNode(object):
    def __repr__(self):
        return self.ToString()
        
    def __str__(self):
        return self.ToString()
        
    def ToString(self):
        return "Bound Origin Nodes"


BO = BoundOriginNode()
BO.ID = []
BO.UpX = []
BO.LowX = []
BO.UpY = []
BO.LowY = []
BO.UpZ = []
BO.LowZ = []

if boundOriginNodeID:
    if len(boundOriginNodeID) == len(boundUpOriginNodeX) and len(boundOriginNodeID) == len(boundLowOriginNodeX):
        BO.ID = boundOriginNodeID
        BO.UpX = [abs(boundUpOriginNodeX_i) for boundUpOriginNodeX_i in boundUpOriginNodeX]
        BO.LowX = [-abs(boundLowOriginNodeX_i) for boundLowOriginNodeX_i in boundLowOriginNodeX]
    elif len(boundUpOriginNodeX) == 1 and len(boundLowOriginNodeX) == 1:
        boundUpOriginNodeXC = []
        for i in range(len(boundOriginNodeID)):
            boundUpOriginNodeXC.append(abs(boundUpOriginNodeX[0]))
        boundLowOriginNodeXC = []
        for i in range(len(boundOriginNodeID)):
            boundLowOriginNodeXC.append(-abs(boundLowOriginNodeX[0]))
        BO.ID = boundOriginNodeID
        BO.UpX = boundUpOriginNodeXC
        BO.LowX = boundLowOriginNodeXC
    else:
        boundUpOriginNodeXC = []
        for i in range(len(boundOriginNodeID)):
            boundUpOriginNodeXC.append(0.0)
        boundLowOriginNodeXC = []
        for i in range(len(boundOriginNodeID)):
            boundLowOriginNodeXC.append(0.0)
        BO.ID = boundOriginNodeID
        BO.UpX = boundUpOriginNodeXC
        BO.LowX = boundLowOriginNodeXC

    if len(boundOriginNodeID) == len(boundUpOriginNodeY) and len(boundOriginNodeID) == len(boundLowOriginNodeY):
        BO.ID = boundOriginNodeID
        BO.UpY = [abs(boundUpOriginNodeY_i) for boundUpOriginNodeY_i in boundUpOriginNodeY]
        BO.LowY = [-abs(boundLowOriginNodeY_i) for boundLowOriginNodeY_i in boundLowOriginNodeY]
    elif len(boundUpOriginNodeY) == 1 and len(boundLowOriginNodeY) == 1:
        boundUpOriginNodeYC = []
        for i in range(len(boundOriginNodeID)):
            boundUpOriginNodeYC.append(abs(boundUpOriginNodeY[0]))
        boundLowOriginNodeYC = []
        for i in range(len(boundOriginNodeID)):
            boundLowOriginNodeYC.append(-abs(boundLowOriginNodeY[0]))
        BO.ID = boundOriginNodeID
        BO.UpY = boundUpOriginNodeYC
        BO.LowY = boundLowOriginNodeYC
    else:
        boundUpOriginNodeYC = []
        for i in range(len(boundOriginNodeID)):
            boundUpOriginNodeYC.append(0.0)
        boundLowOriginNodeYC = []
        for i in range(len(boundOriginNodeID)):
            boundLowOriginNodeYC.append(0.0)
        BO.ID = boundOriginNodeID
        BO.UpY = boundUpOriginNodeYC
        BO.LowY = boundLowOriginNodeYC

    if len(boundOriginNodeID) == len(boundUpOriginNodeZ) and len(boundOriginNodeID) == len(boundLowOriginNodeZ):
        BO.ID = boundOriginNodeID
        BO.UpZ = [abs(boundUpOriginNodeZ_i) for boundUpOriginNodeZ_i in boundUpOriginNodeZ]
        BO.LowZ = [-abs(boundLowOriginNodeZ_i) for boundLowOriginNodeZ_i in boundLowOriginNodeZ]
    elif len(boundUpOriginNodeZ) == 1 and len(boundLowOriginNodeZ) == 1:
        boundUpOriginNodeZC = []
        for i in range(len(boundOriginNodeID)):
            boundUpOriginNodeZC.append(abs(boundUpOriginNodeZ[0]))
        boundLowOriginNodeZC = []
        for i in range(len(boundOriginNodeID)):
            boundLowOriginNodeZC.append(-abs(boundLowOriginNodeZ[0]))
        BO.ID = boundOriginNodeID
        BO.UpZ = boundUpOriginNodeZC
        BO.LowZ = boundLowOriginNodeZC
    else:
        boundUpOriginNodeZC = []
        for i in range(len(boundOriginNodeID)):
            boundUpOriginNodeZC.append(0.0)
        boundLowOriginNodeZC = []
        for i in range(len(boundOriginNodeID)):
            boundLowOriginNodeZC.append(0.0)
        BO.ID = boundOriginNodeID
        BO.UpZ = boundUpOriginNodeZC
        BO.LowZ = boundLowOriginNodeZC
        
else:
    boundUpOriginNodeXC = []
    for i in range(len(boundOriginNodeID)):
        boundUpOriginNodeXC.append(0.0)
    boundLowOriginNodeXC = []
    for i in range(len(boundOriginNodeID)):
        boundLowOriginNodeXC.append(0.0)
    boundUpOriginNodeYC = []
    for i in range(len(boundOriginNodeID)):
        boundUpOriginNodeYC.append(0.0)
    boundLowOriginNodeYC = []
    for i in range(len(boundOriginNodeID)):
        boundLowOriginNodeYC.append(0.0)
    boundUpOriginNodeZC = []
    for i in range(len(boundOriginNodeID)):
        boundUpOriginNodeZC.append(0.0)
    boundLowOriginNodeZC = []
    for i in range(len(boundOriginNodeID)):
        boundLowOriginNodeZC.append(0.0)
    BO.ID = boundOriginNodeID
    BO.UpX = boundUpOriginNodeXC
    BO.LowX = boundLowOriginNodeXC
    BO.UpY = boundUpOriginNodeYC
    BO.LowY = boundLowOriginNodeYC
    BO.UpZ = boundUpOriginNodeZC
    BO.LowZ = boundLowOriginNodeZC