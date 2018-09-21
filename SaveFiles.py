import Grasshopper
import GhPython

if execute:
    
    gh_doc = ghenv.Component.OnPingDocument()
    location = ghenv.LocalScope.gh_doc.FilePath
    
    import os
    folder = os.path.dirname(location)
    
    GhPython.Component.ZuiPythonComponent
    
    for o in gh_doc.Objects:
        if not isinstance(o, GhPython.Component.ZuiPythonComponent): continue
        if o.CodeInputParam: continue
        filename = o.NickName
        if not filename: continue
        
        if not filename.endswith("py"): continue
        
        file_location = os.path.join(folder, filename)
        #
        with open(file_location, 'w+') as fh:
            fh.write(o.Code.Replace("\r\n", "\n"))
            
        print("Saved: {}".format(file_location))