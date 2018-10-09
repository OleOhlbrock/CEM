"""
Calculate the structural model
    Inputs:
        TPC: (topological diagram) The topological diagram used for the calculation of the structural model
        selfWeight: (bool) Activate the self weight of the structure
        yieldStress: (double) The yield stress of the structural members
        specWeight: (double) The specific weight of the structural members
    Outputs:
        M: (structural model) The calculated structural model (empty model on error)
    Remarks:
        This generates a new instance of the structural model for a given topological diagram
"""

__author__    = ['Patrick Ole Ohlbrock','Pierluigi D''Acunto' ]
__copyright__ = 'Copyright 2018 - Chair of Structural Design, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'ohlbrock@arch.ethz.ch'
__version__   = "1.00"

"""
If you use the library of CEM in a project, please refer to the CEM GitHub repository:
@misc{cem-dev,
    title  = {{CEM}: Combinatorial Equilibrium Modeling},
    author = {Patrick Ole Ohlbrock and Pierluigi D'Acunto},
    note   = {https://github.com/OleOhlbrock/CEM},
    year   = {2018},
}
"""


import Rhino.Geometry as rh
import rhinoscriptsyntax as rs
import math
import System.Drawing.Color
import copy
import time


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



import copy
TPC = copy.deepcopy(TP)

if TPC and hasattr(TPC, "db1_StructuralBehaviourOut"):
    if constraintPlane and constraintPlane:
        if len(constraintPlane) == len(constraintPlane):
            TPC.pl1_ConstraintPlaneOut = constraintPlane
            TPC.int1_ConstraintPlaneOut = constraintPlaneID
        else:
            TPC.pl1_ConstraintPlaneOut = None
            TPC.int1_ConstraintPlaneOut = None
    else:
        TPC.pl1_ConstraintPlaneOut = None
        TPC.int1_ConstraintPlaneOut = None
    
    if originNode:
        if len(originNode) == len(TP.pt1_OriginNodeOut):
            TPC.pt1_OriginNodeOut = originNode







M = model()

