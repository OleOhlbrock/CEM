"""
Calculate the structural model
    Inputs:
        TP: (topological diagram) The topological diagram used for the calculation of the structural model
        CPL: (constraintPlaneObject) The constraint planes and their Indices
        N: (originnodeObject) The origin nodes and their Indices
        SW: (selfWeightObject) The Activation of self weight of the structure and their yield stress and specific weight attributes
        O: (optimizationObject) The Settings for an Optimization that can be performed 
    Outputs:
        M: (structural model) The calculated structural model (empty model on error)
    Remarks:
        This generates a new instance of the structural model for a given topological diagram
"""

__author__    = ['Patrick Ole Ohlbrock','Pierluigi D''Acunto' ]
__copyright__ = 'Copyright 2019 - Chair of Structural Design, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'ohlbrock@arch.ethz.ch'
__version__   = "1.80"

"""
If you use the CEM library in a project, please refer to the GitHub repository: 

@Misc{cem2019,
author = {Ohlbrock, Patrick Ole and D'Acunto, Pierluigi},
title = {{CEM: Combinatorial Equilibrium Modeling}},
year = {2019},
note = {Release 1.80},
url = { http://github.com/OleOhlbrock/CEM },
}

"""

import Grasshopper, GhPython
import System
import rhinoscriptsyntax as rs
import Rhino.Geometry as rh
import math
import System.Drawing.Color
import copy
import time
import clr
import os
import collections
from os.path import expanduser
from System import Array, Func

path = expanduser(str(os.getenv('APPDATA')) + ("\\Grasshopper\\Libraries\\NLoptNet\\NLoptNet.dll"))
path = expanduser(path)

clr.AddReferenceToFileAndPath(path)
clr.AddReference('System.Core')

import NLoptNet as nl

global int0_Counter
global pt2_Trails
global pt1_GlobNodeOut
global ln1_GlobTrailEdgeOut
global ln1_GlobDeviation1EdgeOut
global ln1_GlobDeviation2EdgeOut
global vc2_GlobTrailForce
global ln2_GlobExtEdge
global pt2_GlobNode
global pt2_GlobNodeIteration
global ln2_GlobTrailEdge
global cl2_GlobTrailEdge
global db2_GlobTrailEdge
global ln2_GlobDeviation1Edge
global cl2_GlobDeviation1Edge
global db2_GlobDeviation1Edge
global ln2_GlobDeviation2Edge
global cl2_GlobDeviation2Edge
global db2_GlobDeviation2Edge
global ln2_GlobExtFOEdge
global cl2_GlobExtFOEdge
global db2_GlobExtFOEdge
global int0_CounterOpt 
global db0_DistanceBest
global db1_VariableBest
global str1_TrailEdgeID
global str1_Dev1EdgeID
global str1_Dev2EdgeID
global int1_DevEdgeInputID
global str0_GlobSolver
global str0_GlobDivergence
global str0_GlobIteration

class model(object):
    def __repr__(self):
        return self.ToString()
        
    def __str__(self):
        return self.ToString()
        
    def ToString(self):
        if TPC and hasattr(TPC, "db1_StructuralBehaviourOut"):
            str0_Description = ""
            if int0_LayerCount:
                str0_Description += "Structural Model\n\nlayers: " + str(int0_LayerCount)
                if pt1_GlobNodeOut and ln1_GlobTrailEdgeOut:
                    str0_Description += "\nvertices: " + str(len(pt1_GlobNodeOut)-int0_TrailNumber) + "\ntrail members: " + str(len(ln1_GlobTrailEdgeOut)-int0_TrailNumber) 
                    if ln1_GlobDeviation1EdgeOut:
                        str0_Description += "\ndirect deviation members: " + str(len(ln1_GlobDeviation1EdgeOut))
                    if ln1_GlobDeviation2EdgeOut:
                        str0_Description += "\nindirect deviation members: " + str(len(ln1_GlobDeviation2EdgeOut))
                    if str0_GlobSolver:
                        str0_Description += "\nsolver: " +  str0_GlobSolver
                        if str0_GlobDivergence:
                            str0_Description += "\ndivergence: " +  str0_GlobDivergence
                    return str0_Description
                else:
                    return "Empty Structural Model"
            else:
                return "Empty Structural Model"
        else:
            return "Empty Structural Model"



### AUXILIARY FUNCTIONS
def ListListToList(xx2_Data):
    xx1_DataOut = []
    for xx1_Data in xx2_Data:
        xx1_DataOut.extend(xx1_Data)
    return xx1_DataOut

def TransposeListList(xx2_Data):
    xx2_DataOut = list(map(list, zip(*xx2_Data)))
    return xx2_DataOut
    
def ListToListList(xx1_Data, int0_R, int0_C):
    xx2_DataOut = []
    for i in xrange(int0_R):
        xx1_DataOut = []
        for j in xrange(int0_C):
            xx1_DataOut.append(xx1_Data[j+i*int0_C])
        xx2_DataOut.append(xx1_DataOut)
    return xx2_DataOut

def DataTreeToListList(dt2_Data):
    xx2_DataOut = []
    for i in xrange(dt2_Data.BranchCount):
        xx1_DataOut = []
        for j in xrange(len(dt2_Data.Branch(i))):
            xx1_DataOut.append(dt2_Data.Branch(i)[j])
        xx2_DataOut.append(xx1_DataOut)
    return xx2_DataOut


constraintPlane = []
constraintPlaneID = []

if CPL:
    constraintPlane = CPL.constraintPlane
    constraintPlaneID = CPL.constraintPlaneID


targetNode = []
targetNodeID = []
targetNodeCoeff = 0

if O and hasattr(O, "targetNode") and hasattr(O, "targetNodeID"):
    targetNode = O.targetNode
    targetNodeID = O.targetNodeID
    targetNodeCoeff = O.targetNodeCoeff

targetVector = []
targetVectorID = []
targetVectorCoeffMag = 0
targetVectorCoeffDir = 0

if O and hasattr(O, "targetVector") and hasattr(O, "targetVectorID"):
    targetVector = O.targetVector
    targetVectorID = O.targetVectorID
    targetVectorCoeffMag = O.targetVectorCoeffMag
    targetVectorCoeffDir = O.targetVectorCoeffDir

yieldStress = None
specWeight = None

if SW and hasattr(SW, "yieldStress") and hasattr(SW, "specWeight"):
    yieldStress = SW.yieldStress
    specWeight = SW.specWeight

TPC = copy.deepcopy(TP)

if TPC and hasattr(TPC, "db1_StructuralBehaviourOut"):
    if len(constraintPlane) > 0:
        if len(constraintPlane) == len(constraintPlaneID):
            TPC.pl1_ConstraintPlaneOut = constraintPlane
            TPC.int1_ConstraintPlaneOut = constraintPlaneID
        else:
            TPC.pl1_ConstraintPlaneOut = None
            TPC.int1_ConstraintPlaneOut = None
    else:
        TPC.pl1_ConstraintPlaneOut = None
        TPC.int1_ConstraintPlaneOut = None

    if N and hasattr(N, "originNode"):
        if len(N.originNode) == len(TPC.pt1_OriginNodeOut):
            TPC.pt1_OriginNodeOut = N.originNode
        if hasattr(N, "originNodeID") and len(N.originNodeID) == len(TPC.str1_OriginNodeOut):
            int1_OriginNodeOut = [int(str0_OriginNodeOut) for str0_OriginNodeOut in TPC.str1_OriginNodeOut]
            pt1_OriginNodeShift = []
            if collections.Counter(N.originNodeID) == collections.Counter(int1_OriginNodeOut):
                for int0_OriginNodeID in N.originNodeID:
                    pt1_OriginNodeShift.append(TPC.pt1_OriginNodeOut[int1_OriginNodeOut.index(int0_OriginNodeID)])
                TPC.pt1_OriginNodeOut = pt1_OriginNodeShift


## CREATE LIST OF EDGES IDS

if TPC and hasattr(TPC, "dc2_TrailEndsOut"):
    dc2_TrailEdge = dict( [ [tuple(v),k] for k, v in TPC.dc2_TrailEndsOut.items() ] )

str1_NodeOrder = []
if TPC and hasattr(TPC, "db1_StructuralBehaviourOut"):
    str1_NodeOrder = TPC.str1_NodeOrderOut[:]

