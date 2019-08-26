"""
Assign self weight
    Inputs:
        selfWeight: (bool) Activate the self weight of the structure
        yieldStress: (double) The yield stress of the structural members
        specWeight: (double) The specific weight of the structural members
    Outputs:
        SW: (self-weight) The assigned self weight properties 
    Remarks:
        This generates a new instance of self weight
"""





import Rhino


class SWeight(object):
    def __repr__(self):
        return self.ToString()
        
    def __str__(self):
        return self.ToString()
        
    def ToString(self):
        if selfWeight and yieldStress and specWeight:
                return "Self Weight"
        else:
            return "No Self Weight"

SW = SWeight()
if selfWeight and yieldStress and specWeight:
    SW.yieldStress = yieldStress
    SW.specWeight = specWeight


