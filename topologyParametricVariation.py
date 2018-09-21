"""
Update a topological diagram from parametric inputs
    Inputs:
        T: (topological diagram) The topological diagram used for the parametric variation
        parameters: (string) The parameters used for the parametric variation
        values: (double) The values associated to the parameters
    Outputs:
        TM: (updated topological diagram) The topological diagram updated with the parametric values (empty topology on error)
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



def StringToFloat(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return 1.0

import copy
TM = copy.deepcopy(T)


if TM and hasattr(TM, "str1_StructuralBehaviourOut"):
    str1_StructuralBehaviour = T.str1_StructuralBehaviourOut[:]
    str1_DeviationIndirect = T.str1_DeviationIndirectOut[:]
    db1_StructuralBehaviour = []
    db1_DeviationIndirect = []
        
    for i in xrange(len(str1_StructuralBehaviour)):
        if str1_StructuralBehaviour[i] in parameters:
            int0_index = parameters.index(str1_StructuralBehaviour[i])
            if len(values) > int0_index:
                db1_StructuralBehaviour.append(float(values[int0_index]))
            else: 
                db1_StructuralBehaviour.append(StringToFloat(str1_StructuralBehaviour[i]))
        else: 
            db1_StructuralBehaviour.append(StringToFloat(str1_StructuralBehaviour[i]))
    
    for i in xrange(len(str1_DeviationIndirect)):
        if str1_DeviationIndirect[i] in parameters:
            int0_index = parameters.index(str1_DeviationIndirect[i])
            if len(values) > int0_index:
                db1_DeviationIndirect.append(float(values[int0_index]))
            else: 
                db1_DeviationIndirect.append(StringToFloat(str1_DeviationIndirect[i]))
        else: 
            db1_DeviationIndirect.append(StringToFloat(str1_DeviationIndirect[i]))

    
    del TM.str1_StructuralBehaviourOut
    del TM.str1_DeviationIndirectOut
    
    TM.db1_StructuralBehaviourOut = db1_StructuralBehaviour
    TM.db1_DeviationIndirectOut = db1_DeviationIndirect


