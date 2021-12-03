
def LocShooterImporter(correctives_directory):
    import maya.cmds as cmds
    import json
    import os
    import sys
    
    loc_data_path = "{}/data/locsShooterData".format(correctives_directory)
    loc_data_list = os.listdir(loc_data_path)
    
    def loadJson(path):
        with open(path, 'rb') as fp:
            data = json.load(fp)
            return data
            
    def vectorsDisp(name):
        base_loc = cmds.spaceLocator(n="{}_Base".format(name))[0]
        target_loc = cmds.spaceLocator(n="{}_Target".format(name))[0]
        pose_loc = cmds.spaceLocator(n="{}_Pose".format(name))[0]
        cmds.setAttr("{}.visibility".format(base_loc),0)
        cmds.setAttr("{}.visibility".format(target_loc),0)
        cmds.setAttr("{}.visibility".format(pose_loc),0)
        target_vector_sub = cmds.createNode("plusMinusAverage",n="{}_targetVectorSub".format(name))
        cmds.setAttr("{}.operation".format(target_vector_sub),2)
        current_pose_sub = cmds.createNode("plusMinusAverage",n="{}_CurrentPoseSub".format(name))
        cmds.setAttr("{}.operation".format(current_pose_sub),2)
        cmds.connectAttr("{}.worldPosition[0]".format(target_loc),"{}.input3D[0]".format(target_vector_sub))
        cmds.connectAttr("{}.worldPosition[0]".format(base_loc),"{}.input3D[1]".format(target_vector_sub))
        cmds.connectAttr("{}.worldPosition[0]".format(pose_loc),"{}.input3D[0]".format(current_pose_sub))
        cmds.connectAttr("{}.worldPosition[0]".format(base_loc),"{}.input3D[1]".format(current_pose_sub))
        angle = cmds.createNode("angleBetween",n="{}_angle".format(name))
        cmds.connectAttr("{}.output3D".format(target_vector_sub),"{}.vector1".format(angle))
        cmds.connectAttr("{}.output3D".format(current_pose_sub),"{}.vector2".format(angle))
        cmds.addAttr(base_loc,ln="coneAngle",k=True,at="double",dv=180)
        cmds.setAttr ("{}.coneAngle".format(base_loc),channelBox= True)
        cmds.addAttr(base_loc,ln="result",k=True,at="double",dv=0)
        cmds.setAttr ("{}.result".format(base_loc),channelBox= True)
        half_coneangle_doublelinear = cmds.createNode("multDoubleLinear",n="{}_halfConeangleDoublelinear".format(name))
        cmds.connectAttr("{}.coneAngle".format(base_loc),"{}.input1".format(half_coneangle_doublelinear))
        cmds.setAttr("{}.input2".format(half_coneangle_doublelinear),0.5)
        proportion_div = cmds.createNode("multiplyDivide",n="{}_proportionDiv".format(name))
        cmds.setAttr("{}.operation".format(proportion_div),2)
        cmds.connectAttr("{}.angle".format(angle),"{}.input1X".format(proportion_div))
        cmds.connectAttr("{}.output".format(half_coneangle_doublelinear),"{}.input2X".format(proportion_div))
        proportion_sub = cmds.createNode("plusMinusAverage",n="{}_proportionSub".format(name))
        cmds.setAttr("{}.operation".format(proportion_sub),2)
        cmds.setAttr("{}.input1D[0]".format(proportion_sub),1)
        cmds.connectAttr("{}.outputX".format(proportion_div),"{}.input1D[1]".format(proportion_sub))
        outcone_clamp = cmds.createNode("clamp",n="{}_outConeClamp".format(name))
        cmds.setAttr("{}.minR".format(outcone_clamp),0)
        cmds.setAttr("{}.maxR".format(outcone_clamp),1)
        cmds.connectAttr("{}.output1D".format(proportion_sub),"{}.inputR".format(outcone_clamp))
        cmds.connectAttr("{}.outputR".format(outcone_clamp),"{}.result".format(base_loc))
        
    
    #Creacion de los locators
    loc_namespace_list = []    
    for loc_filename in loc_data_list:
        loc_usage = loc_filename.split("_")[2]
        if loc_usage == "matrixLocsData.json":
            loc_name = loc_filename.split("_")[0]
            loc_side = loc_filename.split("_")[1]
            loc_namespace = "{}_{}".format(loc_name,loc_side)
            loc_namespace_list.append(loc_namespace)
    for name_space in loc_namespace_list:
        vectorsDisp(name_space)
    
                        
    #Obtencion de datos
    
    
    for loc_data in loc_data_list:
        loc_data_usage = loc_data.split("_")[2]
        if loc_data_usage == "matrixLocsData.json":
            full_path_loc = loc_data_path+"/"+loc_data
            matrix_data = loadJson(full_path_loc)
            matrix_value_all = matrix_data.values()
            matrix_value_one = matrix_value_all[0]
            matrix_value_two = matrix_value_all[1]
            matrix_value_three = matrix_value_all[2]
            loc_all = matrix_data.keys()
            loc_one = loc_all[0]
            loc_two = loc_all[1]
            loc_three = loc_all[2]
            cmds.xform(loc_one,matrix=matrix_value_one,ws=True)
            cmds.xform(loc_two,matrix=matrix_value_two,ws=True)
            cmds.xform(loc_three,matrix=matrix_value_three,ws=True)
            
        if loc_data_usage == "parentsLocsData.json":
            full_path_loc = loc_data_path+"/"+loc_data
            parent_data = loadJson(full_path_loc)
            parent_all = parent_data.values()
            parent_one = parent_all[0]
            parent_two = parent_all[1]
            parent_three = parent_all[2]
            child_all = parent_data.keys()
            child_one = child_all[0]
            child_two = child_all[1]
            child_three = child_all[2]
            parent_oe = cmds.objExists(parent_one)
            if parent_oe == True:
                try:
                    cmds.parent(child_one,parent_one)
                except RuntimeError:
                    skip = True
                try:
                    cmds.parent(child_two,parent_two)
                except RuntimeError:
                    skip = True
                try:
                    cmds.parent(child_three,parent_three)
                except RuntimeError:
                    skip = True
        if loc_data_usage == "targetsLocsData.json":
            full_path_loc = loc_data_path+"/"+loc_data
            targets_data = loadJson(full_path_loc)
            target = targets_data.keys()[0]
            loc_base =targets_data.values()[0]
            cmds.connectAttr("{}.result".format(loc_base),target)
        if loc_data_usage == "coneAngleLocsData.json":
            full_path_loc = loc_data_path+"/"+loc_data
            cone_data = loadJson(full_path_loc)
            coneangle_value_str = cone_data.keys()[0]
            coneangle_value = float(coneangle_value_str)
            loc_base =cone_data.values()[0]
            cmds.setAttr("{}.coneAngle".format(loc_base),coneangle_value)
            

