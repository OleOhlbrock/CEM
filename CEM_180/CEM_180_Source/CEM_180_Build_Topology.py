"""
Defines a new topological diagram from inputs
    Inputs:
        T: (trailObjects) Trail members in the topological diagram 
        L: (pointLoadObjects) Point Loads in the topological diagram 
        D: (deviationObjects) Deviation members in the topological diagram 
        S: (supportObjects) Supports in the topological diagram
    Outputs:
        TP: (topological diagram) The constructed topological diagram (empty topology on error)
    Remarks:
        This generates a new instance of the topological diagram
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




import System.Drawing.Color
import System.Guid
import Rhino
db0_T = 0.001

class topology(object):
    def __repr__(self):
        return self.ToString()
        
    def __str__(self):
        return self.ToString()
        
    def ToString(self):
        if trailMembers and trailMembersID:
            if len(trailMembers) == len(trailMembersID):
                str0_Description = ""
                if hasattr(self, "str1_StructuralBehaviourOut") or hasattr(self, "db1_StructuralBehaviourOut")  and pt1_NodeOut and int2_Trail:
                    str0_Description += "Topological Diagram\n\nvertices: " + str(len(pt1_NodeOut)) + "\ntrail members: " + str(len(int2_Trail)) 
                    if int2_Deviation1:
                        str0_Description += "\ndirect deviation members: " + str(len(int2_Deviation1))
                        if str2_Deviation2:
                            str0_Description += "\nindirect deviation members: " + str(len(str2_Deviation2))
                    return str0_Description
                else:
                    return "Empty topology"
            else:
                return "Empty topology"
        else:
            return "Empty topology"


def ListListToList(xx2_Data):
    xx1_DataOut = []
    for xx1_Data in xx2_Data:
        xx1_DataOut.extend(xx1_Data)
    return xx1_DataOut


TP = topology()


externalForces = []
externalForcesID = []
if L:
    for l in L:
        if l:
            externalForces.extend(l.geom)
            externalForcesID.extend(l.magn)


trailMembers = []
trailMembersID = []
if T:
    for t in T:
        if t:
            trailMembers.extend(t.geom)
            trailMembersID.extend(t.len)


deviationMembers = []
deviationMembersID = []
if D:
    for d in D:
        if d:
            deviationMembers.extend(d.geom)
            deviationMembersID.extend(d.magn)

supports = []
if S:
    for s in S:
        if s:
            supports.extend(s.geom)



if trailMembers and trailMembersID:
    if len(trailMembers) == len(trailMembersID) and len(deviationMembers) == len(deviationMembersID) and len(externalForces) == len(externalForcesID):

        # Create List of Nodes and trailMembers' Connectivity
        pt1_Node = []
        int2_Trail = []
        int2_Deviation = []
        int2_ExtForce = []
        
        pt1_Node.append(trailMembers[0].PointAtStart)
        
        # Nodes and Egdes from trailMembers
        for crv0_Trail in trailMembers:
            int1_Trail = []
            pt0_Start = crv0_Trail.PointAtStart
            bl0_Check = False
            for i in xrange(len(pt1_Node)):
                if abs(pt0_Start.X - pt1_Node[i].X) < db0_T and abs(pt0_Start.Y - pt1_Node[i].Y) < db0_T and abs(pt0_Start.Z - pt1_Node[i].Z) < db0_T:
                    int1_Trail.append(i)
                    bl0_Check = True
                    break
            if bl0_Check == False:
                pt1_Node.append(pt0_Start)
                int1_Trail.append(len(pt1_Node)-1)
            pt0_End = crv0_Trail.PointAtEnd
            bl0_Check = False
            for i in xrange(len(pt1_Node)):
                if abs(pt0_End.X - pt1_Node[i].X) < db0_T and abs(pt0_End.Y - pt1_Node[i].Y) < db0_T and abs(pt0_End.Z - pt1_Node[i].Z) < db0_T:
                    int1_Trail.append(i)
                    bl0_Check = True
                    break
            if bl0_Check == False:
                pt1_Node.append(pt0_End)
                int1_Trail.append(len(pt1_Node)-1)
            int2_Trail.append(int1_Trail)
        

        # Deviation
        crv1_DeviationClean = []
        id1_DeviationClean = []
        for k in xrange(len(deviationMembers)):
            pt0_StartDeviation = deviationMembers[k].PointAtStart
            pt0_EndDeviation = deviationMembers[k].PointAtEnd
            for i in xrange(len(pt1_Node)):
                if abs(pt0_StartDeviation.X - pt1_Node[i].X) < db0_T and abs(pt0_StartDeviation.Y - pt1_Node[i].Y) < db0_T and abs(pt0_StartDeviation.Z - pt1_Node[i].Z) < db0_T:
                    for j in xrange(len(pt1_Node)):
                        if abs(pt0_EndDeviation.X - pt1_Node[j].X) < db0_T and abs(pt0_EndDeviation.Y - pt1_Node[j].Y) < db0_T and abs(pt0_EndDeviation.Z - pt1_Node[j].Z) < db0_T:
                            crv1_DeviationClean.append(deviationMembers[k])
                            id1_DeviationClean.append(deviationMembersID[k])
                            int1_Deviation = []
                            int1_Deviation.append(i)
                            int1_Deviation.append(j)
                            int2_Deviation.append(int1_Deviation)
                            break
                    break
        deviationMembers = crv1_DeviationClean
        deviationMembersID = id1_DeviationClean
        
        # External Force
        pt1_ExtForceClean = []
        External_Forces_IDClean = []
        for k in xrange(len(externalForces)):
            for i in xrange(len(pt1_Node)):
                int1_ExtForce = []
                if abs(externalForces[k].X - pt1_Node[i].X) < db0_T and abs(externalForces[k].Y - pt1_Node[i].Y) < db0_T and abs(externalForces[k].Z - pt1_Node[i].Z) < db0_T:
                    pt1_ExtForceClean.append(externalForces[k])
                    External_Forces_IDClean.append(externalForcesID[k])
                    int1_ExtForce.append(i)
                    int2_ExtForce.append(int1_ExtForce)
                    break
        
        externalForces = pt1_ExtForceClean
        externalForcesID = External_Forces_IDClean
        
        
        # Extract Attributes External Forces
        st2_externalForcesID = []
        for i in range(len(externalForcesID)):
            st1_externalForcesID = []
            for j in range(len(externalForcesID[i])):
                st1_externalForcesID.append(str(externalForcesID[i][j]))
            st2_externalForcesID.append(st1_externalForcesID)
        str2_ExtForceAtt = st2_externalForcesID

        # Extract Attributes trailMembers
        str1_TrailAtt = [str(x) for x in trailMembersID]

        # Extract Attributes Deviation
        str1_DeviationAtt = [str(x) for x in deviationMembersID]
        
        
        # Create Dictionary of trailMembers' Ends
        dc2_TrailEnds = {}
        for i in xrange(len(int2_Trail)):
            dc2_TrailEnds[str(i)] = [str(x) for x in int2_Trail[i]]
        
        # Create Dictionary of trailMembers' Attributes
        dc1_TrailAtt = {}
        for i in xrange(len(str1_TrailAtt)):
            dc1_TrailAtt[str(i)] = str1_TrailAtt[i]
        
        
        # Create Dictionary of External Forces' End
        dc1_ExtForceEnds = {}
        for i in xrange(len(int2_ExtForce)):
            dc1_ExtForceEnds[str(i)] = str(int2_ExtForce[i][0])
        
        
        # Create Dictionary of External Forces' Attributes
        dc2_ExtForceAtt = {}
        for i in xrange(len(str2_ExtForceAtt)):
            dc2_ExtForceAtt[str(i)] = [x for x in str2_ExtForceAtt[i]]

        
        # Create Lists of Node-Node Connectivity from trailMembers
        int2_Node = []
        for pt0_Node in pt1_Node:
            int1_Node = []
            int2_Node.append(int1_Node)
        for int1_Trail in int2_Trail:
            int2_Node[int1_Trail[0]].append(int1_Trail[1])
            int2_Node[int1_Trail[1]].append(int1_Trail[0])
        
        
        # Create Lists of Deviations' Ends and Attributes
        str2_Deviation = []
        for i in xrange(len(str1_DeviationAtt)):
            str2_Deviation.append( [str(item) for item in int2_Deviation[i] ] )
            str2_Deviation[i].extend([str1_DeviationAtt[i]])
        
        # Convert Trail Input into Polylines
        ln1_Trail = []
        for crv0_Trail in trailMembers:
            if crv0_Trail is Rhino.Geometry.Line:
                ln1_Trail.append(crv0_Trail)
            else:
                ln1_Trail.append(Rhino.Geometry.Line(crv0_Trail.PointAtStart, crv0_Trail.PointAtEnd))
        
        trailMembers = []
        for ln0_Trail in ln1_Trail:
            trailMembers.append(ln0_Trail.ToNurbsCurve())
        
        plc1_Trail = Rhino.Geometry.Curve.JoinCurves(trailMembers)
        
        pln1_Trail = []
        for plc0_Trail in plc1_Trail:
            pln1_Trail.append(plc0_Trail.TryGetPolyline()[1])
        
        
        # Check supports
        pt1_SupportClean = []
        for j in xrange(len(pln1_Trail)):
            if supports:
                pt1_SupportClean.append(pln1_Trail[j][len(pln1_Trail[j])-1])
                for i in xrange(len(supports)):
                    if abs(pln1_Trail[j][0].X - supports[i].X) < db0_T and abs(pln1_Trail[j][0].Y - supports[i].Y) < db0_T and abs(pln1_Trail[j][0].Z - supports[i].Z) < db0_T:
                        pt1_SupportClean[j] = pln1_Trail[j][0]
                        pln1_Trail[j].Reverse()
            else:
                pt1_SupportClean.append(pln1_Trail[j][len(pln1_Trail[j])-1])
        supports = pt1_SupportClean
        
        
        # Find Node Indexes of supports
        int1_Support = []
        for pt0_Support in supports:
            for i in xrange(len(pt1_Node)):
                if abs(pt0_Support.X - pt1_Node[i].X) < db0_T and abs(pt0_Support.Y - pt1_Node[i].Y) < db0_T and abs(pt0_Support.Z - pt1_Node[i].Z) < db0_T:
                    int1_Support.append(i)
                    break
        
        # Create Graph (Dictionary of Node-Node Connectivity from trailMembers)
        dc2_Node = {}
        for i in xrange(len(int2_Node)):
            dc2_Node[str(i)] = [str(x) for x in int2_Node[i]]
        
        int2_TrailPoly = []
        for pln0_Trail in pln1_Trail:
            int1_TrailPoly = []
            for i in xrange(len(pln0_Trail)):
                for k in xrange(len(pt1_Node)):
                    if abs(pln0_Trail[i].X - pt1_Node[k].X) < db0_T and abs(pln0_Trail[i].Y - pt1_Node[k].Y) < db0_T and abs(pln0_Trail[i].Z - pt1_Node[k].Z) < db0_T:
                        int1_TrailPoly.append(k)
                        break
            int2_TrailPoly.append(list(reversed(int1_TrailPoly)))
        
        dc2_ShortPath = {}

        for i in xrange(len(pt1_Node)):
            for int1_TrailPoly in int2_TrailPoly:
                if i in int1_TrailPoly:
                    str1_ShortPath = ["S"]
                    str1_ShortPath.extend(map(str, int1_TrailPoly[:int1_TrailPoly.index(i)+1]))
                    dc2_ShortPath[str(i)] = str1_ShortPath
                    break
        
        dc1_ShortPathDist = {}
        dc2_ShortPathDistGrade = {}
        
        for i in xrange(len(pt1_Node)):
            for pln0_Trail in pln1_Trail:
                for j in xrange(len(pln0_Trail)):
                    if abs(pln0_Trail[j].X - pt1_Node[i].X) < db0_T and abs(pln0_Trail[j].Y - pt1_Node[i].Y) < db0_T and abs(pln0_Trail[j].Z - pt1_Node[i].Z) < db0_T:
                        dc1_ShortPathDist[str(i)] = len(pln0_Trail) - j
                        break
        

        # Define Sequences
        for key in dc1_ShortPathDist:
            if dc1_ShortPathDist[key] not in dc2_ShortPathDistGrade:
                dc2_ShortPathDistGrade[dc1_ShortPathDist[key]] = [key]
            else:
                dc2_ShortPathDistGrade[dc1_ShortPathDist[key]].extend([key])
        
        
        # Separate Deviation1 (direct) and Deviation2 (indirect-bracing)
        
        dc2_Deviation1Ends = {}
        dc2_Deviation2Ends = {}
        
        dc1_Deviation1Att = {}
        dc1_Deviation2Att = {}
        
        int2_Deviation1 = []
        str2_Deviation2 = []
        
        crv1_Deviation1 = []
        crv1_Deviation2 = []
        
        int1_Deviation1ID = []
        int1_Deviation2ID = []
        
        j = 0
        k = 0
        
        
        for i in xrange(len(str2_Deviation)):
            if dc1_ShortPathDist[ str(str2_Deviation[i][0]) ] == dc1_ShortPathDist[ str(str2_Deviation[i][1]) ]:
                dc2_Deviation1Ends[str(j)] = [str(str2_Deviation[i][0]),str(str2_Deviation[i][1])]
                dc1_Deviation1Att[str(j)] = str(str2_Deviation[i][2])
                int2_Deviation1.append([int(str2_Deviation[i][0]),int(str2_Deviation[i][1])])
                crv1_Deviation1.append(deviationMembers[i])
                int1_Deviation1ID.append(i)
                print j
                j += 1
            else:
                dc2_Deviation2Ends[str(k)] = [str(str2_Deviation[i][0]),str(str2_Deviation[i][1])]
                dc1_Deviation2Att[str(k)] = str(str2_Deviation[i][2])
                str2_Deviation2.append(str2_Deviation[i])
                crv1_Deviation2.append(deviationMembers[i])
                int1_Deviation2ID.append(i)
                k += 1
        
        print dc2_Deviation1Ends
        print int1_Deviation1ID
        print int1_Deviation2ID
        
        # Create Dictionary of Trail and Deviation 1 for Structural Matrix
        dc2_EdgeEnds = {}
        dc2_TrailEndsOut = dc2_TrailEnds.copy()
        dc2_Deviation1EndsOut = {}
        
        for key in dc2_TrailEnds:
            dc2_EdgeEnds[str(int(key))] = dc2_TrailEnds[key]
        for key in dc2_Deviation1Ends:
            dc2_EdgeEnds[str(int(key)+len(dc2_TrailEnds))] = dc2_Deviation1Ends[key]
            dc2_Deviation1EndsOut[str(int(key)+len(dc2_TrailEnds))] = dc2_Deviation1Ends[key]
            
        dc1_EdgeAtt = {}
        for key in dc1_TrailAtt:
            dc1_EdgeAtt[str(int(key))] = dc1_TrailAtt[key]
        for key in dc1_Deviation1Att:
            dc1_EdgeAtt[str(int(key)+len(dc1_TrailAtt))] = dc1_Deviation1Att[key]
        
        # Create Dictionary of Trail and Deviation 1 and 2 for Visualization
        dc1_Edge = {}
        for key in dc1_TrailAtt:
            dc1_Edge[str(int(key))] = dc1_TrailAtt[key]
        for key in dc1_Deviation1Att:
            dc1_Edge[str(int(key)+len(dc1_TrailAtt))] = dc1_Deviation1Att[key]
        for key in dc1_Deviation2Att:
            dc1_Edge[str(int(key)+len(dc1_TrailAtt)+len(dc1_Deviation1Att))] = dc1_Deviation2Att[key]
        
        ## Visualization
        
        # Nodes
        pt1_NodeOut = pt1_Node
        pt1_TargetOut = pt1_NodeOut
        str1_NodeOut = [str(i) + " (" + str(dc1_ShortPathDist[str(i)]) + ")" for i in xrange(len(pt1_Node))]
        str1_TargetOut = [str(i) for i in xrange(len(pt1_Node))]
        
        # Edges
        crv1_Edge = []
        for crv0_Trail in trailMembers: crv1_Edge.append(crv0_Trail)
        for crv0_Deviation1 in crv1_Deviation1: crv1_Edge.append(crv0_Deviation1)
        for crv0_Deviation2 in crv1_Deviation2: crv1_Edge.append(crv0_Deviation2)
        
        crv1_EdgeOut = crv1_Edge
        pt1_EdgeOut = [crv0_Edge.PointAtNormalizedLength(0.6) for crv0_Edge in crv1_EdgeOut]
        str1_EdgeOut = [str(i) + " (" + dc1_Edge[str(i)] + ")" for i in xrange(len(crv1_EdgeOut))]

        # Update Lists of Node-Node Connectivity from Deviation 1
        for int1_DevTemp in int2_Deviation1:
            int2_Node[int1_DevTemp[0]].append(int1_DevTemp[1])
            int2_Node[int1_DevTemp[1]].append(int1_DevTemp[0])
        
        
        # Create Graph (Dictionary of Node-Node Connectivity from trailMembers)
        for i in xrange(len(int2_Node)):
            dc2_Node[str(i)] = [str(x) for x in int2_Node[i]]
        
        
        ## Create Dictionaries for Structural Matrix
        dc1_NodeTrailOut = {}
        dc1_NodeTrailIn = {}
        dc2_NodeDeviation = {}
        dc1_NodeExtForce = {}
        dc1_NodeExtForceAtt = {}
        int0_NodeTrailIn = {}

        
        # Trail In and Out
        for key in dc2_ShortPath:
            dc1_NodeTrailOut[key] = dc2_ShortPath[key][len(dc2_ShortPath[key])-2]
        
        int0_ShortPathDistGradeMax = max(dc2_ShortPathDistGrade)
        
        for key in dc1_NodeTrailOut:
            if dc1_NodeTrailOut[key] == "S": dc1_NodeTrailOut[key] = dc1_NodeTrailOut[key] + key
            dc1_NodeTrailIn[dc1_NodeTrailOut[key]] = key

        for key in dc1_NodeTrailOut:
            if key not in dc1_NodeTrailIn:
                str0_Key = "L" + key
                for i in range(int0_ShortPathDistGradeMax - dc1_ShortPathDist[key] + 1):
                    dc1_NodeTrailIn[str0_Key[1:]] = str0_Key
                    str0_Key = "L" + str0_Key

        
        for key in dc1_NodeTrailIn:
            if "L" + key not in dc1_NodeTrailOut:
                dc1_NodeTrailOut[dc1_NodeTrailIn[key]] = key
        
        # Deviation
        for key in dc2_Node:
            str1_v = []
            for v in dc2_Node[key]:
                if v != dc1_NodeTrailOut[key] and v != dc1_NodeTrailIn[key]:
                    str1_v.append(v)
            dc2_NodeDeviation[key] = str1_v
        
        # External Forces
        for key in dc1_ExtForceEnds:
            if dc1_ExtForceEnds[key] not in dc1_NodeExtForce:
                dc1_NodeExtForce[dc1_ExtForceEnds[key]] = [key]
            else:
                dc1_NodeExtForce[dc1_ExtForceEnds[key]].append(key)
        
        for key in dc1_NodeExtForce:
            for v in dc1_NodeExtForce[key]:
                if dc1_ExtForceEnds[v] not in dc1_NodeExtForceAtt:
                    dc1_NodeExtForceAtt[key] = [item for item in dc2_ExtForceAtt[v]]
                else:
                    xx1_NodeExtForceAtt = dc1_NodeExtForceAtt[dc1_ExtForceEnds[v]]
                    for i in xrange(len(xx1_NodeExtForceAtt)):
                        try:
                            xx1_NodeExtForceAtt[i] = float(xx1_NodeExtForceAtt[i])
                        except:
                            xx1_NodeExtForceAtt[i] = -1.0
                            
                            
                    try:
                        dc2_ExtForceAtt[v][0] = float(dc2_ExtForceAtt[v][0])
                    except:
                        dc2_ExtForceAtt[v][0] = -1.0
                    try:
                        dc2_ExtForceAtt[v][1] = float(dc2_ExtForceAtt[v][1])
                    except:
                        dc2_ExtForceAtt[v][1] = -1.0
                    try:
                        dc2_ExtForceAtt[v][2] = float(dc2_ExtForceAtt[v][2])
                    except:
                        dc2_ExtForceAtt[v][2] = -1.0
                    dc1_NodeExtForceAtt[key][0] += float(dc2_ExtForceAtt[v][0])
                    dc1_NodeExtForceAtt[key][1] += float(dc2_ExtForceAtt[v][1])
                    dc1_NodeExtForceAtt[key][2] += float(dc2_ExtForceAtt[v][2])
        
        
        ## Create Structural Matrix According to Weight
        
        # Initialize Matrix with Indices
        str2_StructuralMatrix = []
        str1_NodeOrderMatrix = []
        str2_NodeOrderMatrix = []
        
        str1_NodeOrder = dc2_ShortPathDistGrade[1]

        for i in sorted(xrange(1,len(dc2_ShortPathDistGrade)+1)):
            str1_NodeOrderUp = []
            str2_NodeOrderMatrix.append(str1_NodeOrder)
            for str0_NodeOrder in str1_NodeOrder:
                str1_NodeOrderMatrix.append(str0_NodeOrder)
                if str0_NodeOrder[0] != "L":
                    str2_StructuralMatrix.append(["0"]*(3+len(str1_NodeOrder)+1))
                    str1_NodeOrderUp.append(dc1_NodeTrailIn[str0_NodeOrder])
                    
                else:
                    str2_StructuralMatrix.append(["0"]*(3+len(str1_NodeOrder)+1))
                    str1_NodeOrderUp.append("L" + str0_NodeOrder)
                    dc1_NodeTrailIn[str0_NodeOrder] = str0_NodeOrder[1:]
                    dc2_EdgeEnds[str0_NodeOrder.replace("L","E")] = [str0_NodeOrder[1:], str0_NodeOrder]
                    dc2_TrailEndsOut[str0_NodeOrder.replace("L","E")] = [str0_NodeOrder[1:], str0_NodeOrder]
            str1_NodeOrder = str1_NodeOrderUp
            
        int0_NodeOrderMatrix = len(str2_NodeOrderMatrix[0])

        # Add Attribute External Forces
        for key in dc1_NodeExtForce:
            int0_NodeIndex = str1_NodeOrderMatrix.index(key)
            str2_StructuralMatrix[int0_NodeIndex][0:3] = [str(item) for item in dc1_NodeExtForceAtt[key]]
        
        # Add Attributes Auxiliary Trails
        for key in dc2_EdgeEnds: 
            if key[0] == "E": dc1_EdgeAtt[key] = "0.0"
        
        # Add Attribute Trail Out
        for key in dc2_EdgeEnds:
            if dc2_EdgeEnds[key][0] in dc1_NodeTrailOut and dc2_EdgeEnds[key][1] == dc1_NodeTrailOut[dc2_EdgeEnds[key][0]]:
                int0_NodeIndex = str1_NodeOrderMatrix.index(dc2_EdgeEnds[key][0])
                str2_StructuralMatrix[int0_NodeIndex][len(str2_StructuralMatrix[int0_NodeIndex])-1] = dc1_EdgeAtt[key]
            elif dc2_EdgeEnds[key][1] in dc1_NodeTrailOut and dc2_EdgeEnds[key][0] == dc1_NodeTrailOut[dc2_EdgeEnds[key][1]]:
                int0_NodeIndex = str1_NodeOrderMatrix.index(dc2_EdgeEnds[key][1])
                str2_StructuralMatrix[int0_NodeIndex][len(str2_StructuralMatrix[int0_NodeIndex])-1] = dc1_EdgeAtt[key]
        
        # Add Attribute Deviation
        for key in dc2_EdgeEnds:
            if dc2_EdgeEnds[key][0] in dc2_NodeDeviation and dc2_EdgeEnds[key][1] in dc2_NodeDeviation[dc2_EdgeEnds[key][0]]:
                int0_NodeIndex = str1_NodeOrderMatrix.index(dc2_EdgeEnds[key][0])
                int0_NodeIndexTo = str1_NodeOrderMatrix.index(dc2_EdgeEnds[key][1])
                int0_NodeIndexRaw = (int0_NodeIndexTo) % int0_NodeOrderMatrix
                str2_StructuralMatrix[int0_NodeIndex][3 + int0_NodeIndexRaw] = dc1_EdgeAtt[key]
            if dc2_EdgeEnds[key][1] in dc2_NodeDeviation and dc2_EdgeEnds[key][0] in dc2_NodeDeviation[dc2_EdgeEnds[key][1]]:
                int0_NodeIndex = str1_NodeOrderMatrix.index(dc2_EdgeEnds[key][1])
                int0_NodeIndexTo = str1_NodeOrderMatrix.index(dc2_EdgeEnds[key][0])
                int0_NodeIndexRaw = (int0_NodeIndexTo) % int0_NodeOrderMatrix
                str2_StructuralMatrix[int0_NodeIndex][3 + int0_NodeIndexRaw] = dc1_EdgeAtt[key]
        
        # Order Matrix
        str2_StructuralMatrixOrder = []
        int1_StructuralMatrixOrder = []
        str2_NodeOrderMatrixReversed = []
        
        for i in reversed(xrange(1,len(str2_NodeOrderMatrix)+1)):
            for j in xrange(int0_NodeOrderMatrix):
                int0_Index = int0_NodeOrderMatrix*(i-1)+j
                if i != len(str2_NodeOrderMatrix):
                    int1_StructuralMatrixOrder.append(str2_NodeOrderMatrix[i-1][j])
                str2_StructuralMatrixOrder.append(str2_StructuralMatrix[int0_NodeOrderMatrix*(i-1)+j])
        
        for i in reversed(xrange(1,len(str2_NodeOrderMatrix)+1)):
            str1_NodeOrderMatrixReversed = []
            for j in xrange(int0_NodeOrderMatrix):
                str1_NodeOrderMatrixReversed.append(str2_NodeOrderMatrix[i-1][j])
            str2_NodeOrderMatrixReversed.append(str1_NodeOrderMatrixReversed)

        
        # Substitute Node Index with Matrix Index in Deviation2
        str1_Deviation2 = ListListToList(str2_Deviation2)
        str1_NodeOrder = ListListToList(str2_NodeOrderMatrixReversed)
        
        str1_NodeOrderOut = str1_NodeOrder[:]
        
        # Edge-Node List
        dc2_EdgeEndsComplete = {}
        dc2_EdgeEndsComplete = dict(dc2_EdgeEnds)
        dc2_Deviation2EndsOut = {}
        
        
        int0_EdgeEndsLen = len([k for k in dc2_EdgeEndsComplete if not k.startswith('E')])
        
        for i in range(0,len(str1_Deviation2),3):
            dc2_EdgeEndsComplete[str( int(int0_EdgeEndsLen+i/3) )] = [str1_Deviation2[i],str1_Deviation2[i+1]]
            dc2_Deviation2EndsOut[str( int(int0_EdgeEndsLen+i/3) )] = [str1_Deviation2[i],str1_Deviation2[i+1]]
                
        for i in xrange(len(str1_Deviation2)):
            if (i+1) % 3 != 0:
                str1_Deviation2[i] = str1_NodeOrder.index(str(str1_Deviation2[i]))
        
        
        
        ## Output
        str1_DeviationIndirectOut = str1_Deviation2
        str1_StructuralBehaviourOut = ListListToList(str2_StructuralMatrixOrder)
        
        #### AUTOMATIC GEOMETRIC INPUT FOR FORM DIAGRAM
        
        # str1_NodeOrderOut from Graph with "L" where leaf (as List)
        # str1_NodeOrderC = Clean Node Order without L but duplicated node numbers where needed
        # pt1_NodeOut = geometric locations from vertices in graph
        
        # Amount of layers
        N_layers = len(str1_NodeOrder)/len(supports)
        
        # Create List of Origin Nodes with Indexes
        str1_OriginNodeOut = [str0_OriginNodeOut.replace("L","") for str0_OriginNodeOut in str1_NodeOrder[:len(supports)]]
        pt1_OriginNodeOut = []
        for str0_OriginNodeOut in str1_OriginNodeOut:
            pt1_OriginNodeOut.append(pt1_Node[int(str0_OriginNodeOut)])

        str1_ConstraintPlane = []
        pl1_ConstraintPlane = []

        for key in dc2_TrailEnds:
            
            str0_0 = dc2_TrailEnds[key][0]
            str0_1 = dc2_TrailEnds[key][1]
            int0_0 = dc1_ShortPathDist[str0_0]
            int0_1 = dc1_ShortPathDist[str0_1]
            
            str1_ConstraintPlane.append(str0_0)
            pt0_Start = pt1_NodeOut[int(str0_0)]
            pt0_End = pt1_NodeOut[int(str0_1)]
            
            if int0_0 > int0_1:
                str1_ConstraintPlane[len(str1_ConstraintPlane)-1] = str0_1
                pt0_Start = pt1_NodeOut[int(str0_1)]
                pt0_End = pt1_NodeOut[int(str0_0)]
                
            vc0_Normal = Rhino.Geometry.Vector3d(pt0_End-pt0_Start)
            pl0_Plane = Rhino.Geometry.Plane(pt0_Start,vc0_Normal)
            pl1_ConstraintPlane.append(pl0_Plane)
            

        
        str1_ConstraintPlaneOut = str1_ConstraintPlane
        pl1_ConstraintPlaneOut = pl1_ConstraintPlane

        TP.str1_StructuralBehaviourOut = str1_StructuralBehaviourOut
        TP.str1_DeviationIndirectOut = str1_DeviationIndirectOut
        TP.pt1_NodeOut = pt1_NodeOut
        TP.str1_NodeOut = str1_NodeOut
        TP.crv1_EdgeOut = crv1_EdgeOut
        TP.pt1_EdgeOut = pt1_EdgeOut
        TP.str1_EdgeOut = str1_EdgeOut
        TP.dc2_EdgeEndsCompleteOut = dc2_EdgeEndsComplete
        TP.dc2_TrailEndsOut = dc2_TrailEndsOut
        TP.dc2_Deviation1EndsOut = dc2_Deviation1EndsOut
        TP.dc2_Deviation2EndsOut = dc2_Deviation2EndsOut
        TP.int1_Deviation1ID = int1_Deviation1ID
        TP.int1_Deviation2ID = int1_Deviation2ID
        TP.str1_NodeOrderOut = str1_NodeOrderOut
        TP.str1_ConstraintPlaneOut = str1_ConstraintPlaneOut
        TP.pl1_ConstraintPlaneOut = pl1_ConstraintPlaneOut
        TP.str1_OriginNodeOut = str1_OriginNodeOut
        TP.pt1_OriginNodeOut = pt1_OriginNodeOut


def StringToFloat(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return 1.0

if TP and hasattr(TP, "str1_StructuralBehaviourOut"):
    str1_StructuralBehaviour = TP.str1_StructuralBehaviourOut[:]
    str1_DeviationIndirect = TP.str1_DeviationIndirectOut[:]
    db1_StructuralBehaviour = []
    db1_DeviationIndirect = []
        
    for i in xrange(len(str1_StructuralBehaviour)):
        db1_StructuralBehaviour.append(StringToFloat(str1_StructuralBehaviour[i]))
    
    for i in xrange(len(str1_DeviationIndirect)):
        db1_DeviationIndirect.append(StringToFloat(str1_DeviationIndirect[i]))

    del TP.str1_StructuralBehaviourOut
    del TP.str1_DeviationIndirectOut
    
    TP.db1_StructuralBehaviourOut = db1_StructuralBehaviour
    TP.db1_DeviationIndirectOut = db1_DeviationIndirect