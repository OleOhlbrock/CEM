"""
Combines the Optimization settings
    Inputs:
        TO: (targets) The assigned targets, their ID and weights
        BO: (boundsoriginnodeObject) The bounds for the origin nodes
        BT: (boundstrailObject) The bounds for the trail edges lengths
        BD: (boundsdeviationObject) The bounds for the deviation edges force magnitudes
        gradientDelta: (float) The delta for the determination of the gradient through finite differences
        relativeTolerance: (float) The threshold which describes one stoping criteria
        maxIterations: (Integer) The maximum number of iteration steps
        optimAlgorithm: (AlgorithmType) The type of solver from the NLOpt library
    Outputs:
        O: (optimization set-up) The settings for an optimization that can be performed 
    Remarks:
        This generates a new instance of the optimization set-up
"""



import Rhino


class Opt(object):
    def __repr__(self):
        return self.ToString()
        
    def __str__(self):
        return self.ToString()
        
    def ToString(self):
        bl0_targetNode = False
        bl0_targetVector = False
        if TO and hasattr(TO, "targetNode") and hasattr(TO, "targetNodeID") and len(TO.targetNode) == len(TO.targetNodeID):
                bl0_targetNode = True
        if TO and hasattr(TO, "targetVector") and hasattr(TO, "targetVectorID") and len(TO.targetVector) == len(TO.targetVectorID):
                bl0_targetVector = True
        if bl0_targetNode and bl0_targetVector:
            return "Target Node and Target Vector"
        if bl0_targetNode and not bl0_targetVector:
            return "Target Node"
        if not bl0_targetNode and bl0_targetVector:
            return "Target Vector"
        else:
            return "No Target"

O = Opt()

if TO and hasattr(TO, "targetNode") and hasattr(TO, "targetNodeID"):
    O.targetNode = TO.targetNode
    O.targetNodeID = TO.targetNodeID
    O.targetNodeCoeff = TO.targetNodeCoeff
    
if TO and hasattr(TO, "targetVector") and hasattr(TO, "targetVectorID"):
    O.targetVector = TO.targetVector
    O.targetVectorID = TO.targetVectorID
    O.targetVectorCoeffMag = TO.targetVectorCoeffMag
    O.targetVectorCoeffDir = TO.targetVectorCoeffDir

if BO and hasattr(BO, "ID"):
    O.boundsOriginNodeID = BO.ID
    O.boundsOriginNodeUpX = BO.UpX
    O.boundsOriginNodeLowX = BO.LowX
    O.boundsOriginNodeUpY = BO.UpY
    O.boundsOriginNodeLowY = BO.LowY
    O.boundsOriginNodeUpZ = BO.UpZ
    O.boundsOriginNodeLowZ = BO.LowZ

if BT and hasattr(BT, "ID"):
    O.boundsTrailID = BT.ID
    O.boundsTrailUp = BT.Up
    O.boundsTrailLow = BT.Low

if BD and hasattr(BD, "ID"):
    O.boundsDevID = BD.ID
    O.boundsDevUp = BD.Up
    O.boundsDevLow = BD.Low

if gradientDelta is None:
    O.gradientDelta = 0.001
else:
    O.gradientDelta = gradientDelta

if relativeTolerance is None:
    O.relativeTolerance = 0.001
else:
    O.relativeTolerance = relativeTolerance

if maxIterations is None:
    O.maxIterations = 20
else:
    O.maxIterations = maxIterations

if optimAlgorithm is None:
    O.optimAlgorithm = "LN_BOBYQA"
else:
    O.optimAlgorithm = optimAlgorithm
