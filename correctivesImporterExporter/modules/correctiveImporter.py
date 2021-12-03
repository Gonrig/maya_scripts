def CorrectiveImporter():
    #Importador de correctivos 
    import maya.cmds as cmds
    import json
    import os
    import sys
    # Importacion de modulos
    sistemaop = sys.platform
    windows = ["win32", "win64"]
    mac = "darwin"
    homedir = os.path.expanduser("~")
    
    for win in windows:
    	if sistemaop == win:
    		homedir_win = "{}/maya/scripts/correctivesImporterExporter/modules".format(homedir)
    		sys.path.append(homedir_win)
    		import shapeImporter as shimp
    		import dispImporter as dimp
    		
    		
    if sistemaop == mac:
    	homedir_mac = "{}/Documents/maya/correctivesImporterExporter/modules".format(homedir)
    	sys.path.append(homedir_mac)
    	import shapeImporter as shimp
    
    	
    correctives_directory_total = cmds.fileDialog2(dialogStyle=2,fm=3,caption="import",okc="Set")[0]
    shimp.CorrectiveShapesImport(correctives_directory_total)
    dimp.LocShooterImporter(correctives_directory_total)
    dimp.DrivenShooterImporter(correctives_directory_total)
    dimp.poseInterpolatorImporter(correctives_directory_total) 
    
