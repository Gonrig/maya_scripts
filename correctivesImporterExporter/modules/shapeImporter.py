def CorrectiveShapesImport(correctives_directory):
    import maya.cmds as cmds
    import json
    import os
    import sys
    data_path = "{}/data".format(correctives_directory)
    geo_path = "{}/geoShapes".format(correctives_directory)
    nurb_path = "{}/nurbShapes".format(correctives_directory)
    
    nurb_data_bs = "{}/nurbBlendshapes.json".format(data_path)
    geo_data_bs = "{}/blendshapes.json".format(data_path)
    def loadJson(path):
        with open(path, 'rb') as fp:
            data = json.load(fp)
            return data
    
    nurb_data = loadJson(nurb_data_bs)
    geo_data = loadJson(geo_data_bs)
    
    nurb_blendshapes = nurb_data.keys()
    nurb_shapes = nurb_data.values()
    
    geo_blendshapes = geo_data.keys()
    geo_shapes = geo_data.values()
    
    geo_n = len(geo_shapes)
    nurb_file_path = nurb_path+"/nurbShapes.mb"        
    cmds.file(nurb_file_path,i=True,type="mayaBinary",ignoreVersion=True,mergeNamespacesOnClash=False,rpr="nurbShapes",options="v=0;p=17;f=0",pr=True,importTimeRange="combine")
    nurb_data_path = data_path + "/nurbBlendshapes.json"
    nurb_data = loadJson(nurb_data_path)
    nurb_data_blendshape = nurb_data.keys()
    nurb_data_geo = nurb_data.values()
    nurb_data_n = len(nurb_data_blendshape)
    for n in range(0,nurb_data_n):
        nurb_geo = nurb_data_geo[n]
        nurb_bs = nurb_data_blendshape[n]
        nurb_order = nurb_bs.split("_")[3] 
        bs_grp = "{}_grp".format(nurb_bs)
        target_list = cmds.listRelatives(bs_grp,c=True)
        target_len = len(target_list)
        if nurb_order == "pr":
            cmds.blendShape(nurb_geo,n=nurb_bs,frontOfChain=True)
        if nurb_order == "po":
            cmds.blendShape(nurb_geo,n=nurb_bs,before=True,tc=0)
        for v in range(0,target_len):
            target_index = v+1
            cmds.blendShape(nurb_bs, edit=True, t=(nurb_geo,target_index,target_list[v],1.0))
            
    cmds.delete("targets_c_grp") 

    for n in range(0,geo_n):
        geo = geo_shapes[n]
        cbs_name = geo_blendshapes[n]
        shape_name = cbs_name.split("_")[0]
        shape = "{}.shp".format(shape_name) 
        order_def = cbs_name.split("_")[3]
        if order_def == "pr":
            cmds.blendShape(geo,n=cbs_name,frontOfChain=True)
        if order_def == "po":
            cmds.blendShape(geo,n=cbs_name,before=True,tc=0)
        #line de importacion del blendshape
        cmds.blendShape(cbs_name,edit=True,ip="{}/{}".format(geo_path,shape)) 

