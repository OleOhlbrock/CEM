"""
Locate origin nodes
    Inputs:
        originNode: (point3d) position of origin node in form diagram
        originNodeID: (integer) index of corresponding node
    Outputs:
        N: (origin-nodes) The assigned origin nodes
    Remarks:
        This generates a new instance of origin nodes
"""




import Rhino


class ONode(object):
    def __repr__(self):
        return self.ToString()
        
    def __str__(self):
        return self.ToString()
        
    def ToString(self):
        if originNode and len(originNode) == len(originNodeID):
            return str(len(originNode)) + " Defined Origin Nodes"
        else:
            return "Undefined Origin Nodes"



if originNode:
    N = ONode()
    N.originNode = originNode
    N.originNodeID = originNodeID


