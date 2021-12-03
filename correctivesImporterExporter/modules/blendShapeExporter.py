def ExportBlendShapes(nurb_shapes_path,geo_directory,ost_data_path):   
    import maya.cmds as cmds
    import json
    import os
    import sys
    import maya.mel
    tar_grp = cmds.group(n="targets_c_grp",em=True)
    #Obtencion de diccionario de bs y obj
    blendshapes = []
    objs = []
    blendshapes_nurbs =[]
    obj_nurbs = []
    bs = cmds.ls(type="blendShape")
    for x in bs:
        usage = x.split("_")[2]
        if usage == "cbs":
            object = cmds.blendShape(x,q=True,g=True)[0]
            ot = cmds.objectType(object)
            if ot != "nurbsSurface":
                blendshapes.append(x)
                objs.append(object)
            else:
    		    t_grp = cmds.group(n="{}_grp".format(x),em=True,p=tar_grp)
    		    nurb_targets_list = []
    		    nurb_targets = cmds.listAttr("{}.w".format(x),m=True)
    		    for targets in nurb_targets:
    		        nurb_targets_list.append(targets)
    		    tn = len(nurb_targets_list)
    		    for n in range(0,tn):
    		        del_tar = nurb_targets_list[0]
    		        new_nurb_targets_list = nurb_targets_list.remove(del_tar)
    		        new_nurb_targets_list = nurb_targets_list[0:tn-1]
    		        nurb_targets_list.append(del_tar)
    		        attr = "{}.{}".format(x,del_tar)
    		        maya.mel.eval("source channelBoxCommand; CBdeleteConnection \"%s\""%attr)
    		        cmds.setAttr("{}.{}".format(x,del_tar),1)
    		        full_name_geo_tar = del_tar
    		        for nurb_targets_zero in new_nurb_targets_list:
    		            attrs = "{}.{}".format(x,nurb_targets_zero)
    		            maya.mel.eval("source channelBoxCommand; CBdeleteConnection \"%s\""%attrs)
    		            cmds.setAttr("{}.{}".format(x,nurb_targets_zero),0)
    		        target_geo = cmds.duplicate(object,n=full_name_geo_tar)[0]
    		        print 
    		        cmds.parent(target_geo,t_grp)
    		        blendshapes_nurbs.append(x)
    		        obj_nurbs.append(object)
		        
		        
    cmds.select(cl=True)
    cmds.select(tar_grp)
    cmds.file("{}/nurbShapes.mb".format(nurb_shapes_path),force=True,options="v=0;",typ="mayaBinary",pr=True,es=True)
    cmds.select(cl=True)
    cmds.delete(tar_grp)		        
    data = dict(zip(blendshapes, objs))
    data_nurb = dict(zip(blendshapes_nurbs,obj_nurbs))
    
    # Guardar data en un archivo externo
    def saveJson(path, data):
        with open(path, 'w') as outfile:
          json.dump(data, outfile)
    filename = "blendshapes"
    nurb_filename = "nurbBlendshapes"
    entire_filename = '{}.json'.format(filename)
    nurb_entire_filename = '{}.json'.format(nurb_filename)
    fullpath = ost_data_path + '/' + entire_filename
    fullpath_nurbs = ost_data_path + '/' + nurb_entire_filename
    saveJson(fullpath, data)
    saveJson(fullpath_nurbs, data_nurb)
    
    for shapes in blendshapes:
        shape_name = "{}.shp".format(shapes.split("_")[0])
        cmds.blendShape(shapes,e=True,ep="{}/{}".format(geo_directory,shape_name))