if TPC and hasattr(TPC, "db1_StructuralBehaviourOut"):
    
    db1_StructuralBehaviour = TPC.db1_StructuralBehaviourOut
    str1_NodeOrderC = TPC.str1_NodeOrderOut
    xx1_Bracing = TPC.db1_DeviationIndirectOut
    pl1_ConstraintPlane = TPC.pl1_ConstraintPlaneOut
    id_NodePlane = TPC.int1_ConstraintPlaneOut
    pt1_OriginNode = TPC.pt1_OriginNodeOut
    str1_Edge = TPC.str1_EdgeOut
    

    ### GLOBAL VARIABLES
    
    # Counters and Tolerance
    int0_Counter = 0
    db0_Divergence = float("inf")
    db0_Threshold = 1e-10
    int0_CounterBracing = 100
    
    int0_TrailNumber = len(pt1_OriginNode)  # input nodes
    int0_C = 3+int0_TrailNumber+1
    int0_R = int(len(db1_StructuralBehaviour)/int0_C)
    db2_StructuralBehaviour = ListToListList(db1_StructuralBehaviour, int0_R, int0_C)
    int0_LayerCount = int(len(db2_StructuralBehaviour)/int0_TrailNumber) # amount of layers
    
    # Global Variables
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
    
    
    ### MAIN FUNCTION
    
    def Main(db1_StructuralBehaviour, xx1_Bracing, pt1_OriginNode, pl1_ConstraintPlane):
        
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
        
            ### LAYER DEVELOPMENT
            
            ## Initialize Layer
            
            # Create Deviation Length and Unit Vector Matrix
            vc2_DevLengthVector = []
            vc2_DevUnitVector = []
            
            for i in xrange(int0_TrailNumber):
                vc1_DevLengthVector = []
                vc1_DevUnitVector = []
                for j in xrange(int0_TrailNumber):
                    vc0_DevLengthVector = rh.Vector3d(pt1_InputNode[j]-pt1_InputNode[i])
                    vc0_DevUnitVector = rh.Vector3d(vc0_DevLengthVector)
                    rh.Vector3d.Unitize(vc0_DevUnitVector)
                    vc1_DevLengthVector.append(vc0_DevLengthVector)
                    vc1_DevUnitVector.append(vc0_DevUnitVector)
                vc2_DevLengthVector.append(vc1_DevLengthVector)
                vc2_DevUnitVector.append(vc1_DevUnitVector)
            
            
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
                    db0_DevStatAct = abs((vc2_DevLengthVector[i][j]*db2_DevForceMag[i][j]).Length)
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
            if selfWeight and specWeight and yieldStress:
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
                db1_IndDevStatActSum = 0
            # Construct Equilibrium per each Node
            vc1_TrailForceOut = []
            vc1_SelfWeight = []
            for i in xrange(int0_TrailNumber):
                if int0_Counter == 0:
                    db1_IndDevStatActSum = [0.0 for i in range(int0_TrailNumber)]
                if selfWeight and specWeight and yieldStress:
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
                            if int(str1_NodeOrderC[((g+1)*int0_TrailNumber)+i]) == int(id_NodePlane[j]):
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
                if db1_TrailLength[i] > 0:
                    cl1_TrailEdge.append(System.Drawing.Color.Red)
                elif db1_TrailLength[i] < 0:
                    cl1_TrailEdge.append(System.Drawing.Color.Blue)
                else:
                    cl1_TrailEdge.append(System.Drawing.Color.Black)
                db1_TrailEdge.append(abs(vc1_TrailForceOut[i].Length))
    
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
                        if db2_StructuralBehaviour[i][j] > 0:
                            cl1_Deviation1Edge.append(System.Drawing.Color.Red)
                        else:
                            cl1_Deviation1Edge.append(System.Drawing.Color.Blue)
                        db1_Deviation1Edge.append(abs(db2_StructuralBehaviour[i][j]))
            
            vc2_GlobTrailForce.append(vc1_TrailForceOut)
            
            # Form Diagram
            ln2_GlobTrailEdge.append(ln1_TrailEdge)
            db2_GlobTrailEdge.append(db1_TrailEdge)
            ln2_GlobDeviation1Edge.append(ln1_Deviation1Edge)
            cl2_GlobDeviation1Edge.append(cl1_Deviation1Edge)
            db2_GlobDeviation1Edge.append(db1_Deviation1Edge)
            ln2_GlobExtFOEdge.append(ln1_ExtFOEdge)
            cl2_GlobExtFOEdge.append(cl1_ExtFOEdge)
            db2_GlobExtFOEdge.append(db1_ExtFOEdge)
            pt2_GlobNode.append(pt1_Node)
            cl2_GlobTrailEdge.append(cl1_TrailEdge)
    
            g += 1
        
        # Add Reactions to Form Diagram
        for i in xrange(len(vc2_GlobTrailForce[g-1])):
            if selfWeight and specWeight and yieldStress:
                vc0_SelfWeight = (abs(vc2_GlobTrailForce[g-1][i].Length*ln2_GlobTrailEdge[g-1][i].Length)*specWeight/yieldStress)*(-rh.Vector3d.ZAxis)
                if cl2_GlobTrailEdge[g-1][i] != System.Drawing.Color.Blue:
                    ln1_ExtFOEdge.append(rh.Line(pt2_GlobNode[g-1][i],(pt2_GlobNode[g-1][i] + vc2_GlobTrailForce[g-1][i] + vc0_SelfWeight)))
                    db1_ExtFOEdge.append(abs(ln1_ExtFOEdge[len(ln1_ExtFOEdge)-1].Length))
                else:
                    ln1_ExtFOEdge.append(rh.Line((pt2_GlobNode[g-1][i] - vc2_GlobTrailForce[g-1][i] + vc0_SelfWeight),pt2_GlobNode[g-1][i]))
                    db1_ExtFOEdge.append(abs(ln1_ExtFOEdge[len(ln1_ExtFOEdge)-1].Length))
            else:
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
    
    # Initialization of Nodes' Position
    
    for j in xrange(int0_LayerCount+1):
        pt1_GlobNodeIteration = []
        pt2_GlobNodeIteration.append(pt1_GlobNodeIteration)
    
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
            print("Iteration report")
    
            # Start Iteration
            while int0_Counter < int0_CounterBracing and db0_Divergence > db0_Threshold:
                
                # Call Main Function
                Main(db1_StructuralBehaviour, xx1_Bracing, pt1_OriginNode, pl1_ConstraintPlane)
                
                # Store Nodes' Position
                pt2_GlobNodeIteration[0] = pt1_OriginNode
                for j in xrange(1,len(pt2_GlobNode)+1):
                    if int0_Counter-1 != 0:
                        db0_Divergence = 0
                        for k in xrange(len(pt2_GlobNode[j-1])):
                            db0_Divergence += pt2_GlobNode[j-1][k].DistanceTo(pt2_GlobNodeIteration[j][k])
                    pt2_GlobNodeIteration[j] = pt2_GlobNode[j-1]
                
                print(str(int0_Counter))
                print(str(db0_Divergence))
                print(str("______"))
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
                        if float(xx1_Bracing[i+2]) > 0:
                            cl1_Deviation2Edge.append(System.Drawing.Color.Red)
                        elif float(xx1_Bracing[i+2]) < 0:
                            cl1_Deviation2Edge.append(System.Drawing.Color.Blue)
                        else:
                            cl1_Deviation2Edge.append(System.Drawing.Color.Black)
                        db1_Deviation2Edge.append(xx1_Bracing[i+2])
    
                    ### OUTMUT
    
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
                    ln1_GlobExtFOEdgeOut = ListListToList(ln2_GlobExtFOEdge)
                    cl1_GlobExtFOEdgeOut = ListListToList(cl2_GlobExtFOEdge)
                    db1_GlobExtFOEdgeOut = ListListToList(db2_GlobExtFOEdge)
                    
                    M.ln1_GlobExtEdgeOut = ln1_GlobExtEdgeOut
                    M.pt1_GlobNodeOut = pt1_GlobNodeOut
                    M.ln1_GlobTrailEdgeOut = ln1_GlobTrailEdgeOut
                    M.cl1_GlobTrailEdgeOut = cl1_GlobTrailEdgeOut
                    M.db1_GlobTrailEdgeOut = db1_GlobTrailEdgeOut
                    M.ln1_GlobDeviation1EdgeOut = ln1_GlobDeviation1EdgeOut
                    M.cl1_GlobDeviation1EdgeOut = cl1_GlobDeviation1EdgeOut
                    M.db1_GlobDeviation1EdgeOut = db1_GlobDeviation1EdgeOut
                    M.ln1_GlobDeviation2EdgeOut = ln1_GlobDeviation2EdgeOut
                    M.cl1_GlobDeviation2EdgeOut = cl1_GlobDeviation2EdgeOut
                    M.db1_GlobDeviation2EdgeOut = db1_GlobDeviation2EdgeOut
                    M.ln1_GlobExtFOEdgeOut = ln1_GlobExtFOEdgeOut
                    M.cl1_GlobExtFOEdgeOut = cl1_GlobExtFOEdgeOut
                    M.db1_GlobExtFOEdgeOut = db1_GlobExtFOEdgeOut
                    M.str1_NodeOrderOut = str1_NodeOrderC
                    M.str1_EdgeOut = str1_Edge

