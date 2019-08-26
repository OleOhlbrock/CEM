
"""
Defines a new support object from inputs
    Inputs:
        support: (points) The support points in the topological diagram
    Outputs:
        S: (supportObject) The constructed support object 
    Remarks:
        This generates a new instance of the support object
"""


class Support(object):
    def __repr__(self):
        return self.ToString()
        
    def __str__(self):
        return self.ToString()
        
    def ToString(self):
        if support:
            return "Support"


if support:
    S = Support()
    S.geom = support
