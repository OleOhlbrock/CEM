"""
Defines a new deviation object from inputs
    Inputs:
        deviationEdge: (curves) The curves that define the deviation members in the topological diagram
        deviationMagn: (float) The force magnitudes of the deviation members [kN] (tension-positive, compression-negative) 
    Outputs:
        D: (deviationObject) The constructed deviation object
    Remarks:
        This generates a new instance of the deviation object
"""

class Deviation(object):
    def __repr__(self):
        return self.ToString()
        
    def __str__(self):
        return self.ToString()
        
    def ToString(self):
        if deviationEdge:
            return "Deviation Member"



if deviationEdge:
    D = Deviation()
    D.geom = []
    D.magn = []
    
    if deviationMagn:
        if len(deviationEdge) == len(deviationMagn):
            deviationMagnC = []
            for i in range(len(deviationEdge)):
                deviationMagnC.append( deviationMagn[i] )
            D.geom = deviationEdge
            D.magn = deviationMagnC
        elif len(deviationMagn) == 1:
            deviationMagnC = []
            for i in range(len(deviationEdge)):
                deviationMagnC.append( deviationMagn[0] )
            D.geom = deviationEdge
            D.magn = deviationMagnC
        else:
            deviationMagnC = []
            for i in range(len(deviationEdge)):
                deviationMagnC.append( 1 )
            D.geom = deviationEdge
            D.magn = deviationMagnC
    else:
        deviationMagnC = []
        for i in range(len(deviationEdge)):
            deviationMagnC.append( 1 )
        D.geom = deviationEdge
        D.magn = deviationMagnC


