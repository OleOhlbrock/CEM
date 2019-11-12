"""
Defines a new point load object from inputs
    Inputs:
        pointLoad: (point) The vertices that define the point loads in the topological diagram
        loadMagnX: (float) The magnitude of the point load in x-direction [kN]
        loadMagnY: (float) The magnitude of the point load in y-direction [kN]
        loadMagnZ: (float) The magnitude of the point load in z-direction [kN]
    Outputs:
        L: (pointLoadObject) The constructed point load object
    Remarks:
        This generates a new instance of the constructed point load object 
"""



import Rhino


class Load(object):
    def __repr__(self):
        return self.ToString()
        
    def __str__(self):
        return self.ToString()
        
    def ToString(self):
        if pointLoad:
            return "Point Load"
        else:
            return "No external Load"



if pointLoad:
    L = Load()
    L.geom = []
    L.magn = []
    
    if not loadMagnX: loadMagnX.append(0.0)
    if not loadMagnY: loadMagnY.append(0.0)
    if not loadMagnZ: loadMagnZ.append(0.0)
    
    loadMagn = []
    if len(loadMagnX) == len(loadMagnY) == len(loadMagnZ):
        if len(pointLoad) == len(loadMagnX):
            for i in range(len(pointLoad)):
                loadMagn.append( (loadMagnX[i],loadMagnY[i],loadMagnZ[i]) )
            L.geom = pointLoad
            L.magn = loadMagn
        elif len(loadMagnX) == 1:
            for i in range(len(pointLoad)):
                loadMagn.append( (loadMagnX[0],loadMagnY[0],loadMagnZ[0]) )
            L.geom = pointLoad
            L.magn = loadMagn
        else:
            for i in range(len(pointLoad)):
                loadMagn.append( 0,0,0 )
            L.geom = pointLoad
            L.magn = loadMagn
    else:
        for i in range(len(pointLoad)):
            loadMagn.append( 0,0,0 )
        L.geom = pointLoad
        L.magn = loadMagn
