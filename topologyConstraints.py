"""
Define constraint plane and origin nodes
    Inputs:
        TM: (topological diagram) The topological diagram used for the calculation of the structural model
        constraintPlane: (plane) The constraint planes
        constraintPlaneID: (int) The index of the vertices where the constraint planes are applied
        originNode: (point) The origin nodes
    Outputs:
        TMC: (updated topological diagram) The topological diagram updated with the constraints (empty topology on error)
    Remarks:
        This generates a new instance of the topological diagram
"""

__author__    = ['Patrick Ole Ohlbrock','Pierluigi D''Acunto' ]
__copyright__ = 'Copyright 2018 - Chair of Structural Design, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'ohlbrock@arch.ethz.ch'
__version__   = "1.0.0"

"""
If you use the library of CEM in a project, please refer to the CEM GitHub repository:
@misc{cem-dev,
    title  = {{CEM}: Combinatorial Equilibrium Modeling},
    author = {Patrick Ole Ohlbrock and Pierluigi D'Acunto},
    note   = {http://cem-dev.github.io/cem/},
    year   = {2018},
}
"""

import copy

TMC = copy.deepcopy(TM)

if TMC and hasattr(TMC, "db1_StructuralBehaviourOut"):
    if constraintPlane and constraintPlane:
        if len(constraintPlane) == len(constraintPlane):
            TMC.pl1_ConstraintPlaneOut = constraintPlane
            TMC.int1_ConstraintPlaneOut = constraintPlaneID
        else:
            TMC.pl1_ConstraintPlaneOut = None
            TMC.int1_ConstraintPlaneOut = None
    else:
        TMC.pl1_ConstraintPlaneOut = None
        TMC.int1_ConstraintPlaneOut = None
    
    if originNode:
        if len(originNode) == len(TM.pt1_OriginNodeOut):
            TMC.pt1_OriginNodeOut = originNode
