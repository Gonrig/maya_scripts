def ShooterExporter(loc_data_folder_path,driven_data_folder_path,pose_data_folder_path):
    import maya.cmds as cmds
    import json
    import os 
    ost_data_path = loc_data_folder_path
    #Funcion de exportacion de locators info
    def saveJson(path, data):
        with open(path, 'w') as outfile:
          json.dump(data, outfile)
    def locsDispInfoExporter(locator_base_name,ost_data_path,bs_name): 
        locators_name =locator_base_name.split("_")[0]
        locators_side = locator_base_name.split("_")[1]
        locators_target_name = "{}_{}_Target".format(locators_name,locators_side)
        locators_pose_name = "{}_{}_Pose".format(locators_name,locators_side)
        locators = [locator_base_name,locators_target_name,locators_pose_name]
        loc_matrix_list = []
        loc_parents_list =[]
        for loc in locators:
        	loc_matrix = cmds.xform(loc,q=True,matrix=True,ws=True)
        	loc_matrix_list.append(loc_matrix)
        	loc_parents = cmds.listRelatives(loc,p=True,c=False)[0]
        	loc_parents_list.append(loc_parents)
        matrix_data = dict(zip(locators,loc_matrix_list))
        parents_data = dict(zip(locators,loc_parents_list))
        matrix_filename = "{}_{}_matrixLocsData.json".format(locators_name,locators_side)
        matrix_path = loc_data_folder_path + '/' + matrix_filename
        parents_filename = "{}{}_{}_parentsLocsData.json".format(locators_name,bs_name,locators_side)
        parents_path = loc_data_folder_path + '/' + parents_filename 
        
        saveJson(matrix_path,matrix_data)
        saveJson(parents_path,parents_data)
    # Funcion de exportacion de drivens info
    def drivenDispInfoExporter(bs_driven,target,driven_data_folder_path):
        def saveJson(path, data):
            with open(path, 'w') as outfile:
                json.dump(data, outfile)
        animCurve = cmds.listConnections(target,s=True,d=False,scn=True)[0]
        at = cmds.objectType(animCurve)
        if at == "animCurveUU":
            input = cmds.listConnections(animCurve,p=True,c=False,scn=True,d=False)[0]
            transform_values = cmds.keyframe(animCurve,q=True,iv=0,fc=True)
            target_values = cmds.keyframe(animCurve,q=True,iv=0,vc=True)
            target_name = target.split(".")[1]
            drivenkey_values = dict(zip(transform_values,target_values))
            nodes_input_driven ={input:bs_driven}
            driven_data_filename = "{}_dv.json".format(target_name)
            input_driven_filename = "{}_id.json".format(target_name)
            dv_fullpath = driven_data_folder_path+"/"+driven_data_filename
            ip_fullpath = driven_data_folder_path+"/"+input_driven_filename
            saveJson(dv_fullpath,drivenkey_values)
            saveJson(ip_fullpath,nodes_input_driven)
   
    def poseInterpolatorExporter(pose_data_folder_path):
        pose_interpolator_list = cmds.ls(type="poseInterpolator")
    	for pose_interpolator in pose_interpolator_list:
    		poses = pose_interpolator.replace("Shape","")
    		pose_name = "{}.pose".format(poses)
    		pose_path = "{}/{}".format(pose_data_folder_path,pose_name)
    		cmds.poseInterpolator(poses,e=True,ex=pose_path)  
    		 
    #Listar blendshapes correctivos
    list_bs = []
    blends = cmds.ls(type="blendShape")
    for x in blends:
        usage = x.split("_")[2]
        if usage == "cbs":
            list_bs.append(x)
            
    #Codigo exportacion de disparadores
               
        for bs in list_bs:
            target_attr = cmds.listAttr("{}.w".format(bs),m=True)
            for tar in target_attr:
                tar_all = "{}.{}".format(bs,tar)
                anim_conection_list = cmds.listConnections(tar_all,s=True,d=False,scn=True,type="animCurveUU")
                if anim_conection_list is None:
                    skip = True
                else:
                    anim_conection = anim_conection_list[0]
                    drivenDispInfoExporter(bs,tar_all,driven_data_folder_path)
                base_conection_list = cmds.listConnections(tar_all,s=True,d=False,scn=True,type="transform")
                if base_conection_list is None:
                    skip = True
                else:
                    base_conection = base_conection_list[0]
                    conection_usage = base_conection.split("_")[2]
                    if conection_usage == "Base":
                        target_conection_data = {tar_all:base_conection}
                        coneangle_value = cmds.getAttr("{}.ConeAngle".format(base_conection))
                        # En el futuro cambiarlo la primera C de cone angle en minuscula
                        cone_data = {coneangle_value:base_conection}
                        new_tar_name = base_conection.split("_")[0]
                        new_tar_side = base_conection.split("_")[1]
                        bs_name = bs.split("_")[0]
                        target_filename = "{}{}_{}_targetsLocsData.json".format(new_tar_name,bs_name,new_tar_side)
                        cone_filename = "{}{}_{}_coneAngleLocsData.json".format(new_tar_name,bs_name,new_tar_side)
                        target_fullpath = loc_data_folder_path + "/" + target_filename
                        cone_fullpath = loc_data_folder_path + "/" + cone_filename
                        saveJson(target_fullpath,target_conection_data)
                        saveJson(cone_fullpath,cone_data)
                        locsDispInfoExporter(base_conection,loc_data_folder_path,bs_name)
   
    poseInterpolatorExporter(pose_data_folder_path)    