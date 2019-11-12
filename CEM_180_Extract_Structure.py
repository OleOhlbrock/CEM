"""
Retrieves automatically the data in the structural model
    Inputs:
        M: (structural model) The calculated structural model (empty on error)
    Outputs:
        nodes: (point3D) The nodes of the structural model
        nodesID: (string) The IDs of the nodes
        trails: (line) The trail edges of the structural model
        trailsID: (string) The IDs of the trail edges
        trailsCol: (color) The colors of the trail edges
        trailsMag: (double) The magnitudes of the forces in the trail edges
        deviationDirect: (line) The direct deviation edges of the structural model
        deviationsDirectID: (string) The IDs of the direct deviation edges
        deviationDirectCol: (color) The colors of the direct deviation edges
        deviationDirectMag: (double) The magnitudes of the forces in the direct deviation edges
        deviationIndirect: (line) The indirect deviation edges of the structural model
        deviationsIndirectID: (string) The IDs of the indirect deviation edges
        deviationIndirectCol: (color) The colors of the indirect deviation edges
        deviationIndirectMag: (double) The magnitudes of the forces in the indirect deviation edges
        externalForces: (line) The external forces of the structural model
        externalForcesCol: (color) The colors of the external forces 
        externalForcesMag: (double) The magnitudes of the forces in the external forces 
    Remarks:
        This extract the data within the structural diagram
"""


if M and hasattr(M, "pt1_GlobNodeOut") and hasattr(M, "str1_NodeOrderOut") and hasattr(M, "ln1_GlobTrailEdgeOut") and hasattr(M, "cl1_GlobTrailEdgeOut") and hasattr(M, "db1_GlobTrailEdgeOut") and hasattr(M, "ln1_GlobDeviation1EdgeOut") and hasattr(M, "cl1_GlobDeviation1EdgeOut") and hasattr(M, "db1_GlobDeviation1EdgeOut") and hasattr(M, "ln1_GlobDeviation2EdgeOut") and hasattr(M, "cl1_GlobDeviation2EdgeOut") and hasattr(M, "db1_GlobDeviation2EdgeOut") and hasattr(M, "ln1_GlobExtFOEdgeOut") and hasattr(M, "cl1_GlobExtFOEdgeOut") and hasattr(M, "db1_GlobExtFOEdgeOut"):

    nodes_C = []
    nodesID_C = []
    for i in range(len(M.pt1_GlobNodeOut)):
        if M.str1_NodeOrderOut[i][0] != "L":
            nodes_C.append(M.pt1_GlobNodeOut[i])
            nodesID_C.append(M.str1_NodeOrderOut[i])
        nodes = nodes_C
        nodesID = nodesID_C
        
    trails_C = []
    trailsID_C = []
    trailsCol_C = []
    trailsMag_C = []
    for i in range(len(M.ln1_GlobTrailEdgeOut)):
        if M.str1_GlobTrailEdgeOut[i][0] != "E":
            trails_C.append(M.ln1_GlobTrailEdgeOut[i])
            trailsID_C.append(M.str1_GlobTrailEdgeOut[i])
            trailsCol_C.append(M.cl1_GlobTrailEdgeOut[i])
            trailsMag_C.append(M.db1_GlobTrailEdgeOut[i])
        trails = trails_C
        trailsID = trailsID_C
        trailsCol = trailsCol_C
        trailsMag = trailsMag_C
        
    deviationsDirect = M.ln1_GlobDeviation1EdgeOut
    deviationsDirectID = M.str1_GlobDeviation1EdgeOut
    deviationsDirectCol = M.cl1_GlobDeviation1EdgeOut
    deviationsDirectMag = M.db1_GlobDeviation1EdgeOut
    deviationsIndirect = M.ln1_GlobDeviation2EdgeOut
    deviationsIndirectID = M.str1_GlobDeviation2EdgeOut
    deviationsIndirectCol = M.cl1_GlobDeviation2EdgeOut
    deviationsIndirectMag = M.db1_GlobDeviation2EdgeOut
    deviations = M.ln1_GlobDeviationEdgeOut
    deviationsID = M.str1_GlobDeviationEdgeOut
    deviationsCol = M.cl1_GlobDeviationEdgeOut
    deviationsMag = M.db1_GlobDeviationEdgeOut
    externalForces = M.ln1_GlobExtFOEdgeOut
    externalForcesCol = M.cl1_GlobExtFOEdgeOut
    externalForcesMag = M.db1_GlobExtFOEdgeOut