def DrivenShooterImporter(correctives_directory):
    import maya.cmds as cmds
    import json
    import os
    import sys
    
    driven_data_path = "{}/data/drivenShooterData".format(correctives_directory)
    driven_data_list = os.listdir(driven_data_path)
    
    def loadJson(path):
        with open(path, 'rb') as fp:
            data = json.load(fp)
            return data
    
    bs_list =[]
    driver_list =[]
    target_list =[]
    
    tranform_values_list =[]
    blend_values_list =[]
    
    for files in driven_data_list:
        file_usage = files.split("_")[-1]
        target = files.replace("_{}".format(file_usage),"")
        if file_usage == "id.json":
            full_path = driven_data_path +"/"+files
            animdrive_data = loadJson(full_path)
            driven_data = animdrive_data.keys()[0]
            bs_data = animdrive_data.values()[0]
            bs_list.append(bs_data)
            driver_list.append(driven_data)
            target_list.append(target)
        
        if file_usage == "dv.json":
            full_path = driven_data_path +"/"+files
            driven_values_data = loadJson(full_path)
            transform_values = driven_values_data.keys()
            blend_value = driven_values_data.values()
            tranform_values_list.append(transform_values)
            blend_values_list.append(blend_value)
            
    divenkeys_range = len(bs_list)
    for x in range(0,divenkeys_range):
        bs = bs_list[x]
        driver = driver_list[x]
        target = target_list[x]
        tranform_values_own_list = tranform_values_list[x]
        blend_values_own_list = blend_values_list[x]
        values_range = len(tranform_values_own_list)
        for y in range(0,values_range):
            tranform_value = tranform_values_own_list[y]
            blend_value = blend_values_own_list[y]
            try:
                cmds.setDrivenKeyframe(bs, at=target, cd=driver, dv=float(tranform_value), v=blend_value)
            except RuntimeError:
                min_v = min(tranform_values_own_list)
                max_v = max(tranform_values_own_list)
                driver_obj = driver.split(".")[0]
                driver_attr = driver.split(".")[1]
                cmds.addAttr(driver_obj,ln=driver_attr,k=True,at="double",dv=0,max=float(max_v),min=float(min_v))
                cmds.setAttr (driver,channelBox= True)
                cmds.setAttr (driver,e=True,keyable= True)
                cmds.setDrivenKeyframe(bs, at=target, cd=driver, dv=float(tranform_value), v=blend_value)    
   
def poseInterpolatorImporter(correctives_directory):
    import maya.cmds as cmds
    import os
    pose_data_path = "{}/data/poseInterpolatorData".format(correctives_directory)
    pose_data_list = os.listdir(pose_data_path)
    pose_len = len(pose_data_list)
    pose_grp = cmds.group(em=True,n="poseInterpolator_c_grp")
    for x in range(0,pose_len):
        pose_data = pose_data_list[x]
        pose_path = "{}/{}".format(pose_data_path,pose_data)
        n = x+1
        poses = pose_data.split(".")[0]
        cmds.poseInterpolator(im=pose_path,i=n)
        cmds.parent(poses,pose_grp)
    cmds.select(cl=True)
    name = cmds.pickWalk(d="up")[0]
    rig_grp = "{}Rig_c_grp".format(name)
    try:
        cmds.parent(pose_grp,rig_grp)
    except ValueError:
        skip = True
        