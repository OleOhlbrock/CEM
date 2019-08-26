"""
Retrieves automatically geometric properties from the topological diagram
    Inputs:
        TP: (topological diagram) The topological diagram used for the calculation of the structural model
    Outputs:
        nodes: (point 3D) The vertices describing the topological diagram
        nodesID: (integer) The corresponding node number
        edges: (edge midpoint) The edges describing the topological diagram
        edgesID: (integer) The corresponding edge number
        constraintPlane: (plane) The planes which are based on the trails normal vectors of the toplogical diagram 
        constraintPlaneID: (integer) The indices of these planes
        originNode: (point 3D) The origin points from the topological diagram
        originNodeID: (integer) The indices of these points
    Remarks:
        This extract geometric information from TP
"""




if TP and hasattr(TP, "str1_NodeOut") and hasattr(TP, "pt1_NodeOut"):
    nodes = TP.pt1_NodeOut
    nodesID = TP.str1_NodeOut


if TP and hasattr(TP, "str1_NodeOut") and hasattr(TP, "pt1_NodeOut"):
    edges = TP.pt1_EdgeOut
    edgesID = TP.str1_EdgeOut


if TP and hasattr(TP, "pl1_ConstraintPlaneOut") and hasattr(TP, "str1_ConstraintPlaneOut"):
    constraintPlane = TP.pl1_ConstraintPlaneOut
    constraintPlaneID = TP.str1_ConstraintPlaneOut

if TP and hasattr(TP, "pt1_OriginNodeOut"):
    originNode = TP.pt1_OriginNodeOut
    originNodeID = TP.str1_OriginNodeOut
