def CorrectiveExporter():
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
    		import blendShapeExporter as bsexp
    		import ShootersExporter as shexp
    		
    
    		
    if sistemaop == mac:
    	homedir_mac = "{}/Documents/maya/correctivesImporterExporter/modules".format(homedir)
    	sys.path.append(homedir_mac)
    	import blendShapeExporter as bsexp
    	import ShootersExporter as shexp
    	
    #Ventana de Archivo
    shapes_path = cmds.fileDialog2(dialogStyle=2,fm=0,caption="import",okc="Save")[0]
    shape_directory = shapes_path.replace(".*","")
    #Codigo
    try:
        os.mkdir(shape_directory)
        nurb_shapes_path_total = shape_directory + "/nurbShapes"
        os.mkdir(nurb_shapes_path_total)
        geo_directory_total = shape_directory + "/geoShapes"
        os.mkdir(geo_directory_total)
        ost_data_path_total = shape_directory + "/data"
        os.mkdir(ost_data_path_total)
        loc_data_folder_path = ost_data_path_total + "/locsShooterData"
        os.mkdir(loc_data_folder_path)
        driven_data_folder_path = ost_data_path_total + "/drivenShooterData"
        os.mkdir(driven_data_folder_path)
        pose_data_folder_path = ost_data_path_total + "/poseInterpolatorData"
        os.mkdir(pose_data_folder_path)
    except WindowsError: 
        cmds.warning("Try another name. The name is repeated in this folder")
        sys.exit()
    
            
    bsexp.ExportBlendShapes(nurb_shapes_path_total,geo_directory_total,ost_data_path_total)
    shexp.ShooterExporter(loc_data_folder_path,driven_data_folder_path,pose_data_folder_path)