# Trail Edge
str1_TrailEdgeID = []
for str0_NodeOrder in str1_NodeOrder:
    for key in dc2_TrailEdge:
        if str0_NodeOrder == key[0] and dc2_TrailEdge[key] != "X":
            str1_TrailEdgeID.append( dc2_TrailEdge[key] )
            dc2_TrailEdge[key] = "X"
        if str0_NodeOrder == key[1] and dc2_TrailEdge[key] != "X":
            str1_TrailEdgeID.append( dc2_TrailEdge[key] )
            dc2_TrailEdge[key] = "X"

# Direct Deviation Edges

dc2_Deviation1EndsOut = []
dc2_Deviation2EndsOut = []
db1_StructuralBehaviourOut = []
pt1_OriginNodeOut = []

if TPC and hasattr(TPC, "db1_StructuralBehaviourOut"):
    dc2_Deviation1EndsOut = TPC.dc2_Deviation1EndsOut
    dc2_Deviation2EndsOut = TPC.dc2_Deviation2EndsOut
    db1_StructuralBehaviourOut = TPC.db1_StructuralBehaviourOut
    pt1_OriginNodeOut = TPC.pt1_OriginNodeOut


    dc2_Dev1Edge = dict( [ [tuple(v),k] for k, v in dc2_Deviation1EndsOut.items() ] )
    dc2_Dev2Edge = dict( [ [tuple(v),k] for k, v in dc2_Deviation2EndsOut.items() ] )

    str1_Dev1EdgeID = []
    db2_StructuralBehaviourOut = []
    for i in range(len(str1_NodeOrder)):
        db1_StructuralBehaviourOutRow = db1_StructuralBehaviourOut[i*(3+len(pt1_OriginNodeOut)+1):(i+1)*(3+len(pt1_OriginNodeOut)+1)]
        db2_StructuralBehaviourOut.append(db1_StructuralBehaviourOutRow)
    
    for i in range(len(db2_StructuralBehaviourOut)):
        for j in range(4+(i % (len(db2_StructuralBehaviourOut[i])-4) ) ,len(db2_StructuralBehaviourOut[i])-1):
            if db2_StructuralBehaviourOut[i][j] != 0:
                id_i = str1_NodeOrder[i]
                id_j = str1_NodeOrder[ (i // (len(db2_StructuralBehaviourOut[i])-4)) * (len(db2_StructuralBehaviourOut[i])-4) + j-3]
                if (id_i,id_j) in dc2_Dev1Edge:
                    str1_Dev1EdgeID.append(dc2_Dev1Edge[(id_i,id_j)])
                else:
                    str1_Dev1EdgeID.append(dc2_Dev1Edge[(id_j,id_i)])
    
    # Indirect Deviation Edges
    int1_Dev2EdgeID = sorted([int(key) for key in dc2_Deviation2EndsOut.copy()])
    str1_Dev2EdgeID = [str(key) for key in int1_Dev2EdgeID]
    
    int1_DevEdgeInputID = []
    if TPC and hasattr(TPC, "db1_StructuralBehaviourOut"):
        int1_DevEdgeInputID = TPC.int1_Deviation1ID[:]
        int1_DevEdgeInputID.extend(TPC.int1_Deviation2ID)


### EQUILIBRIUM FUNCTION
def Equilibrium(db1_StructuralBehaviour, xx1_Bracing, pt1_OriginNode, pl1_ConstraintPlane):
    
    global int0_Counter     # global counter
    


    
    g = 0                                   
    ### ITERATE FOR EACH LAYER OF THE STRUCTURE
    
    ## Initialize
    pt1_InputNode = []
    
    
    for g in xrange(int0_LayerCount):
        
        vc1_TrailForceIn = []
        
        if g == 0:
            pt1_InputNode = pt1_OriginNode
            for i in xrange(int0_TrailNumber):
                vc1_TrailForceIn.append(rh.Vector3d(0,0,0)) 
        else:
            pt1_InputNode = pt2_GlobNode[g-1]
            for i in xrange(int0_TrailNumber):
                vc1_TrailForceIn.append(-vc2_GlobTrailForce[g-1][i])
    
        # Extract Deviation Matrix
        db2_DevForceMag = []

        for i in range(g * int0_TrailNumber, (g + 1) * int0_TrailNumber):
            db1_DevForceMag = []
            for j in range(3, int0_TrailNumber + 3):
                db1_DevForceMag.append(db2_StructuralBehaviour[i][j])
            db2_DevForceMag.append(db1_DevForceMag)
    
    
        ### LAYER DEVELOPMENT
        
        ## Initialize Layer
        
        
        # Create Deviation Length and Unit Vector Matrix
        vc2_DevLengthVector = []
        vc2_DevUnitVector = []
        db2_DevLengthVector = []
        
        vc2_DevLengthVector = [ [rh.Vector3d(0.0,0.0,0.0) for i in xrange(int0_TrailNumber)] for i in xrange(int0_TrailNumber)]
        vc2_DevUnitVector = [ [rh.Vector3d(0.0,0.0,0.0) for i in xrange(int0_TrailNumber)] for i in xrange(int0_TrailNumber)]
        db2_DevLengthVector = [ [0.0 for i in xrange(int0_TrailNumber)] for i in xrange(int0_TrailNumber)]
        
        for i in xrange(int0_TrailNumber):
            for j in xrange(int0_TrailNumber):
                if abs(db2_DevForceMag[i][j]) > db0_Threshold:
                    vc0_InputNode_j = rh.Vector3d(pt1_InputNode[j])
                    vc0_InputNode_i = rh.Vector3d(pt1_InputNode[i])
                    vc0_DevLengthVector = vc0_InputNode_j - vc0_InputNode_i
                    vc2_DevLengthVector[i][j] = vc0_DevLengthVector
                    vc2_DevLengthVector[j][i] = -vc0_DevLengthVector
                    db0_DevLengthVector = vc0_DevLengthVector.Length
                    db2_DevLengthVector[i][j] = db0_DevLengthVector
                    db2_DevLengthVector[j][i] = db0_DevLengthVector
                    vc0_DevUnitVector = rh.Vector3d(vc0_DevLengthVector.X/db0_DevLengthVector, vc0_DevLengthVector.Y/db0_DevLengthVector, vc0_DevLengthVector.Z/db0_DevLengthVector)
                    vc2_DevUnitVector[i][j] = vc0_DevUnitVector
                    vc2_DevUnitVector[j][i] = -vc0_DevUnitVector
        
        
        
        ### MAIN FUNCTION
        
        # Create List of External Forces
        # list for external and bracing forces
        db1_ExtForceX = []
        db1_ExtForceY = []
        db1_ExtForceZ = []
        
        # list for external forces only
        db1_ExtFOX = []
        db1_ExtFOY = []
        db1_ExtFOZ = []
        
        # Add External Forces from Matrix    
        for i in xrange(g*int0_TrailNumber,(g+1)*int0_TrailNumber):
            db1_ExtFOX.append(db2_StructuralBehaviour[i][0])
            db1_ExtFOY.append(db2_StructuralBehaviour[i][1])
            db1_ExtFOZ.append(db2_StructuralBehaviour[i][2])
            
        for i in xrange(g*int0_TrailNumber,(g+1)*int0_TrailNumber):
            db1_ExtForceX.append(db2_StructuralBehaviour[i][0])
            db1_ExtForceY.append(db2_StructuralBehaviour[i][1])
            db1_ExtForceZ.append(db2_StructuralBehaviour[i][2])
            
            # Add Magnitudes of Bracing Forces as External Forces
            # Start node of bracing
            if len(xx1_Bracing) > 0:
                if int0_Counter != 0:
                    for j in xrange(0,len(xx1_Bracing),3):
                        int0_BracingFromLayerIndex = int(xx1_Bracing[j]) // int0_TrailNumber
                        if i == int(xx1_Bracing[j]):
                            pt0_BracingFrom = pt2_GlobNodeIteration[g][i-g*int0_TrailNumber]
                            int0_BracingToLayerIndex = int(xx1_Bracing[j+1]) // int0_TrailNumber
                            int0_BracingToTrailIndex = int(xx1_Bracing[j+1]) % int0_TrailNumber
                            pt0_BracingTo = pt2_GlobNodeIteration[int0_BracingToLayerIndex][int0_BracingToTrailIndex]
                            vc0_ForceA = rh.Vector3d(pt0_BracingTo-pt0_BracingFrom)
                            rh.Vector3d.Unitize(vc0_ForceA)
                            vc0_ForceA = float(xx1_Bracing[j+2])*vc0_ForceA
                            db1_ExtForceX[i-g*int0_TrailNumber] += vc0_ForceA.X
                            db1_ExtForceY[i-g*int0_TrailNumber] += vc0_ForceA.Y
                            db1_ExtForceZ[i-g*int0_TrailNumber] += vc0_ForceA.Z
                        
            # End node of bracing
            if len(xx1_Bracing) > 0:
                if int0_Counter != 0:
                    for j in xrange(1,len(xx1_Bracing),3):
                        int0_BracingFromLayerIndex = int(xx1_Bracing[j]) // int0_TrailNumber
                        if i == int(xx1_Bracing[j]):
                            pt0_BracingFrom = pt2_GlobNodeIteration[g][i-g*int0_TrailNumber]
                            int0_BracingToLayerIndex = int(xx1_Bracing[j-1]) // int0_TrailNumber
                            int0_BracingToTrailIndex = int(xx1_Bracing[j-1]) % int0_TrailNumber
                            pt0_BracingTo = pt2_GlobNodeIteration[int0_BracingToLayerIndex][int0_BracingToTrailIndex]
                            vc0_ForceA = rh.Vector3d(pt0_BracingTo-pt0_BracingFrom)
                            rh.Vector3d.Unitize(vc0_ForceA)
                            vc0_ForceA = float(xx1_Bracing[j+1])*vc0_ForceA
                            db1_ExtForceX[i-g*int0_TrailNumber] += vc0_ForceA.X
                            db1_ExtForceY[i-g*int0_TrailNumber] += vc0_ForceA.Y
                            db1_ExtForceZ[i-g*int0_TrailNumber] += vc0_ForceA.Z
        
        # Vector sum of external and bracing forces for the equilibrium calculation
        vc1_ExtForce = []
        for i in xrange(int0_TrailNumber):
            vc0_ExtForce = rh.Vector3d(db1_ExtForceX[i],db1_ExtForceY[i],db1_ExtForceZ[i])
            vc1_ExtForce.append(vc0_ExtForce)
        
        # Vector sum of external forces only for visualization
        vc1_ExtFO = []
        for i in xrange(int0_TrailNumber):
            vc0_ExtFO = rh.Vector3d(db1_ExtFOX[i],db1_ExtFOY[i],db1_ExtFOZ[i])
            vc1_ExtFO.append(vc0_ExtFO)
        
        # Add External Forces to the Form Diagram
        ln1_ExtFOEdge = []
        cl1_ExtFOEdge = []
        db1_ExtFOEdge = []
        
        for i in xrange(len(vc1_ExtFO)):
            ln1_ExtFOEdge.append(rh.Line(pt1_InputNode[i],(pt1_InputNode[i] + vc1_ExtFO[i])))
            cl1_ExtFOEdge.append(System.Drawing.Color.DarkGreen)
            db1_ExtFOEdge.append(abs(vc1_ExtFO[i].Length))
        
        # Extract Deviation Matrix
        db2_DevForceMag = []
        
        for i in xrange(g*int0_TrailNumber,(g+1)*int0_TrailNumber):
            db1_DevForceMag = []
            for j in xrange(3,int0_TrailNumber+3):
                db1_DevForceMag.append(db2_StructuralBehaviour[i][j])
            db2_DevForceMag.append(db1_DevForceMag)
        
        
        # Create Trail Length and Static Action Matrix from Input Origin Points
        db1_TrailLength = []
        db1_TrailStatAct = []
        
        for i in xrange(g*int0_TrailNumber,(g+1)*int0_TrailNumber):
            db1_TrailLength.append(db2_StructuralBehaviour[i][int0_TrailNumber+3])
            if g == 0:
                db1_TrailStatAct.append(0)
            else:
                db1_TrailStatAct.append(abs((db2_StructuralBehaviour[i-int0_TrailNumber][int0_TrailNumber+3]*vc1_TrailForceIn[i-g*int0_TrailNumber]).Length))
        
        # Calculate Hadamard Product of Deviation Length Matrix and Deviation Matrix
        vc2_DevForce = []
        db2_DevStatAct = []
        
        for i in xrange(int0_TrailNumber):
            vc1_DevForce = []
            db1_DevStatAct = []
            for j in xrange(int0_TrailNumber):
                vc0_DevForce = vc2_DevUnitVector[i][j]*db2_DevForceMag[i][j]
                db0_DevStatAct = abs(db2_DevLengthVector[i][j]*db2_DevForceMag[i][j])
                vc1_DevForce.append(vc0_DevForce)
                db1_DevStatAct.append(db0_DevStatAct)
            vc2_DevForce.append(vc1_DevForce)
            db2_DevStatAct.append(db1_DevStatAct)

        
        # Sum Deviation Vectors and Static Action per each Node
        vc1_DevForceSum = []
        db1_DevStatActSum = []
        db1_IndDevStatActSum = []
        
        for i in xrange(int0_TrailNumber):
            vc0_DevForceSum = rh.Vector3d(0,0,0)
            db0_DevStatActSum = 0
            for j in xrange(int0_TrailNumber):
                vc0_DevForceSum += vc2_DevForce[i][j]
                db0_DevStatActSum += db2_DevStatAct[i][j]
            vc1_DevForceSum.append(vc0_DevForceSum)
            db1_DevStatActSum.append(db0_DevStatActSum)
        # Get Static Action per Node for Indirect Deviations
        # Start Node of Inderect Deviations
        if specWeight and yieldStress and len(xx1_Bracing) > 0:
            int1_StartBracingIndex = []
            int1_EndBracingIndex = []
            db1_BracingValue = []
            for i in xrange(0,len(xx1_Bracing),3):
                int1_StartBracingIndex.append(int(xx1_Bracing[i]))
                int1_EndBracingIndex.append(int(xx1_Bracing[i+1]))
                db1_BracingValue.append(float(xx1_Bracing[i+2]))
            for i in xrange(int0_TrailNumber):
                if int0_Counter != 0:
                    int1_StartBracingIndex_C = int1_StartBracingIndex[:]
                    int1_EndBracingIndex_C = int1_EndBracingIndex[:]
                    db1_BracingValue_C = db1_BracingValue[:]
                    db0_IndDevStatActSum = 0
                    for j in int1_StartBracingIndex:
                        if g*int0_TrailNumber + i == j:
                            int0_StartBracingIndex = int1_StartBracingIndex_C.index(g*int0_TrailNumber + i)
                            int0_StartBracingGlobIndex = g*int0_TrailNumber + i
                            int0_EndBracingGlobIndex = int1_EndBracingIndex_C[ int0_StartBracingIndex ]
                            db0_ValueBracingGlobIndex = db1_BracingValue_C[ int0_StartBracingIndex ]
                            int1_StartBracingIndex_C.pop( int0_StartBracingIndex )
                            int1_EndBracingIndex_C.pop( int0_StartBracingIndex )
                            db1_BracingValue_C.pop( int0_StartBracingIndex )
                            # Get Start and End Nodes of Bracing
                            int0_StartBracingLayer = g
                            int0_StartBracingTrail = i
                            int0_EndBracingLayer = int0_EndBracingGlobIndex // int0_TrailNumber
                            int0_EndBracingTrail = int0_EndBracingGlobIndex % int0_TrailNumber
                            pt0_StartBracing = pt2_GlobNodeIteration[int0_StartBracingLayer][int0_StartBracingTrail]
                            pt0_EndBracing = pt2_GlobNodeIteration[int0_EndBracingLayer][int0_EndBracingTrail]
                            db0_IndDevStatActSum += abs(db0_ValueBracingGlobIndex*pt0_StartBracing.DistanceTo(pt0_EndBracing))
                    db1_IndDevStatActSum.append(db0_IndDevStatActSum)
                        
            # End Node of Inderect Deviations
            int1_StartBracingIndex = []
            int1_EndBracingIndex = []
            db1_BracingValue = []
            for i in xrange(1,len(xx1_Bracing),3):
                int1_StartBracingIndex.append(int(xx1_Bracing[i-1]))
                int1_EndBracingIndex.append(int(xx1_Bracing[i]))
                db1_BracingValue.append(float(xx1_Bracing[i+1]))
            for i in xrange(int0_TrailNumber):
                if int0_Counter != 0:
                    int1_StartBracingIndex_C = int1_StartBracingIndex[:]
                    int1_EndBracingIndex_C = int1_EndBracingIndex[:]
                    db1_BracingValue_C = db1_BracingValue[:]
                    db0_IndDevStatActSum = 0
                    for j in int1_EndBracingIndex:
                        if g*int0_TrailNumber + i == j:
                            int0_EndBracingIndex = int1_EndBracingIndex_C.index(g*int0_TrailNumber + i)
                            int0_EndBracingGlobIndex = g*int0_TrailNumber + i
                            int0_StartBracingGlobIndex = int1_StartBracingIndex_C[ int0_EndBracingIndex ]
                            db0_ValueBracingGlobIndex = db1_BracingValue_C[ int0_EndBracingIndex ]
                            int1_StartBracingIndex_C.pop( int0_EndBracingIndex )
                            int1_EndBracingIndex_C.pop( int0_EndBracingIndex )
                            db1_BracingValue_C.pop( int0_EndBracingIndex )
                            # Get Start and End Nodes of Bracing
                            int0_EndBracingLayer = g
                            int0_EndBracingTrail = i
                            int0_StartBracingLayer = int0_StartBracingGlobIndex // int0_TrailNumber
                            int0_StartBracingTrail = int0_StartBracingGlobIndex % int0_TrailNumber
                            pt0_StartBracing = pt2_GlobNodeIteration[int0_StartBracingLayer][int0_StartBracingTrail]
                            pt0_EndBracing = pt2_GlobNodeIteration[int0_EndBracingLayer][int0_EndBracingTrail]
                            db0_IndDevStatActSum += abs(db0_ValueBracingGlobIndex*pt0_StartBracing.DistanceTo(pt0_EndBracing))
                    db1_IndDevStatActSum[i] += db0_IndDevStatActSum
        else:
            db1_IndDevStatActSum = [0.0 for i in range(int0_TrailNumber)]
        
        # Construct Equilibrium per each Node
        vc1_TrailForceOut = []
        vc1_SelfWeight = []
        for i in xrange(int0_TrailNumber):
            if int0_Counter == 0 and len(xx1_Bracing) > 0:
                if specWeight and yieldStress:
                    vc0_SelfWeight = rh.Vector3d(((db1_TrailStatAct[i] + db1_DevStatActSum[i]/2)*specWeight/yieldStress)*(-rh.Vector3d.ZAxis))
                    vc0_TrailForceOut = -(vc1_ExtForce[i] + vc1_DevForceSum[i] + vc1_TrailForceIn[i] + vc0_SelfWeight)
                    vc1_TrailForceOut.append(vc0_TrailForceOut)
                    vc1_SelfWeight.append(vc0_SelfWeight)
                else:
                    vc0_TrailForceOut = -(vc1_ExtForce[i] + vc1_DevForceSum[i] + vc1_TrailForceIn[i])
                    vc1_TrailForceOut.append(vc0_TrailForceOut)
            else:
                if specWeight and yieldStress:
                    vc0_SelfWeight = rh.Vector3d(((db1_TrailStatAct[i] + db1_DevStatActSum[i]/2 + db1_IndDevStatActSum[i]/2 )*specWeight/yieldStress)*(-rh.Vector3d.ZAxis))
                    vc0_TrailForceOut = -(vc1_ExtForce[i] + vc1_DevForceSum[i] + vc1_TrailForceIn[i] + vc0_SelfWeight)
                    vc1_TrailForceOut.append(vc0_TrailForceOut)
                    vc1_SelfWeight.append(vc0_SelfWeight)
                else:
                    vc0_TrailForceOut = -(vc1_ExtForce[i] + vc1_DevForceSum[i] + vc1_TrailForceIn[i])
                    vc1_TrailForceOut.append(vc0_TrailForceOut)
                

        # Add Self Weight to the Form Diagram
        # external force plus self-weight
        for i in xrange(len(vc1_SelfWeight)):
            ln1_ExtFOEdge.append(rh.Line(pt1_InputNode[i],(pt1_InputNode[i] + vc1_SelfWeight[i])))
            cl1_ExtFOEdge.append(System.Drawing.Color.DarkGreen)
            db1_ExtFOEdge.append(abs(vc1_SelfWeight[i].Length))
        
        
        ## Construction Form Diagram
        
        # Find New Nodes
       
        pt1_Node = []
        
        for i in xrange(int0_TrailNumber):
            vc0_TrailForceOutUn = rh.Vector3d(vc1_TrailForceOut[i])
            rh.Vector3d.Unitize(vc0_TrailForceOutUn)
            ln0_TrailOut = rh.Line(pt1_InputNode[i],vc0_TrailForceOutUn)
            pt0_Node = pt1_InputNode[i] + vc0_TrailForceOutUn*db1_TrailLength[i]
            pt1_Node.append(pt0_Node)
            
            # Modify result in case of constraint planes
            if pl1_ConstraintPlane:
                if g != int0_LayerCount-1:
                    for j in xrange(len(id_NodePlane)):
                        if str(str1_NodeOrderC[((g+1)*int0_TrailNumber)+i]) == str(id_NodePlane[j]):
                            pl0_PlaneTrailOut = pl1_ConstraintPlane[j]
                            if pl0_PlaneTrailOut is not None:
                                xx1_Intersect = rh.Intersect.Intersection.LinePlane(ln0_TrailOut,pl0_PlaneTrailOut)
                                bl0_Intersect = xx1_Intersect[0]
                                db0_Intersect = xx1_Intersect[1]
                                if abs(db0_Intersect) < abs(db0_Threshold):
                                    db1_TrailLength[i] = 0.0
                                    pt0_Node = pt1_InputNode[i]
                                if bl0_Intersect and abs(db0_Intersect) > abs(db0_Threshold):
                                    pt0_Node = ln0_TrailOut.PointAt(db0_Intersect)
                                    db1_TrailLength[i] = pt1_InputNode[i].DistanceTo(pt0_Node)*db0_Intersect/abs(db0_Intersect)
                    pt1_Node[len(pt1_Node)-1] = pt0_Node
        
        # Build Trail Edges
        ln1_TrailEdge = []
        cl1_TrailEdge = []
        db1_TrailEdge = []
        
        for i in xrange(int0_TrailNumber):
            ln0_TrailEdge = rh.Line(pt1_InputNode[i],pt1_Node[i])
            ln1_TrailEdge.append(ln0_TrailEdge)
            if db1_TrailLength[i] > 0.0:
                cl1_TrailEdge.append(System.Drawing.Color.Red)
                db1_TrailEdge.append(vc1_TrailForceOut[i].Length)
            elif db1_TrailLength[i] < 0.0:
                cl1_TrailEdge.append(System.Drawing.Color.Blue)
                db1_TrailEdge.append(-vc1_TrailForceOut[i].Length)
            else:
                cl1_TrailEdge.append(System.Drawing.Color.Black)
                db1_TrailEdge.append(0.0)
            #db1_TrailEdge.append(abs(vc1_TrailForceOut[i].Length))


        # Build Deviation Edges
        ln1_Deviation1Edge = []
        cl1_Deviation1Edge = []
        db1_Deviation1Edge = []
        k = 3
        
        for i in xrange(g*int0_TrailNumber,(g+1)*int0_TrailNumber):
            k += 1
            for j in xrange(k,int0_TrailNumber+3):
                if db2_StructuralBehaviour[i][j] != 0:
                    ln0_Deviation1Edge = rh.Line(pt1_InputNode[i % int0_TrailNumber],pt1_InputNode[j-3])
                    ln1_Deviation1Edge.append(ln0_Deviation1Edge)
                    if db2_StructuralBehaviour[i][j] > 0.0:
                        cl1_Deviation1Edge.append(System.Drawing.Color.Red)
                    else:
                        cl1_Deviation1Edge.append(System.Drawing.Color.Blue)
                    #db1_Deviation1Edge.append(abs(db2_StructuralBehaviour[i][j]))
                    db1_Deviation1Edge.append(db2_StructuralBehaviour[i][j])
        vc2_GlobTrailForce.append(vc1_TrailForceOut)


        # Form Diagram
        ln2_GlobTrailEdge.append(ln1_TrailEdge)
        db2_GlobTrailEdge.append(db1_TrailEdge)
        cl2_GlobTrailEdge.append(cl1_TrailEdge)
        ln2_GlobDeviation1Edge.append(ln1_Deviation1Edge)
        cl2_GlobDeviation1Edge.append(cl1_Deviation1Edge)
        db2_GlobDeviation1Edge.append(db1_Deviation1Edge)
        ln2_GlobExtFOEdge.append(ln1_ExtFOEdge)
        cl2_GlobExtFOEdge.append(cl1_ExtFOEdge)
        db2_GlobExtFOEdge.append(db1_ExtFOEdge)
        pt2_GlobNode.append(pt1_Node)

        g += 1
    
    # Add Reactions to Form Diagram
    for i in xrange(len(vc2_GlobTrailForce[g-1])):
        if cl2_GlobTrailEdge[g-1][i] != System.Drawing.Color.Blue:
            ln1_ExtFOEdge.append(rh.Line(pt2_GlobNode[g-1][i],(pt2_GlobNode[g-1][i] + vc2_GlobTrailForce[g-1][i])))
            db1_ExtFOEdge.append(abs(ln1_ExtFOEdge[len(ln1_ExtFOEdge)-1].Length))
        else:
            ln1_ExtFOEdge.append(rh.Line((pt2_GlobNode[g-1][i] - vc2_GlobTrailForce[g-1][i]),pt2_GlobNode[g-1][i]))
            db1_ExtFOEdge.append(abs(ln1_ExtFOEdge[len(ln1_ExtFOEdge)-1].Length))
        cl1_ExtFOEdge.append(System.Drawing.Color.DarkGreen)
        
    # Update Counter
    int0_Counter += 1
    
    
    return


### MAIN FUNCTION
def Main(db1_StructuralBehaviour, str1_NodeOrderC, xx1_Bracing, pl1_ConstraintPlane, id_NodePlane, pt1_OriginNode, str1_Edge, db0_Divergence, db0_Threshold, int0_CounterBracing, int0_TrailNumber, int0_C, int0_R, db2_StructuralBehaviour, int0_LayerCount, db1_Variable, bl0_Print):

    ### GLOBAL VARIABLES
    
    global pt2_Trails
    global pt1_GlobNodeOut
    global ln1_GlobTrailEdgeOut
    global ln1_GlobDeviation1EdgeOut
    global ln1_GlobDeviation2EdgeOut
    global vc2_GlobTrailForce
    global ln2_GlobExtEdge
    global pt2_GlobNode
    global pt2_GlobNodeIteration
    global ln2_GlobTrailEdge
    global cl2_GlobTrailEdge
    global db2_GlobTrailEdge
    global ln2_GlobDeviation1Edge
    global cl2_GlobDeviation1Edge
    global db2_GlobDeviation1Edge
    global ln2_GlobDeviation2Edge
    global cl2_GlobDeviation2Edge
    global db2_GlobDeviation2Edge
    global ln2_GlobExtFOEdge
    global cl2_GlobExtFOEdge
    global db2_GlobExtFOEdge
    global int0_CounterOpt 
    global db0_DistanceBest
    global db1_VariableBest
    global str1_TrailEdgeID
    global str1_Dev1EdgeID
    global str1_Dev2EdgeID
    global int1_DevEdgeInputID
    global str0_GlobSolver
    global str0_GlobDivergence
    global str0_GlobIteration
    
    
    if bl0_Print:
        int0_CounterOpt += 1
        str0_DescriptionOpt = ""
        str0_DescriptionOpt += "\niteration: " + str(int0_CounterOpt)
    
    str0_GlobIteration = str(int0_CounterOpt)
    
    
    # Initialization of Nodes' Position
    for j in xrange(int0_LayerCount+1):
        pt1_GlobNodeIteration = []
        pt2_GlobNodeIteration.append(pt1_GlobNodeIteration)
    
    
    # Re-Inatialize Global Variables
    dbl0_Divergence = 0
    vc2_GlobTrailForce = []
    ln2_GlobExtEdge = []
    pt2_GlobNode = []
    ln2_GlobTrailEdge = []
    cl2_GlobTrailEdge = []
    db2_GlobTrailEdge = []
    ln2_GlobDeviation1Edge = []
    cl2_GlobDeviation1Edge = []
    db2_GlobDeviation1Edge = []
    ln2_GlobDeviation2Edge = []
    cl2_GlobDeviation2Edge = []
    db2_GlobDeviation2Edge = []
    ln2_GlobExtFOEdge = []
    cl2_GlobExtFOEdge = []
    db2_GlobExtFOEdge = []
    
    
    # Initial Check
    int0_StructuralLayersMatrix = int(len(db1_StructuralBehaviour)/(3+len(pt1_OriginNode)+1)/len(pt1_OriginNode))
    if db1_StructuralBehaviour == None or int0_StructuralLayersMatrix == 0:
        print(str("Please input Matrix of Structural Behaviour"))
        if len(pt1_OriginNode) == 0:
            print(str("Please input Origin Points"))
    else:
        if len(pt1_OriginNode) == 0:
            print(str("Please input Origin Points"))
        else:
            pt1_OriginNodeMod = [pt0_OriginNode for pt0_OriginNode in pt1_OriginNode]
            
            
            # Update Variables for Optimization
            if len(db1_Variable) > 0:
                int0_CountVar = 0
                
                for i in range(len(int2_Deviation1Edge)):
                    key1 = int2_Deviation1Edge[i][0] % int0_TrailNumber + 3
                    key0 = (int2_Deviation1Edge[i][0] // int0_TrailNumber)*int0_TrailNumber + int2_Deviation1Edge[i][1] - 3
                    db2_StructuralBehaviour[int2_Deviation1Edge[i][0]][int2_Deviation1Edge[i][1]] =  db1_Variable[int0_CountVar]
                    db2_StructuralBehaviour[key0][key1] = db1_Variable[int0_CountVar]
                    int0_CountVar += 1
                for i in range(len(int2_TrailEdge)):
                    db2_StructuralBehaviour[ int2_TrailEdge[i][0] ][ int2_TrailEdge[i][1]]  =  db1_Variable[int0_CountVar]
                    int0_CountVar += 1
                for i in range(2,len(xx1_Bracing),3):
                    xx1_Bracing[i] = db1_Variable[int0_CountVar]
                    int0_CountVar += 1
                for i in range(len(pt1_OriginNode)):
                    pt1_OriginNodeMod[i] = rh.Point3d(db1_Variable[int0_CountVar], pt1_OriginNode[i].Y, pt1_OriginNode[i].Z)
                    int0_CountVar += 1
                for i in range(len(pt1_OriginNode)):
                    pt1_OriginNodeMod[i] = rh.Point3d(pt1_OriginNodeMod[i].X, db1_Variable[int0_CountVar], pt1_OriginNode[i].Z)
                    int0_CountVar += 1
                for i in range(len(pt1_OriginNode)):
                    pt1_OriginNodeMod[i] = rh.Point3d(pt1_OriginNodeMod[i].X, pt1_OriginNodeMod[i].Y, db1_Variable[int0_CountVar])
                    int0_CountVar += 1

                    
                    
            # Start Iteration
            while int0_Counter < int0_CounterBracing and db0_Divergence > db0_Threshold:
                
                # Call Main Function
                Equilibrium(db1_StructuralBehaviour, xx1_Bracing, pt1_OriginNodeMod, pl1_ConstraintPlane)
                
                # Store Nodes' Position
                # Here the original line was:
                # pt2_GlobNodeIteration[0] = pt1_OriginNode
                
                pt2_GlobNodeIteration[0] = pt1_OriginNodeMod
                
                for j in xrange(1,len(pt2_GlobNode)+1):
                    if int0_Counter-1 != 0:
                        db0_Divergence = 0
                        for k in xrange(len(pt2_GlobNode[j-1])):
                            db0_Divergence += pt2_GlobNode[j-1][k].DistanceTo(pt2_GlobNodeIteration[j][k])
                    pt2_GlobNodeIteration[j] = pt2_GlobNode[j-1]
                
                if bl0_Print:
                    str0_Description = ""
                    
                    str0_Description += "sub-iteration: " + str(int0_Counter) + "\n"
                    if len(xx1_Bracing) == 0:
                        db0_Divergence = 0.00
                    str0_Description += "divergence: " + str(db0_Divergence)
                    
                    print str0_Description

                
                if int0_Counter < int0_CounterBracing and db0_Divergence > db0_Threshold:
                    # Re-Inatialize Global Variables
                    dbl0_Divergence = 0
                    vc2_GlobTrailForce = []
                    ln2_GlobExtEdge = []
                    pt2_GlobNode = []
                    ln2_GlobTrailEdge = []
                    cl2_GlobTrailEdge = []
                    db2_GlobTrailEdge = []
                    ln2_GlobDeviation1Edge = []
                    cl2_GlobDeviation1Edge = []
                    db2_GlobDeviation1Edge = []
                    ln2_GlobDeviation2Edge = []
                    cl2_GlobDeviation2Edge = []
                    db2_GlobDeviation2Edge = []
                    ln2_GlobExtFOEdge = []
                    cl2_GlobExtFOEdge = []
                    db2_GlobExtFOEdge = []
    
                if int0_Counter == int0_CounterBracing or db0_Divergence < db0_Threshold:
                    
                    # Add Bracing
                    ln1_Deviation2Edge = []
                    cl1_Deviation2Edge = []
                    db1_Deviation2Edge = []
                    for i in xrange(0,len(xx1_Bracing),3):
                        int0_BracingFromLayerIndex = int(xx1_Bracing[i]) // int0_TrailNumber
                        int0_BracingFromTrailIndex = int(xx1_Bracing[i]) % int0_TrailNumber
                        int0_BracingToLayerIndex = int(xx1_Bracing[i+1]) // int0_TrailNumber
                        int0_BracingToTrailIndex = int(xx1_Bracing[i+1]) % int0_TrailNumber
                        ln0_Deviation2Edge = rh.Line(pt2_GlobNodeIteration[int0_BracingFromLayerIndex][int0_BracingFromTrailIndex],pt2_GlobNodeIteration[int0_BracingToLayerIndex][int0_BracingToTrailIndex])
                        ln1_Deviation2Edge.append(ln0_Deviation2Edge)
                        if float(xx1_Bracing[i+2]) > 0.0:
                            cl1_Deviation2Edge.append(System.Drawing.Color.Red)
                        elif float(xx1_Bracing[i+2]) < 0.0:
                            cl1_Deviation2Edge.append(System.Drawing.Color.Blue)
                        else:
                            cl1_Deviation2Edge.append(System.Drawing.Color.Black)
                        db1_Deviation2Edge.append(xx1_Bracing[i+2])
                        
                        
                    ### OUTPUT
    
                    ln1_GlobExtEdgeOut = ListListToList(ln2_GlobExtEdge)
                    pt1_GlobNodeOut = ListListToList(pt2_GlobNodeIteration)
                    ln1_GlobTrailEdgeOut = ListListToList(ln2_GlobTrailEdge)
                    cl1_GlobTrailEdgeOut = ListListToList(cl2_GlobTrailEdge)
                    db1_GlobTrailEdgeOut = ListListToList(db2_GlobTrailEdge)
                    ln1_GlobDeviation1EdgeOut = ListListToList(ln2_GlobDeviation1Edge)
                    cl1_GlobDeviation1EdgeOut = ListListToList(cl2_GlobDeviation1Edge)
                    db1_GlobDeviation1EdgeOut = ListListToList(db2_GlobDeviation1Edge)
                    ln1_GlobDeviation2EdgeOut = ln1_Deviation2Edge
                    cl1_GlobDeviation2EdgeOut = cl1_Deviation2Edge
                    db1_GlobDeviation2EdgeOut = db1_Deviation2Edge
                    ln1_GlobDeviationEdgeOut = ln1_GlobDeviation1EdgeOut[:]
                    ln1_GlobDeviationEdgeOut.extend(ln1_GlobDeviation2EdgeOut)
                    str1_GlobDeviationEdgeOut = str1_Dev1EdgeID[:]
                    str1_GlobDeviationEdgeOut.extend(str1_Dev2EdgeID)
                    cl1_GlobDeviationEdgeOut = cl1_GlobDeviation1EdgeOut[:]
                    cl1_GlobDeviationEdgeOut.extend(cl1_GlobDeviation2EdgeOut)
                    db1_GlobDeviationEdgeOut = db1_GlobDeviation1EdgeOut[:]
                    db1_GlobDeviationEdgeOut.extend(db1_GlobDeviation2EdgeOut)
                    int1_DevEdgeInputSortID = int1_DevEdgeInputID[:]
                    if len(str1_GlobDeviationEdgeOut) > 0:
                        str1_GlobDeviationEdgeOut, ln1_GlobDeviationEdgeOut, cl1_GlobDeviationEdgeOut, db1_GlobDeviationEdgeOut = (list(t) for t in zip(*sorted(zip(str1_GlobDeviationEdgeOut, ln1_GlobDeviationEdgeOut, cl1_GlobDeviationEdgeOut, db1_GlobDeviationEdgeOut))))
                        int1_DevEdgeInputSortID, ln1_GlobDeviationEdgeOut, str1_GlobDeviationEdgeOut, cl1_GlobDeviationEdgeOut, db1_GlobDeviationEdgeOut = (list(t) for t in zip(*sorted(zip(int1_DevEdgeInputSortID, ln1_GlobDeviationEdgeOut, str1_GlobDeviationEdgeOut, cl1_GlobDeviationEdgeOut, db1_GlobDeviationEdgeOut))))
                    ln1_GlobExtFOEdgeOut = ListListToList(ln2_GlobExtFOEdge)
                    cl1_GlobExtFOEdgeOut = ListListToList(cl2_GlobExtFOEdge)
                    db1_GlobExtFOEdgeOut = ListListToList(db2_GlobExtFOEdge)
                    M.ln1_GlobExtEdgeOut = ln1_GlobExtEdgeOut
                    M.pt1_GlobNodeOut = pt1_GlobNodeOut[:len(str1_NodeOrderC)]
                    M.ln1_GlobTrailEdgeOut = ln1_GlobTrailEdgeOut[:len(str1_TrailEdgeID)]
                    M.str1_GlobTrailEdgeOut = str1_TrailEdgeID
                    M.cl1_GlobTrailEdgeOut = cl1_GlobTrailEdgeOut[:len(str1_TrailEdgeID)]
                    M.db1_GlobTrailEdgeOut = db1_GlobTrailEdgeOut[:len(str1_TrailEdgeID)]
                    M.ln1_GlobDeviation1EdgeOut = ln1_GlobDeviation1EdgeOut
                    M.str1_GlobDeviation1EdgeOut = str1_Dev1EdgeID
                    M.cl1_GlobDeviation1EdgeOut = cl1_GlobDeviation1EdgeOut
                    M.db1_GlobDeviation1EdgeOut = db1_GlobDeviation1EdgeOut
                    M.ln1_GlobDeviation2EdgeOut = ln1_GlobDeviation2EdgeOut
                    M.str1_GlobDeviation2EdgeOut = str1_Dev2EdgeID
                    M.cl1_GlobDeviation2EdgeOut = cl1_GlobDeviation2EdgeOut
                    M.db1_GlobDeviation2EdgeOut = db1_GlobDeviation2EdgeOut
                    M.ln1_GlobDeviationEdgeOut = ln1_GlobDeviationEdgeOut
                    M.str1_GlobDeviationEdgeOut = str1_GlobDeviationEdgeOut
                    M.cl1_GlobDeviationEdgeOut = cl1_GlobDeviationEdgeOut
                    M.db1_GlobDeviationEdgeOut = db1_GlobDeviationEdgeOut
                    M.ln1_GlobExtFOEdgeOut = ln1_GlobExtFOEdgeOut
                    M.cl1_GlobExtFOEdgeOut = cl1_GlobExtFOEdgeOut
                    M.db1_GlobExtFOEdgeOut = db1_GlobExtFOEdgeOut
                    M.str1_NodeOrderOut = str1_NodeOrderC
                    M.str1_EdgeOut = str1_Edge

    global int0_Counter
    int0_Counter = 0
    
    db0_Distance = 0

    if targetNode and targetNodeID:
        db0_DistanceGeometry = 0
        for i in xrange(0,len(targetNodeID)): 
            if str(targetNodeID[i]) in str1_NodeOrderC:
                int0_IndexGlobNode = int(str1_NodeOrderC.index(str(targetNodeID[i])))
                pt0_GlobNode = pt2_GlobNode[int0_IndexGlobNode // int0_TrailNumber - 1][int0_IndexGlobNode % int0_TrailNumber]
                targetNode0 = pt0_GlobNode
                if isinstance(targetNode[i], rh.Curve):
                    targetNode0 = targetNode[i].PointAt( targetNode[i].ClosestPoint(pt0_GlobNode)[1] )
                elif isinstance(targetNode[i], rh.Brep) or isinstance(targetNode[i], rh.BrepFace):
                    targetNode[i] = rs.coercesurface(targetNode[i])
                    targetNode0 = targetNode[i].PointAt( targetNode[i].ClosestPoint(pt0_GlobNode)[1], targetNode[i].ClosestPoint(pt0_GlobNode)[2] )
                elif isinstance(targetNode[i], rh.Point3d):
                    targetNode0 = targetNode[i]
                db0_DistanceGeometry += targetNodeCoeff*pt0_GlobNode.DistanceToSquared(targetNode0)
        db0_Distance += targetNodeCoeff*db0_DistanceGeometry

    if targetVector and targetVectorID:
        db0_DistanceVectorDir = 0
        db0_DistanceVectorMag = 0
        for i in xrange(0,len(targetVectorID)):
            if str(targetVectorID[i]) in str1_NodeOrderC:
                int0_IndexGlobNode = int(str1_NodeOrderC.index(str(targetVectorID[i])))
                vc0_GlobVector = vc2_GlobTrailForce[int0_IndexGlobNode // int0_TrailNumber][int0_IndexGlobNode % int0_TrailNumber]
                targetVector0 = vc0_GlobVector
                if isinstance(targetVector[i], rh.Vector3d):
                    targetVector0 = targetVector[i]
                db0_DistanceVectorMag += (vc0_GlobVector.Length - targetVector0.Length)**2
                vc0_GlobVectorU = rh.Vector3d(vc0_GlobVector)
                targetVector0U = rh.Vector3d(targetVector0)
                vc0_GlobVectorU.Unitize()
                targetVector0U.Unitize()
                db0_DistanceVectorDir += ((1- abs(rh.Vector3d.Multiply(vc0_GlobVectorU,targetVector0U)))**2)
        db0_Distance = db0_Distance + targetVectorCoeffMag*db0_DistanceVectorMag + targetVectorCoeffDir*db0_DistanceVectorDir

    if bl0_Print:
        str0_DescriptionOpt += "\nobjective: " + str(db0_Distance)
        str0_DescriptionOpt += "\n\n\n "
        print str0_DescriptionOpt
    
    global GlobDivergence
    str0_GlobDivergence = str(int(db0_Distance*1E5)/1E5)
    
    if db0_Distance < db0_DistanceBest:
        db0_DistanceBest = db0_Distance
        db1_VariableBest = db1_Variable
        
    return(db0_Distance)

pt2_Trails = []


M = model()



if TPC and hasattr(TPC,"db1_StructuralBehaviourOut"):

    vc2_GlobTrailForce = []
    ln2_GlobExtEdge = []
    pt2_GlobNode = []
    pt2_GlobNodeIteration = []
    ln2_GlobTrailEdge = []
    cl2_GlobTrailEdge = []
    db2_GlobTrailEdge = []
    ln2_GlobDeviation1Edge = []
    cl2_GlobDeviation1Edge = []
    db2_GlobDeviation1Edge = []
    ln2_GlobDeviation2Edge = []
    cl2_GlobDeviation2Edge = []
    db2_GlobDeviation2Edge = []
    ln2_GlobExtFOEdge = []
    cl2_GlobExtFOEdge = []
    db2_GlobExtFOEdge = []
    
    
    db1_StructuralBehaviour = TPC.db1_StructuralBehaviourOut
    str1_NodeOrderC = TPC.str1_NodeOrderOut
    xx1_Bracing = TPC.db1_DeviationIndirectOut
    pl1_ConstraintPlane = TPC.pl1_ConstraintPlaneOut
    id_NodePlane = TPC.int1_ConstraintPlaneOut
    pt1_OriginNode = TPC.pt1_OriginNodeOut
    str1_Edge = TPC.str1_EdgeOut
    
    # Counters and Tolerance
    int0_Counter = 0
    db0_Divergence = float("inf")
    db0_Threshold = 1e-3
    int0_CounterBracing = 50
    db0_DistanceBest = float("inf")
    db1_VariableBest = []

    if len(xx1_Bracing) == 0: int0_CounterBracing = 1

    int0_TrailNumber = len(pt1_OriginNode)  # input nodes
    int0_C = 3+int0_TrailNumber+1
    int0_R = int(len(db1_StructuralBehaviour)/int0_C)
    db2_StructuralBehaviour = ListToListList(db1_StructuralBehaviour, int0_R, int0_C)
    int0_LayerCount = int(len(db2_StructuralBehaviour)/int0_TrailNumber) # amount of layers
    
    
    # Variables for Optimization
    
    # Deviation 1
    int2_Deviation1Edge = []
    db1_Deviation1Edge = []
    for g in xrange(int0_LayerCount):
        k = 3
        for i in xrange(g*int0_TrailNumber,(g+1)*int0_TrailNumber):
            k += 1
            for j in xrange(k,int0_TrailNumber+3):
                if db2_StructuralBehaviour[i][j] != 0:
                    int2_Deviation1Edge.append((i,j))
                    db1_Deviation1Edge.append(db2_StructuralBehaviour[i][j])
    # Trail
    int2_TrailEdge = []
    db1_TrailEdge = []
    for g in xrange(int0_LayerCount-1):
        for i in xrange(int0_TrailNumber):
            int2_TrailEdge.append([g*int0_TrailNumber + i,int0_TrailNumber+3]) 
            db1_TrailEdge.append(db2_StructuralBehaviour[g*int0_TrailNumber + i][int0_TrailNumber+3])

    # Deviation 2
    db1_Deviation2Edge = []
    for i in range(2,len(xx1_Bracing),3):
        db1_Deviation2Edge.append(xx1_Bracing[i])

    # Origin Nodes
    db1_OriginNodeX = [pt0_OriginNode.X for pt0_OriginNode in pt1_OriginNode]
    db1_OriginNodeY = [pt0_OriginNode.Y for pt0_OriginNode in pt1_OriginNode]
    db1_OriginNodeZ = [pt0_OriginNode.Z for pt0_OriginNode in pt1_OriginNode]

    int0_CounterOpt = 0
    print "Iteration report\n\n "

    # Calculate gradient
    def Grad(var, grad):
        if grad:
            global db0_Dx
            fX_0 = Main(db1_StructuralBehaviour, str1_NodeOrderC, xx1_Bracing, pl1_ConstraintPlane, id_NodePlane, pt1_OriginNode, str1_Edge, db0_Divergence, db0_Threshold, int0_CounterBracing, int0_TrailNumber, int0_C, int0_R, db2_StructuralBehaviour, int0_LayerCount, var, False)
            for i in range(len(var)):
                varDx = var[:]
                varDx[i] += db0_Dx
                if db1_BoundUp[i] != db1_BoundLow[i]:
                    fX_1 = Main(db1_StructuralBehaviour, str1_NodeOrderC, xx1_Bracing, pl1_ConstraintPlane, id_NodePlane, pt1_OriginNode, str1_Edge, db0_Divergence, db0_Threshold, int0_CounterBracing, int0_TrailNumber, int0_C, int0_R, db2_StructuralBehaviour, int0_LayerCount, varDx, False)
                    dfX_1 = (fX_1 - fX_0) / db0_Dx
                else: dfX_1 = 0.0 
                grad[i] = dfX_1
        out = Main(db1_StructuralBehaviour, str1_NodeOrderC, xx1_Bracing, pl1_ConstraintPlane, id_NodePlane, pt1_OriginNode, str1_Edge, db0_Divergence, db0_Threshold, int0_CounterBracing, int0_TrailNumber, int0_C, int0_R, db2_StructuralBehaviour, int0_LayerCount, var, True)
        return out

    # Optimization function
    def Optimization(db1_InitialValues, db1_BoundUp, db1_BoundLow, db0_T, int0_I, nl0_Algo):
        solver = nl.NLoptSolver(nl0_Algo, len(db1_InitialValues), db0_T, int0_I)
        solver.SetLowerBounds(Array[float]( db1_BoundLow ))
        solver.SetUpperBounds(Array[float]( db1_BoundUp ))
        solver.SetMinObjective.Overloads[Func[Array[float], Array[float], float]](Grad)
        initialValue = Array[float](db1_InitialValues)
        out, finalScore = solver.Optimize(initialValue)
        return finalScore
    
    global str0_GlobSolver
    str0_GlobSolver = "None"
    
    if O and (hasattr(O, "targetNode") and hasattr(O, "targetNodeID") or hasattr(O, "targetVector") and hasattr(O, "targetVectorID")):
        int1_T_ID = O.boundsTrailID
        db1_T_Up = O.boundsTrailUp
        db1_T_Low = O.boundsTrailLow
        
        int1_D_ID = O.boundsDevID
        db1_D_Up = O.boundsDevUp
        db1_D_Low = O.boundsDevLow

        int1_O_ID = O.boundsOriginNodeID
        db1_O_UpX = O.boundsOriginNodeUpX 
        db1_O_LowX = O.boundsOriginNodeLowX
        db1_O_UpY = O.boundsOriginNodeUpY
        db1_O_LowY = O.boundsOriginNodeLowY
        db1_O_UpZ = O.boundsOriginNodeUpZ
        db1_O_LowZ = O.boundsOriginNodeLowZ
        
        global db0_Dx
        db0_Dx = O.gradientDelta
        db0_T = O.relativeTolerance
        int0_I = O.maxIterations
        str0_A = O.optimAlgorithm
        str0_GlobSolver = str0_A

        dc1_Algo = {"LD_SLSQP" : nl.NLoptAlgorithm.LD_SLSQP,
                    "LN_BOBYQA" : nl.NLoptAlgorithm.LN_BOBYQA,
                    "GD_MLSL" : nl.NLoptAlgorithm.GD_MLSL,
                    "LD_LBFGS" : nl.NLoptAlgorithm.LD_LBFGS,
                    "LD_AUGLAG" : nl.NLoptAlgorithm.LD_AUGLAG,
                    "LN_SBPLX" : nl.NLoptAlgorithm.LN_SBPLX,
                    "LN_COBYLA" : nl.NLoptAlgorithm.LN_COBYLA,
                    "LD_TNEWTON" : nl.NLoptAlgorithm.LD_TNEWTON,
                    "GN_ISRES" : nl.NLoptAlgorithm.GN_ISRES,
                    "GN_MLSL" : nl.NLoptAlgorithm.GN_MLSL}


        db1_TrailBoundUp = db1_TrailEdge[:]

        for i in range(len(int1_T_ID)):
            if str(int1_T_ID[i]) in str1_TrailEdgeID: db1_TrailBoundUp[ str1_TrailEdgeID.index(str(int1_T_ID[i])) ] += db1_T_Up[i]
        db1_TrailBoundLow = db1_TrailEdge[:]
        for i in range(len(int1_T_ID)):
            if str(int1_T_ID[i]) in str1_TrailEdgeID: db1_TrailBoundLow[ str1_TrailEdgeID.index(str(int1_T_ID[i])) ] += db1_T_Low[i]

        db1_Deviation1BoundUp = db1_Deviation1Edge[:]
        for i in range(len(int1_D_ID)):
            if str(int1_D_ID[i]) in str1_Dev1EdgeID: db1_Deviation1BoundUp[ str1_Dev1EdgeID.index(str(int1_D_ID[i])) ] += db1_D_Up[i]
        db1_Deviation1BoundLow = db1_Deviation1Edge[:]
        for i in range(len(int1_D_ID)):
           if str(int1_D_ID[i]) in str1_Dev1EdgeID: db1_Deviation1BoundLow[ str1_Dev1EdgeID.index(str(int1_D_ID[i])) ] += db1_D_Low[i]

        db1_Deviation2BoundUp = db1_Deviation2Edge[:]
        for i in range(len(int1_D_ID)):
            if str(int1_D_ID[i]) in str1_Dev2EdgeID: db1_Deviation2BoundUp[ str1_Dev2EdgeID.index(str(int1_D_ID[i])) ] += db1_D_Up[i]
        db1_Deviation2BoundLow = db1_Deviation2Edge[:]
        for i in range(len(int1_D_ID)):
            if str(int1_D_ID[i]) in str1_Dev2EdgeID: db1_Deviation2BoundLow[ str1_Dev2EdgeID.index(str(int1_D_ID[i])) ] += db1_D_Low[i]

        db1_OriginNodeXBoundUp = db1_OriginNodeX[:]
        str1_OriginNode = str1_NodeOrderC[:len(pt1_OriginNode)]
        for i in range(len(str1_OriginNode)):
            str1_OriginNode[i] = str1_OriginNode[i].replace("L","")

        for i in range(len(int1_O_ID)):
            if str(int1_O_ID[i]) in str1_OriginNode: db1_OriginNodeXBoundUp[ str1_OriginNode.index(str(int1_O_ID[i])) ] += db1_O_UpX[i]
        db1_OriginNodeXBoundLow = db1_OriginNodeX[:]
        for i in range(len(int1_O_ID)):
            if str(int1_O_ID[i]) in str1_OriginNode: db1_OriginNodeXBoundLow[ str1_OriginNode.index(str(int1_O_ID[i])) ] += db1_O_LowX[i]
        db1_OriginNodeYBoundUp = db1_OriginNodeY[:]
        for i in range(len(int1_O_ID)):
            if str(int1_O_ID[i]) in str1_OriginNode: db1_OriginNodeYBoundUp[ str1_OriginNode.index(str(int1_O_ID[i])) ] += db1_O_UpY[i]
        db1_OriginNodeYBoundLow = db1_OriginNodeY[:]
        for i in range(len(int1_O_ID)):
            if str(int1_O_ID[i]) in str1_OriginNode: db1_OriginNodeYBoundLow[ str1_OriginNode.index(str(int1_O_ID[i])) ] += db1_O_LowY[i]
        db1_OriginNodeZBoundUp = db1_OriginNodeZ[:]
        for i in range(len(int1_O_ID)):
            if str(int1_O_ID[i]) in str1_OriginNode: db1_OriginNodeZBoundUp[ str1_OriginNode.index(str(int1_O_ID[i])) ] += db1_O_UpZ[i]
        db1_OriginNodeZBoundLow = db1_OriginNodeZ[:]
        for i in range(len(int1_O_ID)):
            if str(int1_O_ID[i]) in str1_OriginNode: db1_OriginNodeZBoundLow[ str1_OriginNode.index(str(int1_O_ID[i])) ] += db1_O_LowZ[i]

        # Define Initial Values for Optimization
        db1_InitialValues = []
        db1_InitialValues = db1_Deviation1Edge[:]
        db1_InitialValues.extend(db1_TrailEdge[:])
        db1_InitialValues.extend(db1_Deviation2Edge[:])
        db1_InitialValues.extend(db1_OriginNodeX[:])
        db1_InitialValues.extend(db1_OriginNodeY[:])
        db1_InitialValues.extend(db1_OriginNodeZ[:])

        # Define Bounds for Optimization
        db1_BoundUp = []
        db1_BoundUp = db1_Deviation1BoundUp[:]
        db1_BoundUp.extend(db1_TrailBoundUp[:])
        db1_BoundUp.extend(db1_Deviation2BoundUp[:])
        db1_BoundUp.extend(db1_OriginNodeXBoundUp[:])
        db1_BoundUp.extend(db1_OriginNodeYBoundUp[:])
        db1_BoundUp.extend(db1_OriginNodeZBoundUp[:])
        db1_BoundLow = []
        db1_BoundLow = db1_Deviation1BoundLow[:]
        db1_BoundLow.extend(db1_TrailBoundLow[:])
        db1_BoundLow.extend(db1_Deviation2BoundLow[:])
        db1_BoundLow.extend(db1_OriginNodeXBoundLow[:])
        db1_BoundLow.extend(db1_OriginNodeYBoundLow[:])
        db1_BoundLow.extend(db1_OriginNodeZBoundLow[:])

        Optimization(db1_InitialValues, db1_BoundUp, db1_BoundLow, db0_T, int0_I, dc1_Algo[str0_A])
        
        Main(db1_StructuralBehaviour, str1_NodeOrderC, xx1_Bracing, pl1_ConstraintPlane, id_NodePlane, pt1_OriginNode, str1_Edge, db0_Divergence, db0_Threshold, int0_CounterBracing, int0_TrailNumber, int0_C, int0_R, db2_StructuralBehaviour, int0_LayerCount, db1_VariableBest, True)
    else:
        Main(db1_StructuralBehaviour, str1_NodeOrderC, xx1_Bracing, pl1_ConstraintPlane, id_NodePlane, pt1_OriginNode, str1_Edge, db0_Divergence, db0_Threshold, int0_CounterBracing, int0_TrailNumber, int0_C, int0_R, db2_StructuralBehaviour, int0_LayerCount, [], True)
