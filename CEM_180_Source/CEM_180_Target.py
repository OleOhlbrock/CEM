"""
Assign targets
    Inputs:
        targetNode: (Point3D or Line or Surface) Describes the desired location of a node in the form diagram
        targetNodeID: (integer) The corresponding node ID
        targeNodeCoeff: (Float) The weight factor for matching target nodes
        targetVector: (Vector3D) Describes the desired trail vector in the force diagram
        targetVectorID: (integer) The corresponding trail edge ID
        targeVectorCoeffMag: (Float) The weight factor for matching the magnitude of the target vectors
        targeVectorCoeffDir: (Float) The weight factor for matching the direction of the target vectors
    Outputs:
        TO: (Targets) The assigned targets, their ID and weights.
    Remarks:
        This generates a new instance of targets for the optimization
"""



import Rhino


class TargetOpt(object):
    def __repr__(self):
        return self.ToString()
        
    def __str__(self):
        return self.ToString()
        
    def ToString(self):
        bl0_targetNode = False
        bl0_targetVector = False
        if targetNode and targetNodeID and len(targetNode) == len(targetNodeID):
                bl0_targetNode = True
        if targetVector and targetVectorID and len(targetVector) == len(targetVectorID):
                bl0_targetVector = True
        if bl0_targetNode and bl0_targetVector:
            return "Target Node and Target Vector"
        if bl0_targetNode and not bl0_targetVector:
            return "Target Node"
        if not bl0_targetNode and bl0_targetVector:
            return "Target Vector"
        else:
            return "No Target"

TO = TargetOpt()
if targetNode and targetNodeID and len(targetNode) == len(targetNodeID):
    TO.targetNode = targetNode
    TO.targetNodeID = targetNodeID
    TO.targetNodeCoeff = 0
    if targetNodeCoeff:
        TO.targetNodeCoeff = targetNodeCoeff

if targetVector and targetVectorID and len(targetVector) == len(targetVectorID):
    TO.targetVector = targetVector
    TO.targetVectorID = targetVectorID
    TO.targetVectorCoeffMag = 0
    TO.targetVectorCoeffDir = 0
    if targetVectorCoeffMag:
        TO.targetVectorCoeffMag = targetVectorCoeffMag
    if targetVectorCoeffDir:
        TO.targetVectorCoeffDir = targetVectorCoeffDir
