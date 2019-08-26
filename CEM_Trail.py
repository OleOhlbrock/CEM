"""
Defines new trail edges from inputs
    Inputs:
        trailEdge: (curves) The curves (segments) that define the trail members in the topological diagram
        trailLen: (float) The lenghts of the trail members [m] (tension-positive, compression-negative)
    Outputs:
        T: (trailObject) The constructed trail object
    Remarks:
        This generates a new instance of a trail object
"""

import Rhino


class Trail(object):
    def __repr__(self):
        return self.ToString()
        
    def __str__(self):
        return self.ToString()
        
    def ToString(self):
        if trailEdge:
            return "Trail Member"



if trailEdge:
    T = Trail()
    T.geom = []
    T.len = []
    
    if trailLen:
        if len(trailEdge) == len(trailLen):
            trailLenC = []
            for i in range(len(trailEdge)):
                trailLenC.append( trailLen[i] )
            T.geom = trailEdge
            T.len = trailLenC
        elif len(trailLen) == 1:
            trailLenC = []
            for i in range(len(trailEdge)):
                trailLenC.append( trailLen[0] )
            T.geom = trailEdge
            T.len = trailLenC
        else:
            trailLenC = []
            for i in range(len(trailEdge)):
                trailLenC.append( 1 )
            T.geom = trailEdge
            T.len = trailLenC
    else:
        trailLenC = []
        for i in range(len(trailEdge)):
            trailLenC.append( 1 )
        T.geom = trailEdge
        T.len = trailLenC


