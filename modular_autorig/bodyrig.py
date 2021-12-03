""" Autorig de cuerpo Bipedo Modular
     Basado en el rig de Carlos Contreras "Polilla" impartido en U-tad y programado por
     Gonzalo Berrocal """
import maya.cmds as cmds
from maya import OpenMaya
import math
from PySide2 import QtUiTools
from PySide2 import QtWidgets
from PySide2 import QtCore
#-------------
from maya import OpenMayaUI
from shiboken2 import wrapInstance 
import os.path
number_s = 0
number_n = 0
number_c_r = 0
number_c_l = 0
number_a_l = 0
number_a_r = 0
number_l_l = 0
number_l_r = 0
number_f_l = 0
number_f_r = 0
snap_points = False
def ModularAutorig():     
    global number_s
    number_s = 0
    global number_n
    number_n = 0
    global number_c_r
    number_c_r = 0
    global number_c_l
    number_c_l = 0
    global number_a_l
    number_a_l = 0
    global number_a_r
    number_a_r = 0
    global number_l_l
    number_l_l = 0
    global number_l_r
    number_l_r = 0
    global number_f_l
    number_f_l = 0
    global number_f_r
    number_f_r = 0
    def loadUi(fichero):
        maya_window_ptr = OpenMayaUI.MQtUtil.mainWindow() 
        maya_window_w = wrapInstance(long(maya_window_ptr  ), QtWidgets.QWidget) 
        #-------------
        # cargar el fichero .ui
        # Importante cambiar los \ por / 
        #-------------
        loader = QtUiTools.QUiLoader()
        ui_file = QtCore.QFile(fichero)
        ui_file.open(QtCore.QFile.ReadOnly)
        ui = loader.load(ui_file, parentWidget=maya_window_w)
        ui_file.close()
        ui.show()
        return ui
    
    homedir = os.path.expanduser("~")
    final_homedir = "{}/maya/scripts/modular_autorig/windows/".format(homedir)
    final_two_homedir = "{}/maya/scripts/modular_autorig/".format(homedir)
    min = loadUi("{}Modular Autorig Main.ui".format(final_homedir))
    #name = "char"
    def ModularAutorigBuilder():
        name = min.textEditName.text()
        win = loadUi("{}Modular Autorig.ui".format(final_homedir))
        
        
        # Variables
        pathControles = "{}/controles_ref.mb".format(final_two_homedir)
        char_group = name
        char_controls  = "{}Controls".format(name)
        char_DoNotTouch  = "{}DoNotTouch".format(name)
        
        char_geometry = "{}Geomety_c_grp".format(name)
        char_skeleton = "{}Skeleton_c_grp".format(name)
        char_rig = "{}Rig_c_grp".format(name)
        
        body_locs = "{}BodyLocs_c_grp".format(name)
        body_rig = "{}BodyRig_c_grp".format(name)
        spine_rig = "{}SpineRig_c_grp".format(name)
        neck_rig = "{}NeckRig_c_grp".format(name)
        
        arm_l_rig = "{}ArmRig_l_grp".format(name)
        arm_r_rig ="{}ArmRig_r_grp".format(name)
        
        leg_l_rig = "{}LegRig_l_grp".format(name)
        leg_r_rig = "{}LegRig_r_grp".format(name)
        
        hand_rig = "{}HandRig_c_grp".format(name)
        
        control_base = "base_c_ctr_1"
        control_center = "center_c_ctr_1"
        def AttrSeparator(input):
            cmds.addAttr(input,ln= "_", at="enum",en="attr")
            cmds.setAttr ("{}._".format(input),channelBox= True)
        def Start():               
            #Creacion de estructura
            char_group = cmds.group(n=name,em=1)
            char_controls  = cmds.group(n="{}Controls".format(name),em=1,p=char_group)
            char_DoNotTouch  = cmds.group(n="{}DoNotTouch".format(name),em=1,p=char_group)
            
            char_geometry = cmds.group(n="{}Geomety_c_grp".format(name),em=1,p=char_DoNotTouch)
            char_skeleton = cmds.group(n="{}Skeleton_c_grp".format(name),em=1,p=char_DoNotTouch)
            char_rig = cmds.group(n="{}Rig_c_grp".format(name),em=1,p=char_DoNotTouch)
            
            body_locs = cmds.group(n="{}BodyLocs_c_grp".format(name),em=1,p=char_rig)
            body_rig = cmds.group(n="{}BodyRig_c_grp".format(name),em=1,p=char_rig)
            spine_rig = cmds.group(n="{}SpineRig_c_grp".format(name),em=1,p=body_rig)
            neck_rig = cmds.group(n="{}NeckRig_c_grp".format(name),em=1,p=body_rig)
            
            arm_l_rig = cmds.group(n="{}ArmRig_l_grp".format(name),em=1,p=body_rig)
            arm_r_rig = cmds.group(n="{}ArmRig_r_grp".format(name),em=1,p=body_rig)
            
            leg_l_rig = cmds.group(n="{}LegRig_l_grp".format(name),em=1,p=body_rig)
            leg_r_rig = cmds.group(n="{}LegRig_r_grp".format(name),em=1,p=body_rig)
            
            hand_rig = cmds.group(n="{}HandRig_c_grp".format(name),em=1,p=body_rig)
            #Importacion de controles
            
            controls = cmds.file(pathControles,
            				i=True,type="mayaBinary",
            				ignoreVersion=True,
            				mergeNamespacesOnClash=False, 
            				rpr="Controles",
            				options ="v=0;",
            				pr=True,
            				importFrameRate=True,
            				importTimeRange="override")
            cmds.setAttr("controles.visibility",0)
            #2.2.1 Control Base
            control_base = cmds.duplicate("base_c_ctr_0",n="base_c_ctr_1")[0]
            cmds.xform(control_base, matrix=[1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0] ,worldSpace=True)
            
            AttrSeparator(control_base)    
            cmds.addAttr(control_base,ln= "globalScale",at= "double",min= 0.01,dv=1,k=True)
            base_offset = CreateOffset(control_base,"1")
            cmds.parent(base_offset,char_controls)
            for axis in "XYZ":
                cmds.connectAttr("{}.globalScale".format(control_base),"{}.scale{}".format(control_base,axis))
                cmds.connectAttr("{}.globalScale".format(control_base),"{}.scale{}".format(char_skeleton,axis))
            
                    
            #2.2.2 Control Center
            control_center = cmds.duplicate("center_c_ctr_0",n="center_c_ctr_1")[0]
            cmds.xform(control_center, matrix=[1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0] ,worldSpace=True)
            center_offset = CreateOffset(control_center,"1")
            cmds.parent(center_offset,control_base)
        
        try:
            cmds.select(cl=True)
            cmds.select("*_point_*")
            global snap_points
            snap_points = True
        except ValueError:
            global snap_points
            snap_points = False
        def clickNumberSpine():
            global number_s
            number_s += 1
        
        win.spineLocsButton.clicked.connect(clickNumberSpine)
        def clickNumberNeck():
            global number_n
            number_n += 1  
        
        win.neckLocsButton.clicked.connect(clickNumberNeck)
        def clickNumberClavicleRight():
            global number_c_r
            number_c_r += 1  
            
        def clickNumberClavicleLeft():
            global number_c_l
            number_c_l += 1 
            
        win.ClavicleRightLocsButton.clicked.connect(clickNumberClavicleRight)
        win.ClavicleLeftLocsButton.clicked.connect(clickNumberClavicleLeft)
        
    
        def clickNumberArmLeft():
            global number_a_l
            number_a_l += 1 
        
    
        def clickNumberArmRight():
            global number_a_r
            number_a_r += 1 
        
        win.ArmRightLocsButton.clicked.connect(clickNumberArmRight)
        win.ArmLeftLocsButton.clicked.connect(clickNumberArmLeft)
        
    
        def clickNumberLegLeft():
            global number_l_l
            number_l_l += 1 
        
    
        def clickNumberLegRight():
            global number_l_r
            number_l_r += 1 
        
        win.LegLeftLocsButton.clicked.connect(clickNumberLegLeft)
        win.LegRightLocsButton.clicked.connect(clickNumberLegRight)
        
        def clickNumberFingerLeft():
            global number_f_l
            number_f_l += 1
            
        def clickNumberFingerRight():
            global number_f_r
            number_f_r += 1
        
        win.FingerLeftLocsButton.clicked.connect(clickNumberFingerLeft)
        win.FingerRightLocsButton.clicked.connect(clickNumberFingerRight)
                    
        def MirrorLocClavicle():
            sel = cmds.ls(sl=1)
            obj = sel[0] 
            side_r = "_r_"
            side_l = "_l_" 
            if side_r in obj:
                clickNumberClavicleLeft()
                for input in sel:
                    new_name = "{}_l_loc_{}".format(input.split("_")[0],number_c_l)
                    mirror_side = cmds.duplicate(input,n = new_name)[0]
                    a = cmds.getAttr("{}.translateX".format(mirror_side))
                    cmds.setAttr("{}.translateX".format(mirror_side),0-a)
                    try:
                        cmds.parent(mirror_side,"{}BodyLocs_c_grp".format(name))
                    except RuntimeError:
                        print "Mirror Ok"
            if side_l in obj:
                clickNumberClavicleRight()
                for input in sel:
                    new_name = "{}_r_loc_{}".format(input.split("_")[0],number_c_r)
                    mirror_side = cmds.duplicate(input,n = new_name)[0]
                    a = cmds.getAttr("{}.translateX".format(mirror_side))
                    cmds.setAttr("{}.translateX".format(mirror_side),0-a)
                    try:
                        cmds.parent(mirror_side,"{}BodyLocs_c_grp".format(name))
                    except RuntimeError:
                        print "Mirror Ok"
        win.mirrorLocsClavicleButton.clicked.connect(MirrorLocClavicle)            
        
        def MirrorLocArm():
            sel = cmds.ls(sl=1)
            obj = sel[0] 
            side_r = "_r_"
            side_l = "_l_" 
            if side_r in obj:
                clickNumberArmLeft()
                for input in sel:
                    new_name = "{}_l_loc_{}".format(input.split("_")[0],number_a_l)
                    mirror_side = cmds.duplicate(input,n = new_name)[0]
                    a = cmds.getAttr("{}.translateX".format(mirror_side))
                    cmds.setAttr("{}.translateX".format(mirror_side),0-a)
                    try:
                        cmds.parent(mirror_side,"{}BodyLocs_c_grp".format(name))
                    except RuntimeError:
                        print "Mirror Ok"
            if side_l in obj:
                clickNumberArmRight()
                for input in sel:
                    new_name = "{}_r_loc_{}".format(input.split("_")[0],number_a_r)
                    mirror_side = cmds.duplicate(input,n = new_name)[0]
                    a = cmds.getAttr("{}.translateX".format(mirror_side))
                    cmds.setAttr("{}.translateX".format(mirror_side),0-a)
                    try:
                        cmds.parent(mirror_side,"{}BodyLocs_c_grp".format(name))
                    except RuntimeError:
                        print "Mirror Ok"         
        win.mirrorLocsArmButton.clicked.connect(MirrorLocArm)
        
        def MirrorLocLeg():
            sel = cmds.ls(sl=1)
            obj = sel[0] 
            side_r = "_r_"
            side_l = "_l_" 
            if side_r in obj:
                clickNumberLegLeft()
                for input in sel:
                    new_name = "{}_l_loc_{}".format(input.split("_")[0],number_l_l)
                    mirror_side = cmds.duplicate(input,n = new_name)[0]
                    a = cmds.getAttr("{}.translateX".format(mirror_side))
                    cmds.setAttr("{}.translateX".format(mirror_side),0-a)
                    try:
                        cmds.parent(mirror_side,"{}BodyLocs_c_grp".format(name))
                    except RuntimeError:
                        print "Mirror Ok"
            if side_l in obj:
                clickNumberLegRight()
                for input in sel:
                    new_name = "{}_r_loc_{}".format(input.split("_")[0],number_l_r)
                    mirror_side = cmds.duplicate(input,n = new_name)[0]
                    a = cmds.getAttr("{}.translateX".format(mirror_side))
                    cmds.setAttr("{}.translateX".format(mirror_side),0-a)
                    try:
                        cmds.parent(mirror_side,"{}BodyLocs_c_grp".format(name))
                    except RuntimeError:
                        print "Mirror Ok"         
        win.mirrorLocsLegButton.clicked.connect(MirrorLocLeg)
        def MirrorLocFinger():
            sel = cmds.ls(sl=1)
            obj = sel[0] 
            side_r = "_r_"
            side_l = "_l_" 
            if side_r in obj:
                clickNumberFingerLeft()
                for input in sel:
                    new_name = "{}_l_loc_{}".format(input.split("_")[0],number_f_l)
                    mirror_side = cmds.duplicate(input,n = new_name)[0]
                    a = cmds.getAttr("{}.translateX".format(mirror_side))
                    cmds.setAttr("{}.translateX".format(mirror_side),0-a)
                    try:
                        cmds.parent(mirror_side,"{}BodyLocs_c_grp".format(name))
                    except RuntimeError:
                        print "Mirror Ok"
            if side_l in obj:
                clickNumberFingerRight()
                for input in sel:
                    new_name = "{}_r_loc_{}".format(input.split("_")[0],number_f_r)
                    mirror_side = cmds.duplicate(input,n = new_name)[0]
                    a = cmds.getAttr("{}.translateX".format(mirror_side))
                    cmds.setAttr("{}.translateX".format(mirror_side),0-a)
                    try:
                        cmds.parent(mirror_side,"{}BodyLocs_c_grp".format(name))
                    except RuntimeError:
                        print "Mirror Ok"         
        win.mirrorLocsFingerButton.clicked.connect(MirrorLocFinger)
        
        def ImportPoints():
            points_directory = cmds.fileDialog2(dialogStyle=2,fm=1,caption="import",okc="Import")[0]
            points =cmds.file(points_directory,
        					i=True,
        					type="mayaBinary",
        					ignoreVersion=True,
        					mergeNamespacesOnClash=False, 
        					rpr="Controles",
        					options ="v=0;",
        					pr=True,
        					importFrameRate=True,
        					importTimeRange="override")				
            global snap_points
            snap_points = True 
            cmds.select("*_point_*",add=True)
            point = cmds.ls (sl=1)[0]
            point_group = cmds.listRelatives(point,parent=True)[0]
            cmds.parent(point_group,char_rig)
        win.pushButtonImportPoints.clicked.connect(ImportPoints)
        
        def ExportPoints():
            try:
                sel = cmds.ls(sl=1)
                n = len(sel)
                if n is 0:
                    cmds.select("{}BodyPoints_c_grp".format(name))
                    sel = cmds.ls(sl=1)
                parents = cmds.listRelatives(sel[0],p=True)[0]
                cmds.parent(sel[0],w=1)
                points_directory = cmds.fileDialog2(dialogStyle=2,fm=0,caption="import",okc="Save")[0]
                points_directory = points_directory.replace("*","mb")
                cmds.file(points_directory,force=True,options= "v=0;",typ="mayaBinary",pr=True,es=True)
                cmds.parent(sel[0],parents) 
            except ValueError:
                print "Select Point group"
        win.pushButtonExportPoints.clicked.connect(ExportPoints)
          
        def DisableSnapPoints():
            global snap_points
            snap_points = False
            print "Snap Points Disabled" 
        win.pushButtonDisableSnapPoints.clicked.connect(DisableSnapPoints)
        
        def ConvertLocsToPoints():    
            try:
                sel = cmds.ls(sl=1)
                n = len(sel)
                
                if n is 0:
                    cmds.select("{}BodyLocs_c_grp".format(name))
                    sel = cmds.ls(sl=1)
                sel = sel[0]
                if "grp" in sel.split("_")[2]:
                    children = cmds.listRelatives(c=True,type="transform")
                    body_points = cmds.group(n="{}BodyPoints_c_grp".format(name),em=1,p=char_rig)
                    for x in children:
                        if "loc" in x.split("_")[2]:
                            point = cmds.duplicate(x,n="{}_{}_point_{}".format(x.split("_")[0],x.split("_")[1],x.split("_")[3]))[0]
                            cmds.parent(point,body_points)
                            for axis in "XYZ":
                                cmds.setAttr("{}.localScale{}".format(point,axis),0.1)
                                
                else:
                    print "Select Point group"                    
            except ValueError:
                    print "Select Point group"  
        win.pushButtonConvertLocsPoints.clicked.connect(ConvertLocsToPoints)  
        # Algunas definiciones para todo el AutoRig
        
            #Create Offset
        def CreateOffset(input,number):
            a = cmds.listRelatives(input,p=True)
            con = cmds.polyCone()
            b = cmds.listRelatives(con,p=True)
            c = type(a)
            d = type(b)
            f = c is d
            obj_name = input.split("_")[0]
            obj_side = input.split("_")[1]
            obj_usage = input.split("_")[2]
            group_name = "{}{}_{}_zero_{}".format(obj_name,obj_usage.capitalize(),obj_side,number)
            if f is False: 
                group = cmds.group(em=1,n = group_name)
                p_constraint = cmds.pointConstraint(input,group,mo=0)
                o_constraint = cmds.orientConstraint(input,group,mo=0)
                cmds.delete (p_constraint)
                cmds.delete (o_constraint)
                cmds.parent(input,group)
                cmds.parent(group,a)
                cmds.delete(con)
                return group
            else:
                group = cmds.group(em=1,n = group_name)
                p_constraint = cmds.pointConstraint(input,group,mo=0)
                o_constraint = cmds.orientConstraint(input,group,mo=0)
                cmds.delete (p_constraint)
                cmds.delete (o_constraint)
                cmds.parent(input,group)
                cmds.delete(con)
                return group
        
            #JointChain         
        def JointChain(selection_one,selection_two,name,amount):    
            start_point = cmds.xform(str(selection_one), q=1, t=1)
            end_point = cmds.xform(str(selection_two), q=1, t=1)
            cmds.select(cl=1)
            name = name
            parent = True
            amount = amount 
            def createJointChain(start_point, end_point, amount, name, chain): 
                import maya.cmds as cmds 
                from maya.api import OpenMaya 
                cmds.select(cl=1)  
                start_vector = OpenMaya.MVector(start_point)    
                end_vector = OpenMaya.MVector(end_point)  
                dif_point = end_vector- start_vector  
                ofset = 1.0/(amount-1)  
                new_point = dif_point*ofset  
                cmds.xform(t=list(new_point))   
                final_point= start_vector + new_point  
                cmds.xform(t=list(final_point))  
                all_joints =[] 
                final_all_joints = []  
                for i in range(amount):  
                    mid_pos = dif_point*(ofset*i)  
                    final_pos = start_vector + mid_pos  
                    pos_joint = list(final_pos)  
                    jnt = cmds.joint (p= pos_joint)  
                    all_joints.append(jnt)  
                    if i !=0:  
                        cmds.joint(all_joints[i-1], e=True, zso=True, oj="xyz", sao="yup")  
                cont = 1  
                for created_joints in all_joints:    
                    new_name = name + str(cont).zfill(2)  
                    cont=cont+1  
                    final_name = cmds.rename(created_joints,new_name) 
                    final_all_joints.append(final_name)  
                parents_joints = final_all_joints[1:] 
                if chain is False: 
                    cmds.parent(parents_joints, w=1) 
                cmds.select(cl=1) 
                return final_all_joints 
                
             
            joints_list = createJointChain(start_point, end_point,amount,str(name), parent)
            last_joint = joints_list[-1]
            for axis in "XYZ":
                cmds.setAttr("{}.jointOrient{}".format(last_joint,axis),0)
            return joints_list
        
        # Pole Vector Pos:
        def PoleVector(sel,side):    
            start = cmds.xform(sel[0] ,q= 1 ,ws = 1,t =1 )
            mid = cmds.xform(sel[1] ,q= 1 ,ws = 1,t =1 )
            end = cmds.xform(sel[2] ,q= 1 ,ws = 1,t =1 )
            startV = OpenMaya.MVector(start[0] ,start[1],start[2])
            midV = OpenMaya.MVector(mid[0] ,mid[1],mid[2])
            endV = OpenMaya.MVector(end[0] ,end[1],end[2])
            startEnd = endV - startV
            startMid = midV - startV
            dotP = startMid * startEnd
            proj = float(dotP) / float(startEnd.length())
            startEndN = startEnd.normal()
            projV = startEndN * proj
            arrowV = startMid - projV
            arrowV*= 0.5 
            finalV = arrowV + midV
            cross1 = startEnd ^ startMid
            cross1.normalize()
            cross2 = cross1 ^ arrowV
            cross2.normalize()
            arrowV.normalize()
            matrixV = [arrowV.x , arrowV.y , arrowV.z , 0 , 
            cross1.x ,cross1.y , cross1.z , 0 ,
            cross2.x , cross2.y , cross2.z , 0,
            0,0,0,1]
            matrixM = OpenMaya.MMatrix()
            OpenMaya.MScriptUtil.createMatrixFromList(matrixV , matrixM)
            matrixFn = OpenMaya.MTransformationMatrix(matrixM)
            rot = matrixFn.eulerRotation()
            loc = cmds.spaceLocator(n="PoleVector_{}_loc".format(side))[0]
            cmds.xform(loc , ws =1 , t= (finalV.x , finalV.y ,finalV.z))
            cmds.xform ( loc , ws = 1 , rotation = ((rot.x/math.pi*180.0),
            (rot.y/math.pi*180.0),
            (rot.z/math.pi*180.0)))
            return loc
        # Funcion para ocultar    
        def Hide(input):
            cmds.setAttr("{}.visibility".format(input),0)
        
        # Funciones para loquear
        def LockScaleVis(input):
            for axis in "xyz":
                cmds.setAttr("{}.s{}".format(input,axis),lock=True,keyable=False,channelBox=False)
            cmds.setAttr("{}.v".format(input),lock=True,keyable=False,channelBox=False) 
        
        def LockAll(input):
            for axis in "xyz":
                cmds.setAttr("{}.t{}".format(input,axis),lock=True,keyable=False,channelBox=False)
                cmds.setAttr("{}.r{}".format(input,axis),lock=True,keyable=False,channelBox=False)
                cmds.setAttr("{}.s{}".format(input,axis),lock=True,keyable=False,channelBox=False) 
            cmds.setAttr("{}.v".format(input),lock=True,keyable=False,channelBox=False)
            
        def LockScaleRotVis(input):
            for axis in "xyz":
                cmds.setAttr("{}.r{}".format(input,axis),lock=True,keyable=False,channelBox=False)
                cmds.setAttr("{}.s{}".format(input,axis),lock=True,keyable=False,channelBox=False)
            cmds.setAttr("{}.v".format(input),lock=True,keyable=False,channelBox=False)
            
        def LockScaleTransVis(input):
            for axis in "xyz":
                cmds.setAttr("{}.t{}".format(input,axis),lock=True,keyable=False,channelBox=False)
                cmds.setAttr("{}.s{}".format(input,axis),lock=True,keyable=False,channelBox=False)
            cmds.setAttr("{}.v".format(input),lock=True,keyable=False,channelBox=False)
        
        #Creacion de locators
        locs_list =[]
        def CreateSpineLocs(): 
            spine_dw = cmds.spaceLocator(n="spineDw_c_loc_{}".format(number_s))[0]
            locs_list.append(spine_dw)
            cmds.setAttr("{}.rotateZ".format(spine_dw),90)
            spine_up = cmds.duplicate(spine_dw, n="spineUp_c_loc_{}".format(number_s))[0]
            locs_list.append(spine_up)
            if snap_points is False:
                cmds.setAttr("{}.translateY".format(spine_dw),10)
                cmds.setAttr("{}.translateY".format(spine_up),15)
            else:
                cmds.matchTransform(spine_up,"spineUp_c_point_{}".format(number_s),pos=True,rot=False,scl=False)
                cmds.matchTransform(spine_dw,"spineDw_c_point_{}".format(number_s),pos=True,rot=False,scl=False)
                
        def CreateNeckLocs():
            neck_dw = cmds.spaceLocator(n="neckDw_c_loc_{}".format(number_n))[0]
            locs_list.append(neck_dw)
            cmds.setAttr("{}.rotateZ".format(neck_dw),90)
            neck_up = cmds.duplicate(neck_dw, n="neckUp_c_loc_{}".format(number_n))[0]
            locs_list.append(neck_up)
            if snap_points is False:
                cmds.setAttr("{}.translateY".format(neck_dw),17)
                cmds.setAttr("{}.translateY".format(neck_up),18)
            else:
                cmds.matchTransform(neck_up,"neckUp_c_point_{}".format(number_n),pos=True,rot=False,scl=False)
                cmds.matchTransform(neck_dw,"neckDw_c_point_{}".format(number_n),pos=True,rot=False,scl=False)
                   
        def CreateClavicleLocsRight():
            side_c = "r"
            clavicle = cmds.spaceLocator(n="clavicle_{}_loc_{}".format(side_c,number_c_r))[0]
            locs_list.append(clavicle)
            clavicle_end = cmds.duplicate(clavicle, n="clavicleEnd_{}_loc_{}".format(side_c,number_c_r))[0]
            locs_list.append(clavicle_end)
            if snap_points is False:
                cmds.setAttr("{}.translateY".format(clavicle),15)
                cmds.setAttr("{}.translateX".format(clavicle),-1)
                cmds.setAttr("{}.translateY".format(clavicle_end),16)
                cmds.setAttr("{}.translateX".format(clavicle_end),-5) 
            else:
                cmds.matchTransform(clavicle,"clavicle_{}_point_{}".format(side_c,number_c_r),pos=True,rot=False,scl=False)
                cmds.matchTransform(clavicle_end,"clavicleEnd_{}_point_{}".format(side_c,number_c_r),pos=True,rot=False,scl=False)
        
        def CreateClavicleLocsLeft():
            side_c = "l"
            clavicle = cmds.spaceLocator(n="clavicle_{}_loc_{}".format(side_c,number_c_l))[0]
            locs_list.append(clavicle)
            clavicle_end = cmds.duplicate(clavicle, n="clavicleEnd_{}_loc_{}".format(side_c,number_c_l))[0]
            locs_list.append(clavicle_end)
            if snap_points is False:
                cmds.setAttr("{}.translateY".format(clavicle),15)
                cmds.setAttr("{}.translateX".format(clavicle),1)
                cmds.setAttr("{}.translateY".format(clavicle_end),16)
                cmds.setAttr("{}.translateX".format(clavicle_end),5)
            else:
                cmds.matchTransform(clavicle,"clavicle_{}_point_{}".format(side_c,number_c_l),pos=True,rot=False,scl=False)
                cmds.matchTransform(clavicle_end,"clavicleEnd_{}_point_{}".format(side_c,number_c_l),pos=True,rot=False,scl=False)     
        
        def CreateArmLocsLeft():
            side_a = "l"
            shoulder = cmds.spaceLocator(n="shoulder_{}_loc_{}".format(side_a,number_a_l))[0]
            arm_cl_conexion_check = win.checkBoxArmClavicleConexion.isChecked()
            arm_cl_conexion = win.spinArmClavicleConexion.value()
            if snap_points is False:    
                if arm_cl_conexion_check is True:
                    try:
                        clavicle_end_pos =cmds.xform("clavicleEnd_{}_loc_{}".format(side_a,arm_cl_conexion),q=True,t=True,ws=True)
                        cmds.xform(shoulder,t=clavicle_end_pos,ws=True)
                    except ValueError:
                        cmds.setAttr("{}.translateX".format(shoulder),5.5)
                        cmds.setAttr("{}.translateY".format(shoulder),16)
                else:
                    cmds.setAttr("{}.translateX".format(shoulder),5.5)
                    cmds.setAttr("{}.translateY".format(shoulder),16) 
            locs_list.append(shoulder)
            elbow = cmds.spaceLocator(n="elbow_{}_loc_{}".format(side_a,number_a_l))[0]
            if snap_points is False:
                cmds.parent(elbow,shoulder)
                cmds.setAttr("{}.translateX".format(elbow),4.5)
                cmds.setAttr("{}.translateY".format(elbow),0)
                cmds.setAttr("{}.translateZ".format(elbow),0)
            locs_list.append(elbow)
            hand = cmds.spaceLocator(n="hand_{}_loc_{}".format(side_a,number_a_l))[0]
            if snap_points is False:
                cmds.parent(hand,elbow)
                cmds.setAttr("{}.translateX".format(hand),5)
                cmds.setAttr("{}.translateY".format(hand),0)
                cmds.setAttr("{}.translateZ".format(hand),0)
            locs_list.append(hand)
            hand_end = cmds.spaceLocator(n="handEnd_{}_loc_{}".format(side_a,number_a_l))[0]
            if snap_points is False:
                cmds.parent(hand_end,hand)
                cmds.setAttr("{}.translateX".format(hand_end),2)
                cmds.setAttr("{}.translateY".format(hand_end),0)
                cmds.setAttr("{}.translateZ".format(hand_end),0)
            else:
                cmds.matchTransform(shoulder,"shoulder_{}_point_{}".format(side_a,number_a_l),pos=True,rot=False,scl=False)
                cmds.matchTransform(elbow,"elbow_{}_point_{}".format(side_a,number_a_l),pos=True,rot=False,scl=False)
                cmds.matchTransform(hand,"hand_{}_point_{}".format(side_a,number_a_l),pos=True,rot=False,scl=False)
                cmds.matchTransform(hand_end,"handEnd_{}_point_{}".format(side_a,number_a_l),pos=True,rot=False,scl=False)      
            locs_list.append(hand_end)
            
        def CreateArmLocsRight():
            side_a = "r"
            shoulder = cmds.spaceLocator(n="shoulder_{}_loc_{}".format(side_a,number_a_r))[0]
            arm_cl_conexion_check = win.checkBoxArmClavicleConexion.isChecked()
            arm_cl_conexion = win.spinArmClavicleConexion.value()
            if snap_points is False:
                if arm_cl_conexion_check is True:
                    try:
                        clavicle_end_pos =cmds.xform("clavicleEnd_{}_loc_{}".format(side_a,arm_cl_conexion),q=True,t=True,ws=True)
                        cmds.xform(shoulder,t=clavicle_end_pos,ws=True)
                    except ValueError:
                        cmds.setAttr("{}.translateX".format(shoulder),-5.5)
                        cmds.setAttr("{}.translateY".format(shoulder),16)
                else:
                    cmds.setAttr("{}.translateX".format(shoulder),-5.5)
                    cmds.setAttr("{}.translateY".format(shoulder),16) 
            locs_list.append(shoulder)
            elbow = cmds.spaceLocator(n="elbow_{}_loc_{}".format(side_a,number_a_r))[0]
            if snap_points is False:
                cmds.parent(elbow,shoulder)
                cmds.setAttr("{}.translateX".format(elbow),-4.5)
                cmds.setAttr("{}.translateY".format(elbow),0)
                cmds.setAttr("{}.translateZ".format(elbow),0)
            locs_list.append(elbow)
            hand = cmds.spaceLocator(n="hand_{}_loc_{}".format(side_a,number_a_r))[0]
            if snap_points is False:
                cmds.parent(hand,elbow)
                cmds.setAttr("{}.translateX".format(hand),-5)
                cmds.setAttr("{}.translateY".format(hand),0)
                cmds.setAttr("{}.translateZ".format(hand),0)
            locs_list.append(hand)
            hand_end = cmds.spaceLocator(n="handEnd_{}_loc_{}".format(side_a,number_a_r))[0]
            if snap_points is False:
                cmds.parent(hand_end,hand)
                cmds.setAttr("{}.translateX".format(hand_end),-2)
                cmds.setAttr("{}.translateY".format(hand_end),0)
                cmds.setAttr("{}.translateZ".format(hand_end),0)
            else:
                cmds.matchTransform(shoulder,"shoulder_{}_point_{}".format(side_a,number_a_r),pos=True,rot=False,scl=False)
                cmds.matchTransform(elbow,"elbow_{}_point_{}".format(side_a,number_a_r),pos=True,rot=False,scl=False)
                cmds.matchTransform(hand,"hand_{}_point_{}".format(side_a,number_a_r),pos=True,rot=False,scl=False)
                cmds.matchTransform(hand_end,"handEnd_{}_point_{}".format(side_a,number_a_r),pos=True,rot=False,scl=False)
            locs_list.append(hand_end)
        
        def CreateLegLocsLeft():
            side_l = "l"
            spine_leg_conexion = win.checkBoxLegSpineConexion.isChecked()
            spine_leg_conexion_value = win.spinLegSpineConexion.value()
            
            if spine_leg_conexion is True:
                hip = cmds.spaceLocator(n="hip_{}_loc_{}".format(side_l,number_l_l))[0]
                if snap_points is False:
                    cmds.parent(hip,"spineDw_c_loc_{}".format(spine_leg_conexion_value))
                    cmds.setAttr("{}.translateX".format(hip),0)
                    cmds.setAttr("{}.translateY".format(hip),-1.5)
                knee = cmds.spaceLocator(n="knee_{}_loc_{}".format(side_l,number_l_l))[0]
                if snap_points is False:
                    cmds.parent(knee,hip)
                    cmds.setAttr("{}.translateX".format(knee),0)
                    cmds.setAttr("{}.translateY".format(knee),-4)
                foot = cmds.spaceLocator(n="foot_{}_loc_{}".format(side_l,number_l_l))[0]
                if snap_points is False:
                    cmds.parent(foot,knee)
                    cmds.setAttr("{}.translateX".format(foot),0)
                    cmds.setAttr("{}.translateY".format(foot),-5)
                ball = cmds.spaceLocator(n="ball_{}_loc_{}".format(side_l,number_l_l))[0]
                if snap_points is False:
                    cmds.parent(ball,foot)
                    cmds.setAttr("{}.translateX".format(ball),0)
                    cmds.setAttr("{}.translateZ".format(ball),2)
                toe = cmds.spaceLocator(n="toe_{}_loc_{}".format(side_l,number_l_l))[0]
                if snap_points is False:
                    cmds.parent(toe,ball)
                    cmds.setAttr("{}.translateX".format(toe),0)
                    cmds.setAttr("{}.translateZ".format(toe),1)
                heel = cmds.spaceLocator(n="heelPos_{}_loc_{}".format(side_l,number_l_l))[0]
                if snap_points is False:
                    cmds.parent(heel,toe)
                    cmds.setAttr("{}.translateX".format(heel),0)
                    cmds.setAttr("{}.translateZ".format(heel),-4) 
                bank_ext = cmds.spaceLocator(n="bankExtPos_{}_loc_{}".format(side_l,number_l_l))[0]
                if snap_points is False:
                    cmds.parent(bank_ext,ball)
                    cmds.setAttr("{}.translateX".format(bank_ext),-1)
                    cmds.setAttr("{}.translateZ".format(bank_ext),-1)
                bank_int = cmds.spaceLocator(n="bankIntPos_{}_loc_{}".format(side_l,number_l_l))[0]
                if snap_points is False:
                    cmds.parent(bank_int,ball)
                    cmds.setAttr("{}.translateX".format(bank_int),1)
                    cmds.setAttr("{}.translateZ".format(bank_int),-1)
                else:
                    cmds.matchTransform(hip,"hip_{}_point_{}".format(side_l,number_l_l),pos=True,rot=False,scl=False)
                    cmds.matchTransform(knee,"knee_{}_point_{}".format(side_l,number_l_l),pos=True,rot=False,scl=False)
                    cmds.matchTransform(foot,"foot_{}_point_{}".format(side_l,number_l_l),pos=True,rot=False,scl=False)
                    cmds.matchTransform(ball,"ball_{}_point_{}".format(side_l,number_l_l),pos=True,rot=False,scl=False)
                    cmds.matchTransform(toe,"toe_{}_point_{}".format(side_l,number_l_l),pos=True,rot=False,scl=False)
                    cmds.matchTransform(heel,"heelPos_{}_point_{}".format(side_l,number_l_l),pos=True,rot=False,scl=False)
                    cmds.matchTransform(bank_ext,"bankExtPos_{}_point_{}".format(side_l,number_l_l),pos=True,rot=False,scl=False)
                    cmds.matchTransform(bank_int,"bankIntPos_{}_point_{}".format(side_l,number_l_l),pos=True,rot=False,scl=False)
            else:
                hip = cmds.spaceLocator(n="hip_{}_loc_{}".format(side_l,number_l_l))[0]
                if snap_points is False:
                    cmds.setAttr("{}.translateX".format(hip),1)
                    cmds.setAttr("{}.translateY".format(hip),9.5)
                
                knee = cmds.spaceLocator(n="knee_{}_loc_{}".format(side_l,number_l_l))[0]
                if snap_points is False:
                    cmds.setAttr("{}.translateX".format(knee),1)
                    cmds.setAttr("{}.translateY".format(knee),6)
                
                foot = cmds.spaceLocator(n="foot_{}_loc_{}".format(side_l,number_l_l))[0]
                if snap_points is False:
                    cmds.setAttr("{}.translateX".format(foot),1)
                    cmds.setAttr("{}.translateY".format(foot),1)
                
                ball = cmds.spaceLocator(n="ball_{}_loc_{}".format(side_l,number_l_l))[0]
                if snap_points is False:
                    cmds.setAttr("{}.translateX".format(ball),1)
                    cmds.setAttr("{}.translateZ".format(ball),2)
                
                toe = cmds.spaceLocator(n="toe_{}_loc_{}".format(side_l,number_l_l))[0]
                if snap_points is False:
                    cmds.setAttr("{}.translateX".format(toe),1)
                    cmds.setAttr("{}.translateZ".format(toe),3)
                
                heel = cmds.spaceLocator(n="heelPos_{}_loc_{}".format(side_l,number_l_l))[0]
                if snap_points is False:
                    cmds.setAttr("{}.translateX".format(heel),1)
                    cmds.setAttr("{}.translateZ".format(heel),-1)
                
                bank_ext = cmds.spaceLocator(n="bankExtPos_{}_loc_{}".format(side_l,number_l_l))[0]
                if snap_points is False:
                    cmds.setAttr("{}.translateZ".format(bank_ext),1)
                
                bank_int = cmds.spaceLocator(n="bankIntPos_{}_loc_{}".format(side_l,number_l_l))[0]
                if snap_points is False:
                    cmds.setAttr("{}.translateX".format(bank_int),2)
                    cmds.setAttr("{}.translateZ".format(bank_int),1) 
                else:
                    cmds.matchTransform(hip,"hip_{}_point_{}".format(side_l,number_l_l),pos=True,rot=False,scl=False)
                    cmds.matchTransform(knee,"knee_{}_point_{}".format(side_l,number_l_l),pos=True,rot=False,scl=False)
                    cmds.matchTransform(foot,"foot_{}_point_{}".format(side_l,number_l_l),pos=True,rot=False,scl=False)
                    cmds.matchTransform(ball,"ball_{}_point_{}".format(side_l,number_l_l),pos=True,rot=False,scl=False)
                    cmds.matchTransform(toe,"toe_{}_point_{}".format(side_l,number_l_l),pos=True,rot=False,scl=False)
                    cmds.matchTransform(heel,"heelPos_{}_point_{}".format(side_l,number_l_l),pos=True,rot=False,scl=False)
                    cmds.matchTransform(bank_ext,"bankExtPos_{}_point_{}".format(side_l,number_l_l),pos=True,rot=False,scl=False)
                    cmds.matchTransform(bank_int,"bankIntPos_{}_point_{}".format(side_l,number_l_l),pos=True,rot=False,scl=False)
            leg_locs_list = [hip,knee,foot,ball,toe,heel,bank_ext,bank_int]
            
            for leg_loc in leg_locs_list:
                locs_list.append(leg_loc)
        
        def CreateLegLocsRight():
            side_l = "r"
            spine_leg_conexion = win.checkBoxLegSpineConexion.isChecked()
            spine_leg_conexion_value = win.spinLegSpineConexion.value()
            if spine_leg_conexion is True:
                hip = cmds.spaceLocator(n="hip_{}_loc_{}".format(side_l,number_l_r))[0]
                if snap_points is False:
                    cmds.parent(hip,"spineDw_c_loc_{}".format(spine_leg_conexion_value))
                    cmds.setAttr("{}.translateX".format(hip),0)
                    cmds.setAttr("{}.translateY".format(hip),1.5)
                knee = cmds.spaceLocator(n="knee_{}_loc_{}".format(side_l,number_l_r))[0]
                if snap_points is False:
                    cmds.parent(knee,hip)
                    cmds.setAttr("{}.translateX".format(knee),0)
                    cmds.setAttr("{}.translateY".format(knee),-4)
                foot = cmds.spaceLocator(n="foot_{}_loc_{}".format(side_l,number_l_r))[0]
                if snap_points is False:
                    cmds.parent(foot,knee)
                    cmds.setAttr("{}.translateX".format(foot),0)
                    cmds.setAttr("{}.translateY".format(foot),-5)
                ball = cmds.spaceLocator(n="ball_{}_loc_{}".format(side_l,number_l_r))[0]
                if snap_points is False:    
                    cmds.parent(ball,foot)
                    cmds.setAttr("{}.translateX".format(ball),0)
                    cmds.setAttr("{}.translateZ".format(ball),2)
                toe = cmds.spaceLocator(n="toe_{}_loc_{}".format(side_l,number_l_r))[0]
                if snap_points is False:
                    cmds.parent(toe,ball)
                    cmds.setAttr("{}.translateX".format(toe),0)
                    cmds.setAttr("{}.translateZ".format(toe),1)
                heel = cmds.spaceLocator(n="heelPos_{}_loc_{}".format(side_l,number_l_r))[0]
                if snap_points is False:
                    cmds.parent(heel,toe)
                    cmds.setAttr("{}.translateX".format(heel),0)
                    cmds.setAttr("{}.translateZ".format(heel),-4) 
                bank_ext = cmds.spaceLocator(n="bankExtPos_{}_loc_{}".format(side_l,number_l_r))[0]
                if snap_points is False:
                    cmds.parent(bank_ext,ball)
                    cmds.setAttr("{}.translateX".format(bank_ext),-1)
                    cmds.setAttr("{}.translateZ".format(bank_ext),-1)
                bank_int = cmds.spaceLocator(n="bankIntPos_{}_loc_{}".format(side_l,number_l_r))[0]
                if snap_points is False:
                    cmds.parent(bank_int,ball)
                    cmds.setAttr("{}.translateX".format(bank_int),1)
                    cmds.setAttr("{}.translateZ".format(bank_int),-1)
                else:
                    cmds.matchTransform(hip,"hip_{}_point_{}".format(side_l,number_l_r),pos=True,rot=False,scl=False)
                    cmds.matchTransform(knee,"knee_{}_point_{}".format(side_l,number_l_r),pos=True,rot=False,scl=False)
                    cmds.matchTransform(foot,"foot_{}_point_{}".format(side_l,number_l_r),pos=True,rot=False,scl=False)
                    cmds.matchTransform(ball,"ball_{}_point_{}".format(side_l,number_l_r),pos=True,rot=False,scl=False)
                    cmds.matchTransform(toe,"toe_{}_point_{}".format(side_l,number_l_r),pos=True,rot=False,scl=False)
                    cmds.matchTransform(heel,"heelPos_{}_point_{}".format(side_l,number_l_r),pos=True,rot=False,scl=False)
                    cmds.matchTransform(bank_ext,"bankExtPos_{}_point_{}".format(side_l,number_l_r),pos=True,rot=False,scl=False)
                    cmds.matchTransform(bank_int,"bankIntPos_{}_point_{}".format(side_l,number_l_r),pos=True,rot=False,scl=False)
                    
            else:    
                hip = cmds.spaceLocator(n="hip_{}_loc_{}".format(side_l,number_l_r))[0]
                if snap_points is False:
                    cmds.setAttr("{}.translateX".format(hip),-1)
                    cmds.setAttr("{}.translateY".format(hip),9.5)
                
                knee = cmds.spaceLocator(n="knee_{}_loc_{}".format(side_l,number_l_r))[0]
                if snap_points is False:
                    cmds.setAttr("{}.translateX".format(knee),-1)
                    cmds.setAttr("{}.translateY".format(knee),6)
                
                foot = cmds.spaceLocator(n="foot_{}_loc_{}".format(side_l,number_l_r))[0]
                if snap_points is False:
                    cmds.setAttr("{}.translateX".format(foot),-1)
                    cmds.setAttr("{}.translateY".format(foot),1)
                
                ball = cmds.spaceLocator(n="ball_{}_loc_{}".format(side_l,number_l_r))[0]
                if snap_points is False:
                    cmds.setAttr("{}.translateX".format(ball),-1)
                    cmds.setAttr("{}.translateZ".format(ball),2)
                
                toe = cmds.spaceLocator(n="toe_{}_loc_{}".format(side_l,number_l_r))[0]
                if snap_points is False:
                    cmds.setAttr("{}.translateX".format(toe),-1)
                    cmds.setAttr("{}.translateZ".format(toe),3)
                
                heel = cmds.spaceLocator(n="heelPos_{}_loc_{}".format(side_l,number_l_r))[0]
                if snap_points is False:
                    cmds.setAttr("{}.translateX".format(heel),-1)
                    cmds.setAttr("{}.translateZ".format(heel),-1)
                
                bank_ext = cmds.spaceLocator(n="bankExtPos_{}_loc_{}".format(side_l,number_l_r))[0]
                if snap_points is False:
                    cmds.setAttr("{}.translateZ".format(bank_ext),1)
                
                bank_int = cmds.spaceLocator(n="bankIntPos_{}_loc_{}".format(side_l,number_l_r))[0]
                if snap_points is False:
                    cmds.setAttr("{}.translateX".format(bank_int),-2)
                    cmds.setAttr("{}.translateZ".format(bank_int),1)
                else:
                    cmds.matchTransform(hip,"hip_{}_point_{}".format(side_l,number_l_r),pos=True,rot=False,scl=False)
                    cmds.matchTransform(knee,"knee_{}_point_{}".format(side_l,number_l_r),pos=True,rot=False,scl=False)
                    cmds.matchTransform(foot,"foot_{}_point_{}".format(side_l,number_l_r),pos=True,rot=False,scl=False)
                    cmds.matchTransform(ball,"ball_{}_point_{}".format(side_l,number_l_r),pos=True,rot=False,scl=False)
                    cmds.matchTransform(toe,"toe_{}_point_{}".format(side_l,number_l_r),pos=True,rot=False,scl=False)
                    cmds.matchTransform(heel,"heelPos_{}_point_{}".format(side_l,number_l_r),pos=True,rot=False,scl=False)
                    cmds.matchTransform(bank_ext,"bankExtPos_{}_point_{}".format(side_l,number_l_r),pos=True,rot=False,scl=False)
                    cmds.matchTransform(bank_int,"bankIntPos_{}_point_{}".format(side_l,number_l_r),pos=True,rot=False,scl=False)
            
            leg_locs_list = [hip,knee,foot,ball,toe,heel,bank_ext,bank_int]
            
            for leg_loc in leg_locs_list:
                locs_list.append(leg_loc)
        
        def CreateFingerLocsLeft():
            side_f = "l"
            parent_fin_check = win.checkBoxFingerHandConexion.isChecked()
            parent_fin_num = win.spinFingerHandConexion.value()
            
            fin_sec_a = cmds.spaceLocator(n="fingerSectionA_{}_loc_{}".format(side_f,number_f_l))[0]
            fin_sec_b = cmds.spaceLocator(n="fingerSectionB_{}_loc_{}".format(side_f,number_f_l))[0]
            fin_sec_c = cmds.spaceLocator(n="fingerSectionC_{}_loc_{}".format(side_f,number_f_l))[0]
            fin_end = cmds.spaceLocator(n="fingerEnd_{}_loc_{}".format(side_f,number_f_l))[0]
            finger_loc_list = [fin_sec_a,fin_sec_b,fin_sec_c,fin_end]
            for finger_loc in finger_loc_list:
                locs_list.append(finger_loc)
            if snap_points is False:
                if side_f is "l":
                    if parent_fin_check is False:
                        cmds.setAttr("{}.translateX".format(fin_sec_a),17)
                        cmds.setAttr("{}.translateY".format(fin_sec_a),16)
                    else:
                        cmds.parent(fin_sec_a,"handEnd_{}_loc_{}".format(side_f,parent_fin_num))
                        for axis in "xyz":
                            cmds.setAttr("{}.t{}".format(fin_sec_a,axis),0)
                        cmds.setAttr("{}.tx".format(fin_sec_a,axis),0.5)
                else:
                    if parent_fin_check is False:
                        cmds.setAttr("{}.translateX".format(fin_sec_a),-17)
                        cmds.setAttr("{}.translateY".format(fin_sec_a),16)
                    else:
                        cmds.parent(fin_sec_a,"handEnd_{}_loc_{}".format(side_f,parent_fin_num))
                        for axis in "xyz":
                            cmds.setAttr("{}.t{}".format(fin_sec_a,axis),0)
                        cmds.setAttr("{}.tx".format(fin_sec_a,axis),-0.5)
                        
                cmds.parent(fin_end,fin_sec_c)
                cmds.parent(fin_sec_c,fin_sec_b)
                cmds.parent(fin_sec_b,fin_sec_a)
                
                for axis in "xyz":
                    cmds.setAttr("{}.t{}".format(fin_sec_b,axis),0)
                    cmds.setAttr("{}.t{}".format(fin_sec_c,axis),0)
                    cmds.setAttr("{}.t{}".format(fin_end,axis),0)
                
                if side_f is "l":
                    cmds.setAttr("{}.tx".format(fin_sec_b),0.7)
                    cmds.setAttr("{}.tx".format(fin_sec_c),0.6)
                    cmds.setAttr("{}.tx".format(fin_end),0.5)
                else:
                    cmds.setAttr("{}.tx".format(fin_sec_b),-0.7)
                    cmds.setAttr("{}.tx".format(fin_sec_c),-0.6)
                    cmds.setAttr("{}.tx".format(fin_end),-0.5)
            else:
                cmds.matchTransform(fin_sec_a,"fingerSectionA_{}_point_{}".format(side_f,number_f_l))
                cmds.matchTransform(fin_sec_b,"fingerSectionB_{}_point_{}".format(side_f,number_f_l))
                cmds.matchTransform(fin_sec_c,"fingerSectionC_{}_point_{}".format(side_f,number_f_l))
                cmds.matchTransform(fin_end,"fingerEnd_{}_point_{}".format(side_f,number_f_l))
        def CreateFingerLocsRight():
            side_f = "r"
            parent_fin_check = win.checkBoxFingerHandConexion.isChecked()
            parent_fin_num = win.spinFingerHandConexion.value()
            
            fin_sec_a = cmds.spaceLocator(n="fingerSectionA_{}_loc_{}".format(side_f,number_f_r))[0]
            fin_sec_b = cmds.spaceLocator(n="fingerSectionB_{}_loc_{}".format(side_f,number_f_r))[0]
            fin_sec_c = cmds.spaceLocator(n="fingerSectionC_{}_loc_{}".format(side_f,number_f_r))[0]
            fin_end = cmds.spaceLocator(n="fingerEnd_{}_loc_{}".format(side_f,number_f_r))[0]
            finger_loc_list = [fin_sec_a,fin_sec_b,fin_sec_c,fin_end]
            for finger_loc in finger_loc_list:
                locs_list.append(finger_loc)
            if snap_points is False:
                if side_f is "l":
                    if parent_fin_check is False:
                        cmds.setAttr("{}.translateX".format(fin_sec_a),17)
                        cmds.setAttr("{}.translateY".format(fin_sec_a),16)
                    else:
                        cmds.parent(fin_sec_a,"handEnd_{}_loc_{}".format(side_f,parent_fin_num))
                        for axis in "xyz":
                            cmds.setAttr("{}.t{}".format(fin_sec_a,axis),0)
                        cmds.setAttr("{}.tx".format(fin_sec_a,axis),0.5)
                else:
                    if parent_fin_check is False:
                        cmds.setAttr("{}.translateX".format(fin_sec_a),-17)
                        cmds.setAttr("{}.translateY".format(fin_sec_a),16)
                    else:
                        cmds.parent(fin_sec_a,"handEnd_{}_loc_{}".format(side_f,parent_fin_num))
                        for axis in "xyz":
                            cmds.setAttr("{}.t{}".format(fin_sec_a,axis),0)
                        cmds.setAttr("{}.tx".format(fin_sec_a,axis),-0.5)
                        
                cmds.parent(fin_end,fin_sec_c)
                cmds.parent(fin_sec_c,fin_sec_b)
                cmds.parent(fin_sec_b,fin_sec_a)
                
                for axis in "xyz":
                    cmds.setAttr("{}.t{}".format(fin_sec_b,axis),0)
                    cmds.setAttr("{}.t{}".format(fin_sec_c,axis),0)
                    cmds.setAttr("{}.t{}".format(fin_end,axis),0)
                
                if side_f is "l":
                    cmds.setAttr("{}.tx".format(fin_sec_b),0.7)
                    cmds.setAttr("{}.tx".format(fin_sec_c),0.6)
                    cmds.setAttr("{}.tx".format(fin_end),0.5)
                else:
                    cmds.setAttr("{}.tx".format(fin_sec_b),-0.7)
                    cmds.setAttr("{}.tx".format(fin_sec_c),-0.6)
                    cmds.setAttr("{}.tx".format(fin_end),-0.5)
            else:
                cmds.matchTransform(fin_sec_a,"fingerSectionA_{}_point_{}".format(side_f,number_f_r))
                cmds.matchTransform(fin_sec_b,"fingerSectionB_{}_point_{}".format(side_f,number_f_r))
                cmds.matchTransform(fin_sec_c,"fingerSectionC_{}_point_{}".format(side_f,number_f_r))
                cmds.matchTransform(fin_end,"fingerEnd_{}_point_{}".format(side_f,number_f_r))
                              
        def LocList():
            del locs_list[:]
        def ParentLocs():
            for l in locs_list:
                cmds.parent(l,"{}BodyLocs_c_grp".format(name))
                      
        def LocList():
            del locs_list[:]
        def ParentLocs():
            for l in locs_list:
                cmds.parent(l,"{}BodyLocs_c_grp".format(name))
            
        win.spineLocsButton.clicked.connect(LocList)    
        win.spineLocsButton.clicked.connect(CreateSpineLocs)   
        win.spineLocsButton.clicked.connect(ParentLocs)
        
        win.neckLocsButton.clicked.connect(LocList)
        win.neckLocsButton.clicked.connect(CreateNeckLocs)
        win.neckLocsButton.clicked.connect(ParentLocs)
        
        win.ClavicleLeftLocsButton.clicked.connect(LocList)
        win.ClavicleLeftLocsButton.clicked.connect(CreateClavicleLocsLeft)
        win.ClavicleLeftLocsButton.clicked.connect(ParentLocs)
        
        win.ClavicleRightLocsButton.clicked.connect(LocList)
        win.ClavicleRightLocsButton.clicked.connect(CreateClavicleLocsRight)
        win.ClavicleRightLocsButton.clicked.connect(ParentLocs)           
        
        win.ArmLeftLocsButton.clicked.connect(LocList)
        win.ArmLeftLocsButton.clicked.connect(CreateArmLocsLeft)
        win.ArmLeftLocsButton.clicked.connect(ParentLocs)
        
        win.ArmRightLocsButton.clicked.connect(LocList)
        win.ArmRightLocsButton.clicked.connect(CreateArmLocsRight)
        win.ArmRightLocsButton.clicked.connect(ParentLocs)
        
        win.LegLeftLocsButton.clicked.connect(LocList)
        win.LegLeftLocsButton.clicked.connect(CreateLegLocsLeft)
        win.LegLeftLocsButton.clicked.connect(ParentLocs)
        
        win.LegRightLocsButton.clicked.connect(LocList)
        win.LegRightLocsButton.clicked.connect(CreateLegLocsRight)
        win.LegRightLocsButton.clicked.connect(ParentLocs)
        
        win.FingerLeftLocsButton.clicked.connect(LocList)
        win.FingerLeftLocsButton.clicked.connect(CreateFingerLocsLeft)
        win.FingerLeftLocsButton.clicked.connect(ParentLocs)
        
        win.FingerRightLocsButton.clicked.connect(LocList)
        win.FingerRightLocsButton.clicked.connect(CreateFingerLocsRight)
        win.FingerRightLocsButton.clicked.connect(ParentLocs)              
        #Seleccionador de locators
        def SelectSpineLocs():
            spin_spine_number = win.spinSpineNumber.value()
            cmds.select(cl=True)
            cmds.select("spineDw_c_loc_{}".format(spin_spine_number),"spineUp_c_loc_{}".format(spin_spine_number))
        
        win.selectLocsSpine.clicked.connect(SelectSpineLocs)
        
        def SelectNeckLocs():
            spin_neck_number = win.spinNeckNumber.value()
            cmds.select(cl=True)
            cmds.select("neckDw_c_loc_{}".format(spin_neck_number),"neckUp_c_loc_{}".format(spin_neck_number))
        
        win.selectLocsNeck.clicked.connect(SelectNeckLocs)
        
        def SelectClavicleLocs():
            spin_clavicle_number = win.spinClavicleNumber.value()
            box_side = win.sideClavicleSelectBox.currentText()
            cmds.select(cl=True)
            cmds.select("clavicle_{}_loc_{}".format(box_side,spin_clavicle_number),"clavicleEnd_{}_loc_{}".format(box_side,spin_clavicle_number))   
        
        win.selectLocsClavicle.clicked.connect(SelectClavicleLocs)
        
        def SelectArmLocs():
            spin_arm_number = win.spinArmNumber.value()
            box_side = win.sideArmSelectBox.currentText()
            cmds.select(cl=True)
            cmds.select("shoulder_{}_loc_{}".format(box_side,spin_arm_number),
                        "elbow_{}_loc_{}".format(box_side,spin_arm_number),
                        "hand_{}_loc_{}".format(box_side,spin_arm_number),
                        "handEnd_{}_loc_{}".format(box_side,spin_arm_number))   
        
        win.selectLocsArm.clicked.connect(SelectArmLocs)
        
        def SelectLegLocs():
            spin_leg_number = win.spinLegNumber.value()
            box_side = win.sideLegSelectBox.currentText()
            cmds.select(cl=True)
            cmds.select("hip_{}_loc_{}".format(box_side,spin_leg_number),
                        "knee_{}_loc_{}".format(box_side,spin_leg_number),
                        "foot_{}_loc_{}".format(box_side,spin_leg_number),
                        "ball_{}_loc_{}".format(box_side,spin_leg_number),
                        "toe_{}_loc_{}".format(box_side,spin_leg_number),
                        "heelPos_{}_loc_{}".format(box_side,spin_leg_number),
                        "bankExtPos_{}_loc_{}".format(box_side,spin_leg_number),
                        "bankIntPos_{}_loc_{}".format(box_side,spin_leg_number))   
        
        win.selectLocsLeg.clicked.connect(SelectLegLocs)
       
        def SelectFingerLocs():
            spin_finger_number = win.spinFingerNumber.value()
            box_side = win.sideFingerSelectBox.currentText()
            cmds.select(cl=True)
            cmds.select("fingerSectionA_{}_loc_{}".format(box_side,spin_finger_number),
                        "fingerSectionB_{}_loc_{}".format(box_side,spin_finger_number),
                        "fingerSectionC_{}_loc_{}".format(box_side,spin_finger_number),
                        "fingerEnd_{}_loc_{}".format(box_side,spin_finger_number))
        win.selectLocsFinger.clicked.connect(SelectFingerLocs)
        # Create Snaps
        
        def snap(match_list):
            for each in match_list:
                source= each[1]
                dest= each[0]
                dupli = cmds.duplicate(dest, po=1, n=str(dest).replace(dest.split("_")[2],"snap"))
                cmds.parent(dupli,source)
                
        def createArmSnap(number_snap_arm,side):
            match_list = [["shoulderFK_{}_ctr_{}".format(side,number_snap_arm), "shoulder_{}_jnt_{}".format(side,number_snap_arm)],["elbowFK_{}_ctr_{}".format(side,number_snap_arm), "elbow_{}_jnt_{}".format(side,number_snap_arm)],["handFK_{}_ctr_{}".format(side,number_snap_arm), "hand_{}_skn_{}".format(side,number_snap_arm)]]
            snap(match_list)
            matchik_list = [["handIK_{}_ctr_{}".format(side,number_snap_arm),"hand_{}_skn_{}".format(side,number_snap_arm)]]
            snap(matchik_list)
                
        def createLegSnap(number_snap_leg,side):
            match_list = [["hipFK_{}_ctr_{}".format(side,number_snap_leg), "hip_{}_jnt_{}".format(side,number_snap_leg)],["kneeFK_{}_ctr_{}".format(side,number_snap_leg), "knee_{}_jnt_{}".format(side,number_snap_leg)],["footFK_{}_ctr_{}".format(side,number_snap_leg), "foot_{}_skn_{}".format(side,number_snap_leg)]]
            snap(match_list)
            matchik_list = [["footIK_{}_ctr_{}".format(side,number_snap_leg),"foot_{}_skn_{}".format(side,number_snap_leg)]]
            snap(matchik_list)
                
        Start()
        
        # 3.1.1 Creacion de la cadena principal de la espina
        def BuildSpine():
            number_spine_joints = win.spinBoxSpineNumberJoints.value()
            spine_dw = "spineDw_c_loc_{}".format(number_s)
            spine_up = "spineUp_c_loc_{}".format(number_s)
            spine_joints = JointChain(spine_dw,spine_up,"spine",number_spine_joints)
            new_spine_joints = []
            for joints in spine_joints:
                new = cmds.rename(joints,"{}_c_skn_{}".format(joints,number_s))
                new_spine_joints.append(new)
            spine_end_joint = cmds.rename(new_spine_joints[-1],"spineEnd1_c_jnt_{}".format(number_s))
            spine_end_two_joint = cmds.duplicate(spine_end_joint,n="spineEnd2_c_jnt_{}".format(number_s))[0]
            cmds.parent(spine_end_two_joint,spine_end_joint)
            cmds.setAttr("{}.translateX".format(spine_end_two_joint),0.01)
            
            # 3.1.2 Creacion del hueso de la pelvis
            spine_first_joint = new_spine_joints[0]
            pelvis_joint = cmds.duplicate(spine_first_joint, n="pelvis_c_skn_{}".format(number_s),po=True)[0]
            pelvis_pos = cmds.getAttr("{}.translateY".format(pelvis_joint))
            cmds.setAttr("{}.translateY".format(pelvis_joint),pelvis_pos-0.01)
            
            #3.1.3 Creacion del hueso chest
            chest_joint = cmds.duplicate(pelvis_joint,n="chest_c_skn_{}".format(number_s))[0]
            spine_end_pos = cmds.xform(spine_end_joint,q=True,t=True,ws=True)
            cmds.xform(chest_joint,t=spine_end_pos,ws=True)
            chest_end_joint = cmds.duplicate(chest_joint,n="chestEnd_c_jnt_{}".format(number_s))[0]
            cmds.parent(chest_end_joint,chest_joint)
            cmds.setAttr("{}.translateX".format(chest_end_joint),1)
            
            spine_joints_list = [spine_first_joint,pelvis_joint,chest_joint]
            for j in spine_joints_list:
                cmds.parent(j,char_skeleton)        
            
            # Creacion o duplicacion de controles          
            # 3.2.1 Creacion del control root
            root_ctr = cmds.duplicate("root_c_ctr_0",n="root_c_ctr_{}".format(number_s))[0]
            root_offset = CreateOffset(root_ctr,number_s)
            pelvis_translate_pos = cmds.xform(pelvis_joint,q=True,t=True,ws=True)
                # Situar en hueso de pierna cuando este creado
            cmds.xform(root_offset,t=pelvis_translate_pos,ws=True)
            cmds.xform(root_offset,ro=(0,0,0),ws=True)
            cmds.parent(root_offset,control_center)
            
            # 3.2.2 Creacion del control de la pelvis
            pelvis_ctr = cmds.duplicate("pelvis_c_ctr_0",n="pelvis_c_ctr_{}".format(number_s))[0]
            pelvis_offset = CreateOffset(pelvis_ctr,number_s)
            cmds.xform(pelvis_offset,t=pelvis_translate_pos,ws=True)
            cmds.xform(pelvis_offset,ro=(0,0,0),ws=True)
            cmds.parentConstraint(pelvis_ctr,pelvis_joint,mo=True,n="pelvisParent_c_cns_{}".format(number_s))
            cmds.parent(pelvis_offset,root_ctr)
            
            # 3.2.3 Creacion del control Chest
            chest_ctr = cmds.duplicate("chest_c_ctr_0",n="chest_c_ctr_{}".format(number_s),rc=True)[0]
            chest_offset = CreateOffset(chest_ctr,number_s)
            chest_joint_pos = cmds.xform(chest_joint,q=True,t=True,ws=True)
            cmds.xform(chest_offset,t=chest_joint_pos,ws=True)
            cmds.xform(chest_offset,ro=(0,0,0),ws=True)  
            cmds.parentConstraint(chest_ctr,chest_joint,mo=True,n="chestParent_c_cns_{}".format(number_s))
            cmds.parent(chest_offset,root_ctr)
            
            # 3.2.4 Creacion de controles FK
            spineFK1 = cmds.duplicate("spineFK1_c_ctr_0",n="spineFK1_c_ctr_{}".format(number_s),rc=True)[0]
            spineFK2 = cmds.duplicate("spineFK2_c_ctr_0",n="spineFK2_c_ctr_{}".format(number_s),rc=True)[0]
            spineFK3 = cmds.duplicate("spineFK3_c_ctr_0",n="spineFK3_c_ctr_{}".format(number_s))[0]
            FK_ctr_list = [spineFK1,spineFK2,spineFK3] 
            FK1_pos = cmds.xform(spine_first_joint,q=True,t=True,ws=True)
            cmds.xform(spineFK1,t=FK1_pos,ws=True)
            cmds.xform(spineFK3,t= chest_joint_pos,ws=True)
            delete_cons = cmds.pointConstraint(spineFK3,spineFK1,spineFK2,mo=False)
            cmds.delete(delete_cons)
            for x in FK_ctr_list:
                cmds.xform(x,ro=(0,0,0),ws=True)
            spineFK1_ofsset = CreateOffset(spineFK1,number_s) 
            spineFK2_ofsset = CreateOffset(spineFK2,number_s) 
            spineFK3_ofsset = CreateOffset(spineFK3,number_s)
            cmds.parent(spineFK3_ofsset,spineFK2)
            cmds.parent(spineFK2_ofsset,spineFK1)
            cmds.parent(spineFK1_ofsset,root_ctr)
            cmds.parentConstraint(spineFK3,chest_offset,mo=True,n="spineFKParent_c_cns_{}".format(number_s))
            
            # 3.2.5 Creacion de controles FK Invertidos
            spineFK1_inv = cmds.duplicate("spineFK1Inv_c_ctr_0",n="spineFK1Inv_c_ctr_{}".format(number_s))[0]
            spineFK2_inv = cmds.duplicate("spineFK2Inv_c_ctr_0",n="spineFK2Inv_c_ctr_{}".format(number_s),rc=True)[0]
            spineFK3_inv = cmds.duplicate("spineFK3Inv_c_ctr_0",n="spineFK3Inv_c_ctr_{}".format(number_s),rc=True)[0]
            FK_inverse_ctr_list = [spineFK1_inv,spineFK2_inv,spineFK3_inv]
            cmds.xform(spineFK1_inv,t=FK1_pos,ws=True)
            cmds.xform(spineFK3_inv,t=chest_joint_pos,ws=True)
            FK2_pos = cmds.xform(spineFK2_ofsset,q=True,t=True,ws=True)
            cmds.xform(spineFK2_inv,t=FK2_pos,ws=True)
            for x in FK_inverse_ctr_list:
                cmds.xform(x,ro=(0,0,0),ws=True)
            spineFK1_inv_offset = CreateOffset(spineFK1_inv,number_s)
            spineFK2_inv_offset = CreateOffset(spineFK2_inv,number_s)
            spineFK3_inv_offset = CreateOffset(spineFK3_inv,number_s)
            cmds.parent(spineFK1_inv_offset,spineFK2_inv)
            cmds.parent(spineFK2_inv_offset,spineFK3_inv)
            cmds.parent(spineFK3_inv_offset,root_ctr)
            cmds.parentConstraint(spineFK1_inv,pelvis_offset,mo=True,n="spineFKParent_c_cns_{}".format(number_s))
                
            # 3.3.1 Creacion del IkSpline
            spine_ik_list = cmds.ikHandle(sj=spine_first_joint,
                                          ee=spine_end_two_joint,
                                          sol="ikSplineSolver",
                                          roc=True,
                                          ccv=True,
                                          scv=True,
                                          snc=False,
                                          rtm=False,
                                          ns=1,
                                          tws="linear",
                                          pcv=False,
                                          n="spineIkHandle_c_ik_{}".format(number_s))
            spine_ikhandle = spine_ik_list[0]
            spine_ikcurve = spine_ik_list[2]
            spine_ikcurve = cmds.rename(spine_ikcurve,"spineIkCurve_c_crv_{}".format(number_s))
            cmds.parent(spine_ikhandle,spine_rig)
            cmds.parent(spine_ikcurve,spine_rig)
            # 3.3.2 Configuracion Advanced Twist Control
            cmds.setAttr("{}.dTwistControlEnable".format(spine_ikhandle),1)
            cmds.setAttr("{}.dWorldUpType".format(spine_ikhandle),4)
            cmds.setAttr("{}.dForwardAxis".format(spine_ikhandle),0)
            cmds.setAttr("{}.dWorldUpAxis".format(spine_ikhandle),3)
            cmds.setAttr("{}.dWorldUpVectorX".format(spine_ikhandle),0)
            cmds.setAttr("{}.dWorldUpVectorY".format(spine_ikhandle),0)
            cmds.setAttr("{}.dWorldUpVectorZ".format(spine_ikhandle),1)
            cmds.setAttr("{}.dWorldUpVectorEndX".format(spine_ikhandle),0)
            cmds.setAttr("{}.dWorldUpVectorEndY".format(spine_ikhandle),0)
            cmds.setAttr("{}.dWorldUpVectorEndZ".format(spine_ikhandle),1)
            cmds.connectAttr("{}.worldMatrix".format(pelvis_ctr),"{}.dWorldUpMatrix".format(spine_ikhandle),f=1)
            cmds.connectAttr("{}.worldMatrix".format(chest_ctr),"{}.dWorldUpMatrixEnd".format(spine_ikhandle),f=1)
            # 3.3.3 Creacion de los clusters
            chest_cluster = cmds.cluster("{}.cv[2:3]".format(spine_ikcurve),n="spineChestCluster_c_cl_{}".format(number_s))[1]
            cmds.parent(chest_cluster,chest_ctr)
            pelvis_cluster = cmds.cluster("{}.cv[0:1]".format(spine_ikcurve),n="spinePelvisCluster_c_cl_{}".format(number_s))[1]
            cmds.parent(pelvis_cluster,pelvis_ctr)
            
            # 3.4.1 Configuracion autostretch eje X
            spine_curve_info = cmds.createNode("curveInfo",n="spineCurveInfo_c_ci_{}".format(number_s))
            cmds.connectAttr("{}.worldSpace[0]".format(spine_ikcurve),"{}.inputCurve".format(spine_curve_info))
            
            spine_stretch_div = cmds.createNode("multiplyDivide",n="spineStretch_c_div_{}".format(number_s))
            cmds.setAttr("{}.operation".format(spine_stretch_div),2)
            cmds.connectAttr("{}.arcLength".format(spine_curve_info),"{}.input1X".format(spine_stretch_div))
            spine_curve_length = cmds.getAttr("{}.arcLength".format(spine_curve_info))
            cmds.setAttr("{}.input2X".format(spine_stretch_div),spine_curve_length)
            
            spine_global_div = cmds.createNode("multiplyDivide",n="spineGlobal_c_div_{}".format(number_s))
            cmds.setAttr("{}.operation".format(spine_global_div),2)
            cmds.connectAttr("{}.outputX".format(spine_stretch_div),"{}.input1X".format(spine_global_div))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.input2X".format(spine_global_div))
            
            # 3.4.2 Configuracion de los ejes X y Z (a mi manera)y conexion final en todos los ejes de los huesos
            spine_stretch_yz_div = cmds.createNode("multiplyDivide",n="spineStretchYZ_c_div_{}".format(number_s))
            cmds.setAttr("{}.operation".format(spine_stretch_yz_div),2)
            cmds.connectAttr("{}.outputX".format(spine_global_div),"{}.input1X".format(spine_stretch_yz_div))
            cmds.setAttr("{}.input2X".format(spine_stretch_yz_div),6)
            
            spine_stretch_yz_clamp = cmds.createNode("clamp",n="spineStretchYZ_c_clamp_{}".format(number_s))
            cmds.setAttr(".minR".format(spine_stretch_yz_clamp),0)
            cmds.setAttr(".maxR".format(spine_stretch_yz_clamp),0.9)
            cmds.connectAttr("{}.outputX".format(spine_stretch_yz_div),"{}.input.inputR".format(spine_stretch_yz_clamp))
            
            spine_stretch_yz_sub = cmds.createNode("plusMinusAverage",n="spineStretchYZ_c_sub_{}".format(number_s))
            difference_division_stretch = cmds.getAttr("{}.output.outputR".format(spine_stretch_yz_clamp))
            cmds.setAttr("{}.operation".format(spine_stretch_yz_sub),2)
            cmds.setAttr("{}.input1D[0]".format(spine_stretch_yz_sub),difference_division_stretch+1)
            cmds.connectAttr("{}.output.outputR".format(spine_stretch_yz_clamp),"{}.input1D[1]".format(spine_stretch_yz_sub))
            
            spine_stretch_yz_blend = cmds.createNode("blendColors",n="spineStretchYZ_c_blend_{}".format(number_s))
            cmds.connectAttr("{}.output1D".format(spine_stretch_yz_sub),"{}.color1R".format(spine_stretch_yz_blend))
            cmds.setAttr("{}.color2R".format(spine_stretch_yz_blend),1)
            
            spine_joint_list_stretch = new_spine_joints[0:number_spine_joints-1]+[spine_end_joint]
            for joints in spine_joint_list_stretch:
                cmds.connectAttr("{}.outputX".format(spine_global_div),"{}.scaleX".format(joints))
                cmds.connectAttr("{}.output.outputR".format(spine_stretch_yz_blend),"{}.scaleY".format(joints))
                cmds.connectAttr("{}.output.outputR".format(spine_stretch_yz_blend),"{}.scaleZ".format(joints))
            
            # 3.4.3 Configuracion de atributos info    
            AttrSeparator(pelvis_ctr)
            AttrSeparator(chest_ctr)
            cmds.addAttr(chest_ctr,ln= "autoSquash",at= "double",min= 0,max=1,dv=1,k=True)
            cmds.connectAttr("{}.autoSquash" .format(chest_ctr),"{}.blender".format(spine_stretch_yz_blend))
            cmds.addAttr(pelvis_ctr,ln= "spineStretch", at= "double")
            cmds.setAttr ("{}.spineStretch".format(pelvis_ctr),channelBox= True)
            cmds.addAttr(chest_ctr,ln= "spineStretch", at= "double")
            cmds.setAttr ("{}.spineStretch".format(chest_ctr),channelBox= True)
            cmds.connectAttr("{}.outputX".format(spine_global_div),"{}.spineStretch".format(chest_ctr))
            cmds.connectAttr("{}.outputX".format(spine_global_div),"{}.spineStretch".format(pelvis_ctr))
            
            # 3.5.1 Creacion del control Middlespine
            middlespine_ctr = cmds.duplicate("middleSpineIK_c_ctr_0",n="middleSpineIK_c_ctr_{}".format(number_s))[0]
            del_cons = cmds.pointConstraint(chest_ctr,pelvis_ctr,middlespine_ctr,mo=False)
            cmds.delete(del_cons)
            cmds.xform(middlespine_ctr,ro=(0,0,0),ws=True)
            middlespine_offset = CreateOffset(middlespine_ctr,number_s)
            middlespine_closestjoint_label = (len(spine_joint_list_stretch)/2)-1
            middlespine_closestjoint = spine_joint_list_stretch[middlespine_closestjoint_label]
            cmds.pointConstraint(middlespine_closestjoint,middlespine_offset,mo=True)
            cmds.parent(middlespine_offset,root_ctr)
           
            # 3.5.2 Creacion de la curva Bend y de los clusters
            spine_ik_curve_bend = cmds.duplicate(spine_ikcurve,n="spineIkCurveBend_c_crv_{}".format(number_s))[0]
            spine_ik_curve_bend_orig = cmds.listRelatives(spine_ik_curve_bend)[1]
            cmds.delete(spine_ik_curve_bend_orig)
            spine_top_bend_cluster = cmds.cluster("{}.cv[2]".format(spine_ik_curve_bend),n="spineTopBendCluster_c_cl_{}".format(number_s))[1]
            spine_low_bend_cluster = cmds.cluster("{}.cv[1]".format(spine_ik_curve_bend),n="spineLowBendCluster_c_cl_{}".format(number_s))[1]
            # 3.5.3 Creacion del grupo Bend
            spine_bend_grp = cmds.duplicate(middlespine_offset,po=True,n="spineBend_c_grp_{}".format(number_s))[0]
            cmds.parent(spine_top_bend_cluster,spine_bend_grp)
            cmds.parent(spine_low_bend_cluster,spine_bend_grp)
            spine_bend_grp_offset = CreateOffset(spine_bend_grp,number_s)
            cmds.parent(spine_bend_grp_offset,spine_rig)
            for axis in "XYZ":
                cmds.connectAttr("{}.translate{}".format(middlespine_ctr,axis),"{}.translate{}".format(spine_bend_grp,axis))
                cmds.connectAttr("{}.rotate{}".format(middlespine_ctr,axis),"{}.rotate{}".format(spine_bend_grp,axis))
            
            # 3.5.4 Creacion del blendShape
            spine_ik_curve_bs = cmds.blendShape(spine_ik_curve_bend,spine_ikcurve,origin="local",ib=False,tc=True,foc=True,n="spineIkCurve_c_bs_{}".format(number_s))[0]
            cmds.setAttr("{}.spineIkCurveBend_c_crv_{}".format(spine_ik_curve_bs,number_s),1)   
            
            #Cerrar rig
            Hide(spine_rig)
            Hide(pelvis_cluster)
            Hide(chest_cluster)
            LockScaleVis(spineFK1)
            LockScaleVis(spineFK2)
            LockScaleVis(spineFK3)
            LockScaleVis(spineFK1_inv)
            LockScaleVis(spineFK2_inv)
            LockScaleVis(spineFK3_inv)
            LockScaleVis(chest_ctr)
            LockScaleVis(pelvis_ctr)
            LockScaleVis(middlespine_ctr)
            LockScaleVis(root_ctr)
                
        win.spineButton.clicked.connect(BuildSpine)
        
        
        
        def BuildNeck():
            number_neck_joints = win.spinBoxNeckNumberJoints.value()
            neck_dw = "neckDw_c_loc_{}".format(number_n)
            neck_up = "neckUp_c_loc_{}".format(number_n)
            # 4.1.1 Creacion de la cadena principal del cuello 
            neck_joints = JointChain(neck_dw,neck_up,"neck",number_neck_joints)
            new_neck_joints = []
            for joints in neck_joints:
                new = cmds.rename(joints,"{}_c_skn_{}".format(joints,number_n))
                new_neck_joints.append(new)
            last_neck_joint = cmds.rename( new_neck_joints[-1],"neckEnd1_c_jnt_{}".format(number_n))
            new_neck_joints = new_neck_joints[0:number_neck_joints-1]+[last_neck_joint]
            last2_neck_joint = cmds.duplicate(last_neck_joint,n="neckEnd2_c_jnt_{}".format(number_n))[0]
            x_pos_last_neck_jnt = cmds.getAttr("{}.translateX".format(last2_neck_joint))
            cmds.setAttr("{}.translateX".format(last2_neck_joint),x_pos_last_neck_jnt+0.01)
            cmds.parent(last2_neck_joint,last_neck_joint)
            
            # 4.1.2 Creacion del hueso de la cabeza
            head_jnt = cmds.duplicate(last2_neck_joint, n="head_c_skn_{}".format(number_n))[0]
            head_end_jnt = cmds.duplicate(head_jnt, n="headEnd_c_jnt_{}".format(number_n))[0]
            cmds.parent(head_end_jnt,head_jnt)
            cmds.setAttr("{}.translateX".format(head_end_jnt),1)
            head_jnt_offset = CreateOffset(head_jnt,number_n)
            first_neck_joint = new_neck_joints[0] 
            cmds.parent(first_neck_joint,char_skeleton)
            cmds.parent(head_jnt_offset,char_skeleton)
            # 4.2.1 Creacion del control de cuello
            neck_ctr = cmds.duplicate("neck_c_ctr_0",n="neck_c_ctr_{}".format(number_n))[0]
            first_neck_joint_pos = cmds.xform(first_neck_joint,q=True,t=True,ws=True)
            cmds.xform(neck_ctr,t=first_neck_joint_pos,ws=True)
            cmds.parent(neck_ctr,first_neck_joint)
            cmds.setAttr("{}.rotateX".format(first_neck_joint),0)
            neck_offset = CreateOffset(neck_ctr,number_n)
            cmds.parent(neck_offset,control_center)
            
            # 4.2.2 Creacion del control de cabeza 
            head_ctr = cmds.duplicate("head_c_ctr_0",n="head_c_ctr_{}".format(number_n))[0]
            head_joint_pos  = cmds.xform(head_jnt,q=True,t=True,ws=True)
            cmds.xform(head_ctr,t=head_joint_pos,ws=True)
            cmds.xform(head_ctr,ro=(0,0,0),ws=True)
            head_offset = CreateOffset(head_ctr,number_n)
            cmds.parentConstraint(head_ctr,head_jnt,mo=True,n="headParent_c_cns_{}".format(number_n))
            cmds.parent(head_offset,control_center)
            
            # 4.2.3 Creacion del control middleNeck
            middleneck_ctr = cmds.duplicate("middleNeck_c_ctr_0",n="middleNeck_c_ctr_{}".format(number_n))[0]
            middleneck_joint = new_neck_joints[(number_neck_joints-1)/2]
            middleneck_joint_pos = cmds.xform(middleneck_joint,q=True,t=True,ws=True)
            cmds.xform(middleneck_ctr,t=middleneck_joint_pos,ws=True)
            middleneck_offset = CreateOffset(middleneck_ctr,number_n)
            cmds.parent(middleneck_offset,neck_ctr)
            for axis in "XYZ":
                cmds.setAttr("{}.rotate{}".format(middleneck_offset,axis),0)
                
            #4.3.1 Creacion del ikSpline
            neck_ik_list = cmds.ikHandle(sj=first_neck_joint,
                                          ee=last2_neck_joint,
                                          sol="ikSplineSolver",
                                          roc=True,
                                          ccv=True,
                                          scv=True,
                                          snc=False,
                                          rtm=False,
                                          ns=1,
                                          tws="linear",
                                          pcv=False,
                                          n="neckIkHandle_c_ik_{}".format(number_n))
            neck_ikhandle = neck_ik_list[0]
            neck_ikcurve = neck_ik_list[2]
            neck_ikcurve = cmds.rename(neck_ikcurve,"neckIkCurve_c_crv_{}".format(number_n))
            cmds.parent(neck_ikhandle,neck_rig)
            cmds.parent(neck_ikcurve,neck_rig)
            
            #4.3.2 Configuracion del advanced twist control del ikSpline
            cmds.setAttr("{}.dTwistControlEnable".format(neck_ikhandle),1)
            cmds.setAttr("{}.dWorldUpType".format(neck_ikhandle),4)
            cmds.setAttr("{}.dForwardAxis".format(neck_ikhandle),0)
            cmds.setAttr("{}.dWorldUpAxis".format(neck_ikhandle),3)
            cmds.setAttr("{}.dWorldUpVectorX".format(neck_ikhandle),0)
            cmds.setAttr("{}.dWorldUpVectorY".format(neck_ikhandle),0)
            cmds.setAttr("{}.dWorldUpVectorZ".format(neck_ikhandle),1)
            cmds.setAttr("{}.dWorldUpVectorEndX".format(neck_ikhandle),0)
            cmds.setAttr("{}.dWorldUpVectorEndY".format(neck_ikhandle),0)
            cmds.setAttr("{}.dWorldUpVectorEndZ".format(neck_ikhandle),1)
            cmds.connectAttr("{}.worldMatrix".format(neck_ctr),"{}.dWorldUpMatrix".format(neck_ikhandle),f=1)
            cmds.connectAttr("{}.worldMatrix".format(head_ctr),"{}.dWorldUpMatrixEnd".format(neck_ikhandle),f=1)
        
            #4.3.3 Creaccion de los clusters
            low_neck_cluster = cmds.cluster("{}.cv[0]".format(neck_ikcurve),n="neckLowCluster_c_cl_{}".format(number_n))[1]    
            cmds.parent(low_neck_cluster,neck_ctr)
            middle_neck_cluster = cmds.cluster("{}.cv[1:2]".format(neck_ikcurve),n="neckMiddleCluster_c_cl_{}".format(number_n))[1]    
            cmds.parent(middle_neck_cluster,middleneck_ctr)
            top_neck_cluster = cmds.cluster("{}.cv[3]".format(neck_ikcurve),n="neckTopCluster_c_cl_{}".format(number_n))[1]    
            cmds.parent(top_neck_cluster,head_ctr)    
            
            #4.4.1 Configuracion del autostretch: eje X 
            neck_curve_info = cmds.createNode("curveInfo",n="neckCurveInfo_c_ci_{}".format(number_n))
            cmds.connectAttr("{}.worldSpace[0]".format(neck_ikcurve),"{}.inputCurve".format(neck_curve_info))
            
            neck_stretch_div = cmds.createNode("multiplyDivide",n="neckStretch_c_div_{}".format(number_n))
            cmds.setAttr("{}.operation".format(neck_stretch_div),2)
            cmds.connectAttr("{}.arcLength".format(neck_curve_info),"{}.input1X".format(neck_stretch_div))
            neck_curve_length = cmds.getAttr("{}.arcLength".format(neck_curve_info))
            cmds.setAttr("{}.input2X".format(neck_stretch_div),neck_curve_length)
            
            neck_global_div = cmds.createNode("multiplyDivide",n="neckGlobal_c_div_{}".format(number_n))
            cmds.setAttr("{}.operation".format(neck_global_div),2)
            cmds.connectAttr("{}.outputX".format(neck_stretch_div),"{}.input1X".format(neck_global_div))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.input2X".format(neck_global_div))
            
            for neck_j in new_neck_joints:
                cmds.connectAttr("{}.outputX".format(neck_global_div),"{}.scaleX".format(neck_j))
            
            #4.4.2 Configuracion de lo atributos info
            AttrSeparator(neck_ctr)
            AttrSeparator(head_ctr)
            cmds.addAttr(neck_ctr,ln= "neckStretch", at= "double")
            cmds.setAttr ("{}.neckStretch".format(neck_ctr),channelBox= True)
            cmds.addAttr(head_ctr,ln= "neckStretch", at= "double")
            cmds.setAttr ("{}.neckStretch".format(head_ctr),channelBox= True)
        
            cmds.connectAttr("{}.outputX".format(neck_global_div),"{}.neckStretch".format(neck_ctr))
            cmds.connectAttr("{}.outputX".format(neck_global_div),"{}.neckStretch".format(head_ctr))
        
            #4.5.1 Configuracion de spaces en el control neck
            spine_conexion_check = win.checkBoxNeckSpineConexion.isChecked()
            spine_conexion = win.spinSpineConexion.value()
            if spine_conexion_check is True:
                pcon_neck = cmds.duplicate(neck_offset,n="pconNeck_c_pcon_{}".format(number_n),po=True)[0]
                pcon_cons = cmds.pointConstraint(pcon_neck,neck_offset,mo=False,n="middleSpineClosestPoint_c_cns_{}".format(number_n))
                cmds.parent(pcon_neck,"chest_c_ctr_{}".format(spine_conexion))
                cmds.addAttr(neck_ctr,ln= "__", at="enum",en="spaces")
                cmds.setAttr ("{}.__".format(neck_ctr),channelBox= True)
                cmds.addAttr(neck_ctr,ln= "chestSpace",at= "double",min= 0,max=1,dv=1,k=True)
                
                world_space_neck = cmds.duplicate(neck_offset,n="neckWorldSpace_c_grp_{}".format(number_n),po=True)[0]
                chest_space_neck = cmds.duplicate(neck_offset,n="neckChestSpace_c_grp_{}".format(number_n),po=True)[0]
                
                neck_spaces_cns = cmds.orientConstraint(world_space_neck,chest_space_neck,neck_offset,mo=False,n="neckSpacesPoint_c_cns_{}".format(number_n))[0]
                cmds.parent(chest_space_neck,"chest_c_ctr_{}".format(spine_conexion))
                
                cmds.connectAttr("{}.chestSpace".format(neck_ctr),"{}.{}W1".format(neck_spaces_cns,chest_space_neck))
                dyn_parent_rev_neck = cmds.createNode("reverse",n="neckDynParent_c_rev_{}".format(number_n))
                cmds.connectAttr("{}.chestSpace".format(neck_ctr),"{}.inputX".format(dyn_parent_rev_neck))
                cmds.connectAttr("{}.outputX".format(dyn_parent_rev_neck),"{}.{}W0".format(neck_spaces_cns,world_space_neck))            
                #4.5.2 Configuracion de spaces en control head
                cmds.addAttr(head_ctr,ln= "followNeck",at= "double",min= 0,max=1,dv=1,k=True)
                
                head_world_space = cmds.duplicate(head_offset,n="headWorldSpace_c_grp_{}".format(number_n),po=True)[0]
                head_neck_space = cmds.duplicate(head_offset,n="headNeckSpace_c_grp_{}".format(number_n),po=True)[0]
                head_follow_pcon = cmds.pointConstraint(head_world_space,head_neck_space,head_offset,mo=False,n="headFollowNeckPoint_c_cns_{}".format(number_n))[0]
                cmds.parent(head_neck_space,neck_ctr)
                cmds.connectAttr("{}.followNeck".format(head_ctr),"{}.{}W1".format(head_follow_pcon,head_neck_space))
                head_dyn_parent_rev = cmds.createNode("reverse",n="headDynParent_c_rev_{}".format(number_n))
                cmds.connectAttr("{}.followNeck".format(head_ctr),"{}.inputX".format(head_dyn_parent_rev))
                cmds.connectAttr("{}.outputX".format(head_dyn_parent_rev),"{}.{}W0".format(head_follow_pcon,head_world_space))
                
                cmds.addAttr(head_ctr,ln= "__", at="enum",en="spaces")
                cmds.setAttr ("{}.__".format(head_ctr),channelBox= True)
                cmds.addAttr(head_ctr,ln= "neckSpace",at= "double",min= 0,max=1,dv=1,k=True)
            
                head_spaces_ocon = cmds.orientConstraint(head_world_space,head_neck_space,head_offset,mo=False,n="headSpacesOrient_c_cns_{}".format(number_n))[0]
                cmds.connectAttr("{}.neckSpace".format(head_ctr),"{}.{}W1".format(head_spaces_ocon,head_neck_space))
                cmds.connectAttr("{}.neckSpace".format(head_ctr),"{}.inputY".format(head_dyn_parent_rev))
                cmds.connectAttr("{}.outputY".format(head_dyn_parent_rev),"{}.{}W0".format(head_spaces_ocon,head_world_space))
            #Cerrar rig
            Hide(neck_rig)
            Hide(top_neck_cluster)
            Hide(low_neck_cluster)
            Hide(middle_neck_cluster)
            LockScaleVis(neck_ctr)
            LockScaleVis(head_ctr)
            LockScaleVis(middleneck_ctr)
                
        win.neckButton.clicked.connect(BuildNeck)
        
        def BuildLeftClavicle():
            clavicle = "clavicle_l_loc_{}".format(number_c_l)
            clavicle_end = "clavicleEnd_l_loc_{}".format(number_c_l)
            # 5.2.2 Creacion de la cadena de huesos clavicula
            del_cons = cmds.aimConstraint(clavicle_end,clavicle,offset=(0,0,0),weight=1,aimVector=(1,0,0),upVector=(0,1,0),worldUpType="scene")[0]
            cmds.delete(del_cons)
            del_cons = cmds.aimConstraint(clavicle,clavicle_end,offset=(0,0,0),weight=1,aimVector=(-1,0,0),upVector=(0,1,0),worldUpType="scene")[0]
            cmds.delete(del_cons)
            side_c = clavicle.split("_")[1]
            cmds.select(cl=1)
            clavicle_jnt = cmds.joint(n="clavicle_{}_skn_{}".format(side_c,number_c_l))
            clavicle_matrix = cmds.xform(clavicle,q=True,matrix=True,ws=True)
            cmds.xform(clavicle_jnt,matrix=clavicle_matrix,ws=True)
            clavicle_end_jnt = cmds.joint(n="clavicleEnd_{}_jnt_{}".format(side_c,number_c_l))
            clavicle_end_matrix = cmds.xform(clavicle_end,q=True,matrix=True,ws=True)
            cmds.xform(clavicle_end_jnt,matrix=clavicle_end_matrix,ws=True)
            spine_clavicle_conexion = win.spinClavicleConexion.value()
            spine_clavicle_conexion_check = win.checkBoxClavicleSpineConexion.isChecked()
            if spine_clavicle_conexion_check is True:
                cmds.parent(clavicle_jnt,"chest_c_skn_{}".format(spine_clavicle_conexion))
            else:
                cmds.parent(clavicle_jnt,char_skeleton)
            
            #5.3.1 Creacion del control clavicle
            clavicle_ctr = cmds.duplicate("clavicle_{}_ctr_0".format(side_c),n="clavicle_{}_ctr_{}".format(side_c,number_c_l))[0]
            clavicle_offset = CreateOffset(clavicle_ctr,number_c_l)
            clavicle_jnt_pos = cmds.xform(clavicle_jnt,q=True,t=True,ws=True)
            cmds.xform(clavicle_offset,t=clavicle_jnt_pos,ws=True)
            cmds.xform(clavicle_offset,ro=(0,0,0),ws=True)
            if spine_clavicle_conexion_check is True:
                cmds.parent(clavicle_offset,"chest_c_ctr_{}".format(spine_clavicle_conexion))
            else:
                cmds.parent(clavicle_offset,control_center)
                
            #5.4 Creacion del Ik Handle
            clavicle_ik = cmds.ikHandle(sj=clavicle_jnt,ee=clavicle_end_jnt,sol="ikSCsolver",ap=False,s=0,n="clavicleIkHandle_{}_ik_{}".format(side_c,number_c_l))[0]
            cmds.parent(clavicle_ik,clavicle_ctr)
            Hide(clavicle_ik)
            
            # 5.5.1 Configuracion del autostretch: eje X
            AttrSeparator(clavicle_ctr)
            cmds.addAttr(clavicle_ctr,ln= "autoStretch",at= "double",min= 0,max=1,dv=1,k=True)
            
            clavicle_ref = cmds.duplicate(clavicle,n="clavicleDistanceRef_{}_loc_{}".format(side_c,number_c_l))[0]
            clavicle_end_ref = cmds.duplicate(clavicle_end,n="clavicleEndDistanceRef_{}_loc_{}".format(side_c,number_c_l))[0]
            cmds.xform(clavicle_ref,ro=(0,0,0),ws=True)
            cmds.xform(clavicle_end_ref,ro=(0,0,0),ws=True)
            if spine_clavicle_conexion_check is True:
                cmds.parent(clavicle_ref,"chest_c_ctr_{}".format(spine_clavicle_conexion))
            else:
                cmds.parent(clavicle_ref,control_center)
            cmds.parent(clavicle_end_ref,clavicle_ctr)
            Hide(clavicle_ref)
            Hide(clavicle_end_ref)
            
            clavicle_length_dist = cmds.createNode("distanceBetween",n="clavicleLength_{}_dist_{}".format(side_c,number_c_l))
            cmds.connectAttr("{}.worldPosition[0]".format(clavicle_ref),"{}.point1".format(clavicle_length_dist))
            cmds.connectAttr("{}.worldPosition[0]".format(clavicle_end_ref),"{}.point2".format(clavicle_length_dist))
            
            clavicle_stretch_div = cmds.createNode("multiplyDivide",n="clavicleStretch_{}_div_{}".format(side_c,number_c_l))
            cmds.setAttr("{}.operation".format(clavicle_stretch_div),2)
            cmds.connectAttr("{}.distance".format(clavicle_length_dist),"{}.input1X".format(clavicle_stretch_div))
            clavicle_distance = cmds.getAttr("{}.distance".format(clavicle_length_dist))
            cmds.setAttr("{}.input2X".format(clavicle_stretch_div),clavicle_distance)
            
            clavicle_global_stretch_div = cmds.createNode("multiplyDivide",n="clavicleGlobalStretch_{}_div_{}".format(side_c,number_c_l))
            cmds.setAttr("{}.operation".format(clavicle_global_stretch_div),2)
            cmds.connectAttr("{}.outputX".format(clavicle_stretch_div),"{}.input1X".format(clavicle_global_stretch_div))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.input2X".format(clavicle_global_stretch_div))
            
            switch_autostretch_blend = cmds.createNode("blendColors",n="switchAutoStretch_{}_blend_{}".format(side_c,number_c_l))
            cmds.connectAttr("{}.autoStretch".format(clavicle_ctr),"{}.blender".format(switch_autostretch_blend))
            cmds.connectAttr("{}.outputX".format(clavicle_global_stretch_div),"{}.color1R".format(switch_autostretch_blend))
            cmds.setAttr("{}.color2R".format(switch_autostretch_blend),1)
            
            cmds.connectAttr("{}.outputR".format(switch_autostretch_blend),"{}.scaleX".format(clavicle_jnt))
            
            #Cerrar rig
            LockScaleVis(clavicle_ctr)
            
        win.clavicleLeftButton.clicked.connect(BuildLeftClavicle)
        
        def BuildRightClavicle():
            clavicle = "clavicle_r_loc_{}".format(number_c_r)
            clavicle_end = "clavicleEnd_r_loc_{}".format(number_c_r)
            # 5.2.2 Creacion de la cadena de huesos clavicula
            del_cons = cmds.aimConstraint(clavicle_end,clavicle,offset=(0,0,0),weight=1,aimVector=(-1,0,0),upVector=(0,-1,0),worldUpType="scene")[0]
            cmds.delete(del_cons)
            del_cons = cmds.aimConstraint(clavicle,clavicle_end,offset=(0,0,0),weight=1,aimVector=(1,0,0),upVector=(0,-1,0),worldUpType="scene")[0]
            cmds.delete(del_cons)
            side_c = clavicle.split("_")[1]
            cmds.select(cl=1)
            clavicle_jnt = cmds.joint(n="clavicle_{}_skn_{}".format(side_c,number_c_r))
            clavicle_matrix = cmds.xform(clavicle,q=True,matrix=True,ws=True)
            cmds.xform(clavicle_jnt,matrix=clavicle_matrix,ws=True)
            clavicle_end_jnt = cmds.joint(n="clavicleEnd_{}_jnt_{}".format(side_c,number_c_r))
            clavicle_end_matrix = cmds.xform(clavicle_end,q=True,matrix=True,ws=True)
            cmds.xform(clavicle_end_jnt,matrix=clavicle_end_matrix,ws=True)
            spine_clavicle_conexion_check = win.checkBoxClavicleSpineConexion.isChecked()
            spine_clavicle_conexion = win.spinClavicleConexion.value()
            if spine_clavicle_conexion_check is True:
                cmds.parent(clavicle_jnt,"chest_c_skn_{}".format(spine_clavicle_conexion))
            else:
                cmds.parent(clavicle_jnt,char_skeleton)
            #5.3.1 Creacion del control clavicle
            clavicle_ctr = cmds.duplicate("clavicle_{}_ctr_0".format(side_c),n="clavicle_{}_ctr_{}".format(side_c,number_c_r))[0]
            clavicle_offset = CreateOffset(clavicle_ctr,number_c_r)
            cmds.setAttr("{}.scaleX".format(clavicle_offset),-1)  
            clavicle_jnt_pos = cmds.xform(clavicle_jnt,q=True,t=True,ws=True)
            cmds.xform(clavicle_offset,t=clavicle_jnt_pos,ws=True)
            cmds.xform(clavicle_offset,ro=(0,0,0),ws=True)
            if spine_clavicle_conexion_check is True:
                cmds.parent(clavicle_offset,"chest_c_ctr_{}".format(spine_clavicle_conexion))
            else:
                cmds.parent(clavicle_offset,control_center)
            
            #5.4 Creacion del Ik Handle
            clavicle_ik = cmds.ikHandle(sj=clavicle_jnt,ee=clavicle_end_jnt,sol="ikRPsolver",ap=False,s=0,n="clavicleIkHandle_{}_ik_{}".format(side_c,number_c_r))[0]
            cmds.parent(clavicle_ik,clavicle_ctr)
            Hide(clavicle_ik)
            
            # 5.5.1 Configuracion del autostretch: eje X
           
            AttrSeparator(clavicle_ctr)
            cmds.addAttr(clavicle_ctr,ln= "autoStretch",at= "double",min= 0,max=1,dv=1,k=True)
            
            clavicle_ref = cmds.duplicate(clavicle,n="clavicleDistanceRef_{}_loc_{}".format(side_c,number_c_r))[0]
            clavicle_end_ref = cmds.duplicate(clavicle_end,n="clavicleEndDistanceRef_{}_loc_{}".format(side_c,number_c_r))[0]
            cmds.xform(clavicle_ref,ro=(0,0,0),ws=True)
            cmds.xform(clavicle_end_ref,ro=(0,0,0),ws=True)
            if spine_clavicle_conexion_check is True:
                cmds.parent(clavicle_ref,"chest_c_ctr_{}".format(spine_clavicle_conexion))
            else:
                cmds.parent(clavicle_ref,control_center)
            cmds.parent(clavicle_end_ref,clavicle_ctr)
            Hide(clavicle_ref)
            Hide(clavicle_end_ref)
            
            clavicle_length_dist = cmds.createNode("distanceBetween",n="clavicleLength_{}_dist_{}".format(side_c,number_c_r))
            cmds.connectAttr("{}.worldPosition[0]".format(clavicle_ref),"{}.point1".format(clavicle_length_dist))
            cmds.connectAttr("{}.worldPosition[0]".format(clavicle_end_ref),"{}.point2".format(clavicle_length_dist))
            
            clavicle_stretch_div = cmds.createNode("multiplyDivide",n="clavicleStretch_{}_div_{}".format(side_c,number_c_r))
            cmds.setAttr("{}.operation".format(clavicle_stretch_div),2)
            cmds.connectAttr("{}.distance".format(clavicle_length_dist),"{}.input1X".format(clavicle_stretch_div))
            clavicle_distance = cmds.getAttr("{}.distance".format(clavicle_length_dist))
            cmds.setAttr("{}.input2X".format(clavicle_stretch_div),clavicle_distance)
            
            clavicle_global_stretch_div = cmds.createNode("multiplyDivide",n="clavicleGlobalStretch_{}_div_{}".format(side_c,number_c_r))
            cmds.setAttr("{}.operation".format(clavicle_global_stretch_div),2)
            cmds.connectAttr("{}.outputX".format(clavicle_stretch_div),"{}.input1X".format(clavicle_global_stretch_div))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.input2X".format(clavicle_global_stretch_div))
            
            switch_autostretch_blend = cmds.createNode("blendColors",n="switchAutoStretch_{}_blend_{}".format(side_c,number_c_r))
            cmds.connectAttr("{}.autoStretch".format(clavicle_ctr),"{}.blender".format(switch_autostretch_blend))
            cmds.connectAttr("{}.outputX".format(clavicle_global_stretch_div),"{}.color1R".format(switch_autostretch_blend))
            cmds.setAttr("{}.color2R".format(switch_autostretch_blend),1)
            
            cmds.connectAttr("{}.outputR".format(switch_autostretch_blend),"{}.scaleX".format(clavicle_jnt))
        
            #Cerrar rig
            LockScaleVis(clavicle_ctr)
            
        win.clavicleRightButton.clicked.connect(BuildRightClavicle)
        
        def BuildLeftArm():
            number_uparm_joints = win.spinBoxUparmNumberJoints.value()
            number_forearm_joints = win.spinBoxForearmNumberJoints.value()
            side_a = "l"
            shoulder = "shoulder_{}_loc_{}".format(side_a,number_a_l)
            elbow = "elbow_{}_loc_{}".format(side_a,number_a_l)
            hand = "hand_{}_loc_{}".format(side_a,number_a_l)
            hand_end = "handEnd_{}_loc_{}".format(side_a,number_a_l)
            shoulder_roll_l_system = cmds.group(n="shoulderRollSystem_l_grp_{}".format(number_a_l),em=1,p=arm_l_rig)
            shoulder_non_roll_l = cmds.group(n="shoulderNonRoll_l_grp_{}".format(number_a_l),em=1,p=shoulder_roll_l_system)
            forearm_roll_l_system = cmds.group(n="forearmRollSystem_l_grp_{}".format(number_a_l),em=1,p=arm_l_rig)
            elbow_non_roll_l = cmds.group(n="elbowNonRoll_l_grp_{}".format(number_a_l),em=1,p=forearm_roll_l_system)
            hand_non_roll_l = cmds.group(n="handNonRoll_l_grp_{}".format(number_a_l),em=1,p=forearm_roll_l_system)
            for axis in "XYZ":
                cmds.connectAttr("{}.globalScale".format(control_base),"{}.scale{}".format(shoulder_roll_l_system,axis))
            # 6.1 Creacion de los huesos y reorientacion de locators
            del_cons = cmds.aimConstraint(elbow,
                                            shoulder,
                                            offset=(0,0,0),
                                            weight=1,
                                            aimVector=(1,0,0),
                                            upVector=(0,1,0),
                                            worldUpType="scene")[0]
            cmds.delete(del_cons)
            del_cons = cmds.aimConstraint(hand,
                                          elbow,
                                          offset=(0,0,0),
                                          weight=1,
                                          aimVector=(1,0,0),
                                          upVector=(0,1,0),
                                          worldUpType="scene")[0]
            cmds.delete(del_cons)
            del_cons = cmds.aimConstraint(hand_end,
                                          hand,
                                          offset=(0,0,0),
                                          weight=1,
                                          aimVector=(1,0,0),
                                          upVector=(0,1,0),
                                          worldUpType="scene")[0]
            cmds.delete(del_cons)
            del_cons = cmds.aimConstraint(hand,
                                          hand_end,
                                          offset=(0,0,0),
                                          weight=1,
                                          aimVector=(-1,0,0),
                                          upVector=(0,1,0),
                                          worldUpType="scene")[0]
            cmds.delete(del_cons)
            
            cmds.select(cl=1)
            cmds.select(shoulder)
            shoulder_jnt = cmds.joint(n="shoulder_{}_jnt_{}".format(side_a,number_a_l))
            cmds.select(cl=1)
            
            elbow_jnt = cmds.joint(n="elbow_{}_jnt_{}".format(side_a,number_a_l))
            elbow_pos = cmds.xform(elbow,q=True,matrix=True,ws=True)
            cmds.xform(elbow_jnt,matrix=elbow_pos,ws=True)
            cmds.parent(elbow_jnt,shoulder_jnt)
            arm_end_jnt = cmds.joint(n="armEnd_{}_jnt_{}".format(side_a,number_a_l))
            hand_pos = cmds.xform(hand,q=True,matrix=True,ws=True)
            cmds.xform(arm_end_jnt,matrix=hand_pos,ws=True)
            
            cmds.select(cl=1)
            hand_jnt = cmds.joint(n="hand_{}_skn_{}".format(side_a,number_a_l))
            cmds.xform(hand_jnt,matrix=hand_pos,ws=True)
            
            hand_end_jnt = cmds.joint(n="handEnd_{}_jnt_{}".format(side_a,number_a_l))
            hand_end_pos = cmds.xform(hand_end,q=True,matrix=True,ws=True)
            cmds.xform(hand_end_jnt,matrix=hand_end_pos,ws=True)
            
            shoulder_offset = CreateOffset(shoulder_jnt,number_a_l)
            cmds.parent(shoulder_offset,char_skeleton)
            
            if "l" in side_a:
                cmds.setAttr("{}.preferredAngleY".format(elbow_jnt),-90)
            if "r" in side_a:
                cmds.setAttr("{}.preferredAngleY".format(elbow_jnt),90)
                
            hand_offset = CreateOffset(hand_jnt,number_a_l)
            cmds.parent(hand_offset,char_skeleton)
            cmds.pointConstraint(arm_end_jnt,hand_offset,mo=False,n="armEndPoint_{}_cns_{}".format(side_a,number_a_l))
            # 6.2 Creacion del Ik Handle del la cadena principal
            arm_main_ik = cmds.ikHandle( sj=shoulder_jnt, ee=arm_end_jnt, s="sticky",n="armMainikHandle_{}_ik_{}".format(side_a,number_a_l),sol="ikRPsolver")[0]
            if "l" in side_a:
                cmds.parent(arm_main_ik,arm_l_rig)
            if "r" in side_a:
                cmds.parent(arm_main_ik,arm_r_rig)
        
            # 6.3.1 Configuracion de la cadena NonRoll de shoulder
            shoulder_non_roll = cmds.duplicate(shoulder_jnt,po=True,n="shoulderNonRoll_{}_jnt_{}".format(side_a,number_a_l))[0]
            shoulder_end_non_roll = cmds.duplicate(elbow_jnt,po=True,n="shoulderEndNonRoll_{}_jnt_{}".format(side_a,number_a_l))[0]
            cmds.parent(shoulder_end_non_roll,shoulder_non_roll)
            
            shoulder_nonroll_ik = cmds.ikHandle( sj=shoulder_non_roll, ee=shoulder_end_non_roll, s="sticky",n="shoulderNonRollikHandle_{}_ik_{}".format(side_a,number_a_l),sol="ikRPsolver")[0]
            for axis in "XYZ":
                cmds.setAttr("{}.poleVector{}".format(shoulder_nonroll_ik,axis),0)
            if "l" in side_a:
                cmds.parent(shoulder_non_roll,shoulder_non_roll_l)
                cmds.parent(shoulder_nonroll_ik,shoulder_non_roll_l)
            if "r" in side_a:
                cmds.parent(shoulder_non_roll,shoulder_non_roll_r)
                cmds.parent(shoulder_nonroll_ik,shoulder_non_roll_r)
            
            cmds.pointConstraint(shoulder_jnt,shoulder_non_roll,mo=False,n="shouldertoNonPoint_{}_cns_{}".format(side_a,number_a_l))
            cmds.pointConstraint(elbow_jnt,shoulder_nonroll_ik,mo=False,n="shoulderEndtiIkPoint_{}_cns_{}".format(side_a,number_a_l))
            
            # 6.3.2 Configuracion de la cadena NonRoll del elbow
            elbow_non_roll = cmds.duplicate(elbow_jnt,po=True,n="elbowNonRoll_{}_jnt_{}".format(side_a,number_a_l))[0]
            elbow_end_non_roll = cmds.duplicate(arm_end_jnt,po=True,n="elbowEndNonRoll_{}_jnt_{}".format(side_a,number_a_l))[0]
            cmds.parent(elbow_end_non_roll,elbow_non_roll)
            
            elbow_nonroll_ik = cmds.ikHandle( sj=elbow_non_roll, ee=elbow_end_non_roll, s="sticky",n="elbowNonRollikHandle_{}_ik_{}".format(side_a,number_a_l),sol="ikRPsolver")[0]
            for axis in "XYZ":
                cmds.setAttr("{}.poleVector{}".format(elbow_nonroll_ik,axis),0)
            if "l" in side_a:
                cmds.parent(elbow_non_roll,elbow_non_roll_l)
                cmds.parent(elbow_nonroll_ik,elbow_non_roll_l)
            if "r" in side_a:
                cmds.parent(elbow_non_roll,elbow_non_roll_r)
                cmds.parent(elbow_nonroll_ik,elbow_non_roll_r)
            
            cmds.pointConstraint(elbow_jnt,elbow_non_roll,mo=False,n="elbowtoNonPoint_{}_cns_{}".format(side_a,number_a_l))
            cmds.pointConstraint(hand_jnt,elbow_nonroll_ik,mo=False,n="handtiIkNonPoint_{}_cns_{}".format(side_a,number_a_l))
            
            elbow_twist_value = cmds.duplicate(elbow_jnt,po=True,n="elbowTwistValue_{}_jnt_{}".format(side_a,number_a_l))[0]
            cmds.parent(elbow_twist_value,elbow_jnt)
            cmds.aimConstraint(hand_jnt,
                                elbow_twist_value,
                                offset=(0,0,0),
                                weight=1,
                                aimVector=(1,0,0),
                                upVector=(0,1,0),
                                worldUpType="objectrotation",
                                worldUpVector=(0,1,0),
                                worldUpObject=elbow_non_roll,
                                n="handtoElbowNonAim_{}_cns_{}".format(side_a,number_a_l))
            
            if "l" in side_a:
                cmds.parentConstraint(shoulder_non_roll,elbow_non_roll_l,mo=True,n="shoulderNontoElbowNonGrpParent_l_cns_{}".format(number_a_l))
            if "r" in side_a:
                cmds.parentConstraint(shoulder_non_roll,elbow_non_roll_r,mo=True,n="shoulderNontoElbowNonGrpParent_r_cns_{}".format(number_a_l))
            
            # 6.3.3 Confuguracion de la cadena Non Roll Hand
            hand_non_roll = cmds.duplicate(hand_jnt,po=True,n="handNonRoll_{}_jnt_{}".format(side_a,number_a_l))[0]
            hand_end_non_roll = cmds.duplicate(hand_end_jnt,po=True,n="handEndNonRoll_{}_jnt_{}".format(side_a,number_a_l))[0]
            cmds.parent(hand_end_non_roll,hand_non_roll)
            
            hand_nonroll_ik = cmds.ikHandle( sj=hand_non_roll, ee=hand_end_non_roll, s="sticky",n="handNonRollikHandle_{}_ik_{}".format(side_a,number_a_l),sol="ikRPsolver")[0]
            for axis in "XYZ":
                cmds.setAttr("{}.poleVector{}".format(hand_nonroll_ik,axis),0)
                
            if "l" in side_a:
                cmds.parent(hand_non_roll,hand_non_roll_l)
                cmds.parent(hand_nonroll_ik,hand_non_roll_l)
            if "r" in side_a:
                cmds.parent(hand_non_roll,hand_non_roll_r)
                cmds.parent(hand_nonroll_ik,hand_non_roll_r)
            
            cmds.pointConstraint(hand_jnt,hand_non_roll)
            cmds.pointConstraint(hand_end_jnt,hand_nonroll_ik)
            
            hand_twist_value = cmds.duplicate(hand_jnt,po=True,n="handTwistValue_{}_jnt_{}".format(side_a,number_a_l))[0]
            cmds.parent(hand_twist_value,hand_jnt)
            cmds.aimConstraint(hand_end_jnt,
                                hand_twist_value,
                                offset=(0,0,0),
                                weight=1,
                                aimVector=(1,0,0),
                                upVector=(0,1,0),
                                worldUpType="objectrotation",
                                worldUpVector=(0,1,0),
                                worldUpObject=hand_non_roll,
                                n="handEndtoHandTwistNonAim_{}_cns_{}".format(side_a,number_a_l))
            
            
            if "l" in side_a:
                cmds.parentConstraint(elbow_jnt,hand_non_roll_l,mo=True,n="elbowtohandNonGrpParent_l_cns_{}".format(number_a_l))
            if "r" in side_a:
                cmds.parentConstraint(elbow_jnt,hand_non_roll_r,mo=True,n="elbowtohandNonGrpParent_r_cns_{}".format(number_a_l))        
        
            # 6.4.1 Creacion de la cadena twist del shoulder
            shoulder_twist_list = JointChain(shoulder,elbow,"shoulderTwist",number_uparm_joints)
            new_shoulder_twist_list=[] 
            for shoulder_twist in shoulder_twist_list:
                shoulder_twist_jnt = cmds.rename(shoulder_twist,"{}_{}_skn_{}".format(shoulder_twist,side_a,number_a_l))
                new_shoulder_twist_list.append(shoulder_twist_jnt)
            first_shoulder_twist_jnt = new_shoulder_twist_list[0]
            cmds.parent(first_shoulder_twist_jnt,"shoulderRollSystem_{}_grp_{}".format(side_a,number_a_l))
            last_shoulder_twist_jnt = new_shoulder_twist_list[-1]
            ikhandle_shoulder_twist_list = cmds.ikHandle(sj=first_shoulder_twist_jnt,
                                                         ee=last_shoulder_twist_jnt,
                                                         sol="ikSplineSolver",
                                                         scv=False,
                                                         pcv=False,
                                                         n="shoulderTwistikHandle_{}_ik_{}".format(side_a,number_a_l))
            shoulder_twist_ik = ikhandle_shoulder_twist_list[0]
            shoulder_twist_crv = ikhandle_shoulder_twist_list[2]
            shoulder_twist_crv = cmds.rename(shoulder_twist_crv,"shoulderTwist_{}_crv_{}".format(side_a,number_a_l))
            cmds.parent(shoulder_twist_ik,"shoulderRollSystem_{}_grp_{}".format(side_a,number_a_l))
            cmds.parent(shoulder_twist_crv,"{}ArmRig_{}_grp".format(name,side_a))
            
            elbow_twist_mult = cmds.createNode("multiplyDivide",n="elbowTwistValue_{}_mult_{}".format(side_a,number_a_l))
            cmds.connectAttr("{}.rotateX".format(elbow_twist_value),"{}.input1X".format(elbow_twist_mult))
            cmds.setAttr("{}.input2X".format(elbow_twist_mult),-1)
            cmds.connectAttr("{}.outputX".format(elbow_twist_mult),"{}.twist".format(shoulder_twist_ik))
        
            # 6.4.2 Creacion de la cadena twist del forearm
            forearm_twist_list = JointChain(elbow,hand,"forearmTwist",number_forearm_joints)
            new_forearm_twist_list=[] 
            for forearm_twist in forearm_twist_list:
                forearm_twist_jnt = cmds.rename(forearm_twist,"{}_{}_skn_{}".format(forearm_twist,side_a,number_a_l))
                new_forearm_twist_list.append(forearm_twist_jnt)
            first_forearm_twist_jnt = new_forearm_twist_list[0]
            cmds.parent(first_forearm_twist_jnt,elbow_jnt)
            last_forearm_twist_jnt = new_forearm_twist_list[-1]
            ikhandle_forearm_twist_list = cmds.ikHandle(sj=first_forearm_twist_jnt,
                                                         ee=last_forearm_twist_jnt,
                                                         sol="ikSplineSolver",
                                                         scv=False,
                                                         pcv=False,
                                                         n="forearmTwistikHandle_{}_ik_{}".format(side_a,number_a_l))
            forearm_twist_ik = ikhandle_forearm_twist_list[0]
            forearm_twist_crv = ikhandle_forearm_twist_list[2]
            forearm_twist_crv = cmds.rename(forearm_twist_crv,"forearmTwist_{}_crv_{}".format(side_a,number_a_l))
            cmds.parent(forearm_twist_ik,"forearmRollSystem_{}_grp_{}".format(side_a,number_a_l))
            cmds.parent(forearm_twist_crv,"{}ArmRig_{}_grp".format(name,side_a))
            forearm_twist_mult = cmds.createNode("multiplyDivide",n="forearmTwistValue_{}_mult_{}".format(side_a,number_a_l))
            cmds.connectAttr("{}.rotateX".format(hand_twist_value),"{}.input1X".format(forearm_twist_mult))
            cmds.setAttr("{}.input2X".format(forearm_twist_mult),-1)
            cmds.connectAttr("{}.outputX".format(forearm_twist_mult),"{}.twist".format(forearm_twist_ik))    
        
            #6.5.1 Creacion del control HandIK
            hand_ik_ctr = cmds.duplicate("handIK_{}_ctr_0".format(side_a),n="handIK_{}_ctr_{}".format(side_a,number_a_l))[0]
            hand_ik_offset = CreateOffset(hand_ik_ctr,number_a_l)
            hand_pos = cmds.xform(hand_jnt,q=True,matrix=True,ws=True)
            cmds.xform(hand_ik_offset,matrix=hand_pos,ws=True)
            cmds.parent(hand_ik_offset,control_center)
            
            AttrSeparator(hand_ik_ctr)    
            cmds.addAttr(hand_ik_ctr,ln= "elbow",at= "double",dv=1,k=True)
            cmds.addAttr(hand_ik_ctr,ln= "autoStretch",at= "double",max=1,min=0,dv=1,k=True)
        
            # 6.5.2 Creacion del control armPole
            arm_pole_ctr = cmds.duplicate("armPole_{}_ctr_0".format(side_a),n="armPole_{}_ctr_{}".format(side_a,number_a_l))[0]
            arm_pole_offset = CreateOffset(arm_pole_ctr,number_a_l)
            pole_loc = PoleVector(sel=[shoulder_jnt,elbow_jnt,arm_end_jnt],side=side_a)
        
            pole_desplace_distance = cmds.getAttr("{}.translateX".format(elbow_jnt))
            pole_loc_child = cmds.duplicate(pole_loc,n="PoleVectorChild_{}_loc_{}".format(side_a,number_a_l))[0]
            cmds.parent(pole_loc_child,pole_loc)
            cmds.setAttr("{}.translateX".format(pole_loc_child),pole_desplace_distance)
            pole_pos = cmds.xform(pole_loc_child,q=True,t=True,ws=True)
            cmds.xform(arm_pole_offset,t=pole_pos,ws=True)
            cmds.parent(arm_pole_offset,control_center)
            cmds.delete(pole_loc)
            
            AttrSeparator(arm_pole_ctr)
            cmds.addAttr(arm_pole_ctr,ln= "pinElbow",at= "double",max=1,min=0,dv=0,k=True)
        
            #6.5.3 Creacion del control armSettings
            arm_settings_ctr = cmds.duplicate("armSettings_{}_ctr_0".format(side_a),n="armSettings_{}_ctr_{}".format(side_a,number_a_l))[0]
            arm_settings_offset = CreateOffset(arm_settings_ctr,number_a_l)
            cmds.xform(arm_settings_offset,matrix=hand_pos,ws=True)
            arm_settings_desplace_distance = cmds.getAttr("{}.translateX".format(hand_end_jnt))
            refresh_pos_arm_set = cmds.getAttr("{}.translateX".format(arm_settings_offset))
            cmds.setAttr("{}.translateX".format(arm_settings_offset),refresh_pos_arm_set+arm_settings_desplace_distance+arm_settings_desplace_distance)
            cmds.parent(arm_settings_offset,control_center)
            
            AttrSeparator(arm_settings_ctr)
            cmds.addAttr(arm_settings_ctr,ln= "armIK",at= "double",max=1,min=0,dv=0,k=True)
            cmds.addAttr(arm_settings_ctr,ln= "autoSquash",at= "double",max=1,min=0,dv=0,k=True)
            cmds.addAttr(arm_settings_ctr,ln= "visBends",at= "double",max=1,min=0,dv=1,k=True)
            cmds.addAttr(arm_settings_ctr,ln= "visFingers",at= "double",max=1,min=0,dv=1,k=True)
        
            #6.5.4 Creacion del control shoulderFK
            shoulder_fk_ctr = cmds.duplicate("shoulderFK_{}_ctr_0".format(side_a),n="shoulderFK_{}_ctr_{}".format(side_a,number_a_l))[0]
            shoulder_fk_offset = CreateOffset(shoulder_fk_ctr,number_a_l)
            shoulder_pos = cmds.xform(shoulder_jnt,q=True,matrix=True,ws=True)
            cmds.xform(shoulder_fk_offset,matrix=shoulder_pos,ws=True)
            cmds.parent(shoulder_fk_offset,"center_c_ctr_1")
            
            AttrSeparator(shoulder_fk_ctr)
            cmds.addAttr(shoulder_fk_ctr,ln= "stretch",at= "double",dv=1,k=True)
            
            #6.5.5 Creacion del control elbowFK
            elbow_fk_ctr = cmds.duplicate("elbowFK_{}_ctr_0".format(side_a),n="elbowFK_{}_ctr_{}".format(side_a,number_a_l))[0]
            elbow_fk_offset = CreateOffset(elbow_fk_ctr,number_a_l)
            elbow_pos = cmds.xform(elbow_jnt,q=True,matrix=True,ws=True)
            cmds.xform(elbow_fk_offset,matrix=elbow_pos,ws=True)
            cmds.parent(elbow_fk_offset,shoulder_fk_ctr)
            
            AttrSeparator(elbow_fk_ctr)
            cmds.addAttr(elbow_fk_ctr,ln= "stretch",at= "double",dv=1,k=True)
            
            #6.5.6 Creacion del control handFK
            hand_fk_ctr = cmds.duplicate("handFK_{}_ctr_0".format(side_a),n="handFK_{}_ctr_{}".format(side_a,number_a_l))[0]
            hand_fk_offset = CreateOffset(hand_fk_ctr,number_a_l)
            hand_pos = cmds.xform(hand_jnt,q=True,matrix=True,ws=True)
            cmds.xform(hand_fk_offset,matrix=hand_pos,ws=True)
            cmds.parent(hand_fk_offset,elbow_fk_ctr)
        
            #6.6.1 Creacion de los joints PAC
            shoulder_pac = cmds.duplicate(shoulder_jnt,n="shoulderPAC_{}_jnt_{}".format(side_a,number_a_l),po=True)[0]
            cmds.parent(shoulder_pac,shoulder_fk_ctr)
            
            elbow_pac = cmds.duplicate(elbow_jnt,n="elbowPAC_{}_jnt_{}".format(side_a,number_a_l),po=True)[0]
            cmds.parent(elbow_pac,elbow_fk_ctr)
            
            hand_fk_pac = cmds.duplicate(hand_jnt,n="handFkPAC_{}_jnt_{}".format(side_a,number_a_l),po=True)[0]
            cmds.parent(hand_fk_pac,hand_fk_ctr)
            
            hand_ik_pac = cmds.duplicate(hand_jnt,n="handIkPAC_{}_jnt_{}".format(side_a,number_a_l),po=True)[0]
            cmds.parent(hand_ik_pac,hand_ik_ctr)
           
           #6.6.2 Relaciones basicas entre controles, huesos e ikHandles
            cmds.pointConstraint(hand_ik_pac,arm_main_ik,n="PacIkHandPoint_{}_cns_{}".format(side_a,number_a_l))
            cmds.poleVectorConstraint(arm_pole_ctr,arm_main_ik,w=1,n="PoleIkPole_{}_cns_{}".format(side_a,number_a_l))
            orient_shoulder_cns = cmds.orientConstraint(shoulder_pac,shoulder_jnt,mo=False,n="PacShoulderOrient_{}_cns_{}".format(side_a,number_a_l))[0]
            cmds.cycleCheck(e=False)
            orient_elbow_cns = cmds.orientConstraint(elbow_pac,elbow_jnt,mo=False,n="PacElbowOrient_{}_cns_{}".format(side_a,number_a_l))[0]
            cmds.parentConstraint(hand_jnt,arm_settings_offset,mo=True,n="handSettingsParent_{}_cns_{}".format(side_a,number_a_l))
            orient_hand_cns = cmds.orientConstraint(hand_fk_pac,hand_ik_pac,hand_jnt,n="HandPACFkIkOrient_{}_cns_{}".format(side_a,number_a_l))[0]
        
            #6.6.3 Conexiones para realizar el switch FK/IK
            cmds.connectAttr("{}.armIK".format(arm_settings_ctr),"{}.ikBlend".format(arm_main_ik))
            cmds.connectAttr("{}.armIK".format(arm_settings_ctr),"{}.{}W1".format(orient_hand_cns,hand_ik_pac))
            reverse_switch_armik = cmds.createNode("reverse",n="armIk_{}_rev_{}".format(side_a,number_a_l))
            cmds.connectAttr("{}.armIK".format(arm_settings_ctr),"{}.inputX".format(reverse_switch_armik))
            cmds.connectAttr("{}.outputX".format(reverse_switch_armik),"{}.{}W0".format(orient_hand_cns,hand_fk_pac))
            cmds.connectAttr("{}.outputX".format(reverse_switch_armik),"{}.{}W0".format(orient_elbow_cns,elbow_pac))
            cmds.cycleCheck(e=True)
            cmds.connectAttr("{}.outputX".format(reverse_switch_armik),"{}.{}W0".format(orient_shoulder_cns,shoulder_pac))
            cmds.connectAttr("{}.armIK".format(arm_settings_ctr),"{}.visibility".format(hand_ik_offset))
            cmds.connectAttr("{}.armIK".format(arm_settings_ctr),"{}.visibility".format(arm_pole_offset))
            cmds.connectAttr("{}.outputX".format(reverse_switch_armik),"{}.visibility".format(shoulder_fk_offset))
            
            #6.6.4 Otras conexiones
            cmds.connectAttr("{}.elbow".format(hand_ik_ctr),"{}.twist".format(arm_main_ik))
            
            # 6.7 Configuracion del Squash/Stretch
            # 6.7.1 Creacion de locators para medir las distancias
            stretch_shoulder_loc = cmds.spaceLocator(n="stretchShoulder_{}_loc_{}".format(side_a,number_a_l))[0]
            stretch_elbow_loc = cmds.spaceLocator(n="stretchElbow_{}_loc_{}".format(side_a,number_a_l))[0]
            stretch_hand_loc = cmds.spaceLocator(n="stretchHand_{}_loc_{}".format(side_a,number_a_l))[0]
            shoulder_t = cmds.xform(shoulder_jnt,q=True,t=True,ws=True)
            elbow_t = cmds.xform(elbow_jnt,q=True,t=True,ws=True)
            hand_t = cmds.xform(hand_jnt,q=True,t=True,ws=True)
            cmds.xform(stretch_shoulder_loc,t=shoulder_t,ws=True)
            cmds.xform(stretch_elbow_loc,t=elbow_t,ws=True)
            cmds.xform(stretch_hand_loc,t=hand_t,ws=True)
            arm_cl_conexion_check = win.checkBoxArmClavicleConexion.isChecked()
            arm_cl_conexion = win.spinArmClavicleConexion.value()
            if arm_cl_conexion_check is True:
                cmds.parent(stretch_shoulder_loc,"clavicleEnd_{}_jnt_{}".format(side_a,arm_cl_conexion))
            else:
                cmds.parent(stretch_shoulder_loc,shoulder_fk_ctr)
            cmds.parent(stretch_elbow_loc, arm_pole_ctr)
            cmds.parent(stretch_hand_loc, hand_ik_ctr)
        
            # 6.7.2 Conectar los locators con nodos distance
            uparm_distance = cmds.createNode("distanceBetween",n="uparm_{}_dist_{}".format(side_a,number_a_l))
            cmds.connectAttr("{}.worldPosition[0]".format(stretch_shoulder_loc),"{}.point1".format(uparm_distance))
            cmds.connectAttr("{}.worldPosition[0]".format(stretch_elbow_loc),"{}.point2".format(uparm_distance))
            lowarm_distance = cmds.createNode("distanceBetween",n="lowarm_{}_dist_{}".format(side_a,number_a_l))
            cmds.connectAttr("{}.worldPosition[0]".format(stretch_elbow_loc),"{}.point1".format(lowarm_distance))
            cmds.connectAttr("{}.worldPosition[0]".format(stretch_hand_loc),"{}.point2".format(lowarm_distance))
            entire_arm_distance = cmds.createNode("distanceBetween",n="entireArm_{}_dist_{}".format(side_a,number_a_l))
            cmds.connectAttr("{}.worldPosition[0]".format(stretch_shoulder_loc),"{}.point1".format(entire_arm_distance))
            cmds.connectAttr("{}.worldPosition[0]".format(stretch_hand_loc),"{}.point2".format(entire_arm_distance))
           
            # 6.7.3 Configurar el stretchIK y normalizarlo
            arm_normal_stretch_div = cmds.createNode("multiplyDivide",n="armNormalStretch_{}_div_{}".format(side_a,number_a_l))
            cmds.setAttr("{}.operation".format(arm_normal_stretch_div),2)
            cmds.connectAttr("{}.distance".format(entire_arm_distance),"{}.input1X".format(arm_normal_stretch_div))
            etire_arm_distance_value = cmds.getAttr("{}.distance".format(entire_arm_distance))
            cmds.setAttr("{}.input2X".format(arm_normal_stretch_div),etire_arm_distance_value)
            
            arm_stretch_clamp = cmds.createNode("clamp",n="armStretch_{}_clamp_{}".format(side_a,number_a_l))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.minR".format(arm_stretch_clamp))
            cmds.setAttr("{}.maxR".format(arm_stretch_clamp),999)
            cmds.connectAttr("{}.outputX".format(arm_normal_stretch_div),"{}.inputR".format(arm_stretch_clamp))
            
            uparm_stretch_div = cmds.createNode("multiplyDivide",n="upArmStretch_{}_div_{}".format(side_a,number_a_l))
            cmds.setAttr("{}.operation".format(uparm_stretch_div),2)
            cmds.connectAttr("{}.distance".format(uparm_distance),"{}.input1X".format(uparm_stretch_div))
            uparm_distance_value = cmds.getAttr("{}.distance".format(uparm_distance))
            cmds.setAttr("{}.input2X".format(uparm_stretch_div),uparm_distance_value)
            
            lowarm_stretch_div = cmds.createNode("multiplyDivide",n="lowArmStretch_{}_div_{}".format(side_a,number_a_l))
            cmds.setAttr("{}.operation".format(lowarm_stretch_div),2)
            cmds.connectAttr("{}.distance".format(lowarm_distance),"{}.input1X".format(lowarm_stretch_div))
            lowarm_distance_value = cmds.getAttr("{}.distance".format(lowarm_distance))
            cmds.setAttr("{}.input2X".format(lowarm_stretch_div),lowarm_distance_value)
            
            arm_ikstretch_blend = cmds.createNode("blendColors",n="armIkStretch_{}_blend_{}".format(side_a,number_a_l))
            cmds.connectAttr("{}.outputX".format(uparm_stretch_div),"{}.color1G".format(arm_ikstretch_blend))
            cmds.connectAttr("{}.outputX".format(lowarm_stretch_div),"{}.color1B".format(arm_ikstretch_blend))
            cmds.connectAttr("{}.outputR".format(arm_stretch_clamp),"{}.color2G".format(arm_ikstretch_blend))
            cmds.connectAttr("{}.outputR".format(arm_stretch_clamp),"{}.color2B".format(arm_ikstretch_blend))
            
            arm_finalstretch_blend = cmds.createNode("blendColors",n= "armFinalStretch_{}_blend_{}".format(side_a,number_a_l))
            cmds.connectAttr("{}.armIK".format(arm_settings_ctr),"{}.blender".format(arm_finalstretch_blend))
            cmds.connectAttr("{}.outputG".format(arm_ikstretch_blend),"{}.color1G".format(arm_finalstretch_blend))            
            cmds.connectAttr("{}.outputB".format(arm_ikstretch_blend),"{}.color1B".format(arm_finalstretch_blend))
            cmds.setAttr("{}.color2G".format(arm_finalstretch_blend),1)
            cmds.setAttr("{}.color2B".format(arm_finalstretch_blend),1)
        
            # 6.7.4 Configurar el autoStretch 
            arm_stretchiness_blend = cmds.createNode("blendColors",n="armStretchiness_{}_blend_{}".format(side_a,number_a_l))
            cmds.connectAttr("{}.outputG".format(arm_finalstretch_blend),"{}.color1G".format(arm_stretchiness_blend))
            cmds.connectAttr("{}.outputB".format(arm_finalstretch_blend),"{}.color1B".format(arm_stretchiness_blend))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.color2G".format(arm_stretchiness_blend))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.color2B".format(arm_stretchiness_blend))
            
            arm_stretch_global_div = cmds.createNode("multiplyDivide",n="armStretchByGlobal_{}_div_{}".format(side_a,number_a_l))
            cmds.setAttr("{}.operation".format(arm_stretch_global_div),2)
            cmds.connectAttr("{}.outputG".format(arm_stretchiness_blend),"{}.input1X".format(arm_stretch_global_div))
            cmds.connectAttr("{}.outputB".format(arm_stretchiness_blend),"{}.input1Y".format(arm_stretch_global_div))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.input2X".format(arm_stretch_global_div))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.input2Y".format(arm_stretch_global_div))
            
            handik_autostretch_override_sum = cmds.createNode("plusMinusAverage",n="handIkAutostretchOverride_{}_sum_{}".format(side_a,number_a_l))
            cmds.connectAttr("{}.outputX".format(reverse_switch_armik),"{}.input2D[0].input2Dx".format(handik_autostretch_override_sum))
            cmds.connectAttr("{}.autoStretch".format(hand_ik_ctr),"{}.input2D[1].input2Dx".format(handik_autostretch_override_sum))
            
            handik_finalstretchiness_clamp = cmds.createNode("clamp",n="handIkFinalStretchiness_{}_clamp_{}".format(side_a,number_a_l))
            cmds.setAttr("{}.maxR".format(handik_finalstretchiness_clamp),1)
            cmds.connectAttr("{}.output2D.output2Dx".format(handik_autostretch_override_sum),"{}.inputR".format(handik_finalstretchiness_clamp))
            cmds.connectAttr("{}.outputR".format(handik_finalstretchiness_clamp),"{}.blender".format(arm_stretchiness_blend))
            
            # 6.7.5 Conectar con las escalas de los huesos
            cmds.connectAttr("{}.outputX".format(arm_stretch_global_div),"{}.scaleX".format(shoulder_jnt))
            cmds.connectAttr("{}.outputY".format(arm_stretch_global_div),"{}.scaleX".format(elbow_jnt))
        
            # 6.7.6 Configurar el stretch FK
            shoulderfk_stretchglobal_mult = cmds.createNode("multiplyDivide",n="shoulderFkStretchByGlobal_{}_mult_{}".format(side_a,number_a_l))
            cmds.connectAttr("{}.stretch".format(shoulder_fk_ctr),"{}.input1X".format(shoulderfk_stretchglobal_mult))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.input2X".format(shoulderfk_stretchglobal_mult))
            cmds.connectAttr("{}.outputX".format(shoulderfk_stretchglobal_mult),"{}.color2G".format(arm_finalstretch_blend))
            
            cmds.pointConstraint(elbow_jnt,elbow_fk_offset,n="elbowToOffsetPoint_{}_cns_{}".format(side_a,number_a_l))
            
            elbowfk_stretchglobal_mult = cmds.createNode("multiplyDivide",n="elbowFkStretchByGlobal_{}_mult_{}".format(side_a,number_a_l))
            cmds.connectAttr("{}.stretch".format(elbow_fk_ctr),"{}.input1X".format(elbowfk_stretchglobal_mult))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.input2X".format(elbowfk_stretchglobal_mult))
            cmds.connectAttr("{}.outputX".format(elbowfk_stretchglobal_mult),"{}.color2B".format(arm_finalstretch_blend))
            
            cmds.pointConstraint(arm_end_jnt,hand_fk_offset,n="armEndToHandOffsetPoint_{}_cns_{}".format(side_a,number_a_l))
        
            # 6.7.7 Conectar los joints del twistShoulderChain con el stetch
            shoulder_twiststretch_ci = cmds.createNode("curveInfo",n="shoulderTwistStretch_{}_ci_{}".format(side_a,number_a_l))
            shoulder_twist_crv_shape = cmds.listRelatives(shoulder_twist_crv,s=True)[0]
            cmds.connectAttr("{}.worldSpace[0]".format(shoulder_twist_crv_shape),"{}.inputCurve".format(shoulder_twiststretch_ci))
            
            shoulder_ikcurvelength_div = cmds.createNode("multiplyDivide",n="shoulderIkCurveLength_{}_div_{}".format(side_a,number_a_l))
            cmds.setAttr("{}.operation".format(shoulder_ikcurvelength_div),2)
            cmds.connectAttr("{}.arcLength".format(shoulder_twiststretch_ci),"{}.input1X".format(shoulder_ikcurvelength_div))
            shoulder_ikcurvelength_value = cmds.getAttr("{}.arcLength".format(shoulder_twiststretch_ci))
            cmds.setAttr("{}.input2X".format(shoulder_ikcurvelength_div),shoulder_ikcurvelength_value)
            
            
            shoulder_lengthbyglobal_div = cmds.createNode("multiplyDivide",n="shoulderLengthByGlobal_{}_div_{}".format(side_a,number_a_l))
            cmds.setAttr("{}.operation".format(shoulder_lengthbyglobal_div),2)
            cmds.connectAttr("{}.outputX".format(shoulder_ikcurvelength_div),"{}.input1X".format(shoulder_lengthbyglobal_div))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.input2X".format(shoulder_lengthbyglobal_div))
            
            n_twit_shoulder = len(new_shoulder_twist_list) 
            new_shoulder_twist_list_stretch = new_shoulder_twist_list[0:n_twit_shoulder-1]
            for shoulder_twist_joints in new_shoulder_twist_list_stretch:
                cmds.connectAttr("{}.outputX".format(shoulder_lengthbyglobal_div),"{}.scaleX".format(shoulder_twist_joints))
        
            #6.7.8 Conectar los joints del twistForearmChain con el stretch 
            forearm_twiststretch_ci = cmds.createNode("curveInfo",n="forearmTwistStretch_{}_ci_{}".format(side_a,number_a_l))
            forearm_twist_crv_shape = cmds.listRelatives(forearm_twist_crv,s=True)[0]
            cmds.connectAttr("{}.worldSpace[0]".format(forearm_twist_crv_shape),"{}.inputCurve".format(forearm_twiststretch_ci))
            
            forearm_ikcurvelength_div = cmds.createNode("multiplyDivide",n="forearmIkCurveLength_{}_div_{}".format(side_a,number_a_l))
            cmds.setAttr("{}.operation".format(forearm_ikcurvelength_div),2)
            cmds.connectAttr("{}.arcLength".format(forearm_twiststretch_ci),"{}.input1X".format(forearm_ikcurvelength_div))
            forearm_ikcurvelength_value = cmds.getAttr("{}.arcLength".format(forearm_twiststretch_ci))
            cmds.setAttr("{}.input2X".format(forearm_ikcurvelength_div),forearm_ikcurvelength_value)
            
            forearm_lengthbyglobal_div = cmds.createNode("multiplyDivide",n="forarmLengthByGlobal_{}_div_{}".format(side_a,number_a_l))
            cmds.setAttr("{}.operation".format(forearm_lengthbyglobal_div),2)
            cmds.connectAttr("{}.outputX".format(forearm_ikcurvelength_div),"{}.input1X".format(forearm_lengthbyglobal_div))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.input2X".format(forearm_lengthbyglobal_div))
            
            n_twit_forearm = len(new_forearm_twist_list) 
            new_forearm_twist_list_stretch = new_forearm_twist_list[0:n_twit_forearm-1]
            for forearm_twist_joints in new_forearm_twist_list_stretch:
                cmds.connectAttr("{}.outputX".format(forearm_lengthbyglobal_div),"{}.scaleX".format(forearm_twist_joints)) 
        
            # 6.7.9 Conectar el pinElbow 
            pinelbow_byik_mult = cmds.createNode("multiplyDivide",n="pinElbowByIk_{}_mult_{}".format(side_a,number_a_l))
            cmds.connectAttr("{}.pinElbow".format(arm_pole_ctr),"{}.input1X".format(pinelbow_byik_mult))
            cmds.connectAttr("{}.armIK".format(arm_settings_ctr),"{}.input2X".format(pinelbow_byik_mult))
            cmds.connectAttr("{}.outputX".format(pinelbow_byik_mult),"{}.blender".format(arm_ikstretch_blend))
            cmds.connectAttr("{}.outputX".format(pinelbow_byik_mult),"{}.input2D[2].input2Dx".format(handik_autostretch_override_sum))
            
            # 6.7.10 Reposicionar el elbowStretchLoc en el ctrArmPole
            arm_pole_pos = cmds.xform(arm_pole_ctr,q=True,t=True,ws=True)
            cmds.xform(stretch_elbow_loc,t=arm_pole_pos,ws=True)
        
            # 6.7.11 Configuracion del autoSquash
            shoulder_lengthbyglobal_inv_div = cmds.createNode("multiplyDivide",n="shoulderLengthByGlobalInv_{}_div_{}".format(side_a,number_a_l))
            cmds.setAttr("{}.operation".format(shoulder_lengthbyglobal_inv_div),2)
            cmds.connectAttr("{}.outputX".format(shoulder_lengthbyglobal_div),"{}.input2X".format(shoulder_lengthbyglobal_inv_div))
            cmds.setAttr("{}.input1X".format(shoulder_lengthbyglobal_inv_div),1)
            
            forearm_lengthbyglobal_inv_div = cmds.createNode("multiplyDivide",n="forearmLengthByGlobalInv_{}_div_{}".format(side_a,number_a_l))
            cmds.setAttr("{}.operation".format(forearm_lengthbyglobal_inv_div),2)
            cmds.connectAttr("{}.outputX".format(forearm_lengthbyglobal_div),"{}.input2X".format(forearm_lengthbyglobal_inv_div))
            cmds.setAttr("{}.input1X".format(forearm_lengthbyglobal_inv_div),1)
            
            
            arm_autosquash_blend =cmds.createNode("blendColors",n="armAutoSquash_{}_blend_{}".format(side_a,number_a_l))
            cmds.connectAttr( "{}.autoSquash".format(arm_settings_ctr),"{}.blender".format(arm_autosquash_blend))
            cmds.connectAttr("{}.outputX".format(shoulder_lengthbyglobal_inv_div),"{}.color1R".format(arm_autosquash_blend))
            cmds.connectAttr("{}.outputX".format(forearm_lengthbyglobal_inv_div),"{}.color1B".format(arm_autosquash_blend))
            cmds.setAttr("{}.color2R".format(arm_autosquash_blend),1)
            cmds.setAttr("{}.color2B".format(arm_autosquash_blend),1)
            for joints in new_shoulder_twist_list:
                cmds.connectAttr("{}.outputR".format(arm_autosquash_blend),"{}.scaleY".format(joints))
                cmds.connectAttr("{}.outputR".format(arm_autosquash_blend),"{}.scaleZ".format(joints))
            for joints in new_forearm_twist_list:
                cmds.connectAttr("{}.outputB".format(arm_autosquash_blend),"{}.scaleY".format(joints))
                cmds.connectAttr("{}.outputB".format(arm_autosquash_blend),"{}.scaleZ".format(joints))
        
            # 6.8 Creacion de sistema bend
            # 6.8.1 Reconstruccion de curvas
            shoulder_twist_crv = cmds.rebuildCurve(shoulder_twist_crv,ch=1,rpo=1,rt=0,end=1,kr=0,kcp=0,kep=1,kt=0,s=1,d=3,tol=0.01)[0]
            forearm_twist_crv = cmds.rebuildCurve(forearm_twist_crv,ch=1,rpo=1,rt=0,end=1,kr=0,kcp=0,kep=1,kt=0,s=1,d=3,tol=0.01)[0]
            
            # 6.8.2 Creacion de clusters
            armbend_cluster_a =cmds.cluster("{}.cv[0]".format(shoulder_twist_crv),n="armBendA_{}_cl_{}".format(side_a,number_a_l))[1]
            armbend_cluster_b =cmds.cluster("{}.cv[1:2]".format(shoulder_twist_crv),n="armBendB_{}_cl_{}".format(side_a,number_a_l))[1]
            armbend_cluster_c =cmds.cluster("{}.cv[3]".format(shoulder_twist_crv),"{}.cv[0]".format(forearm_twist_crv),n="armBendC_{}_cl_{}".format(side_a,number_a_l))[1]
            armbend_cluster_d =cmds.cluster("{}.cv[1:2]".format(forearm_twist_crv),n="armBendD_{}_cl_{}".format(side_a,number_a_l))[1]
            armbend_cluster_e =cmds.cluster("{}.cv[3]".format(forearm_twist_crv),n="armBendE_{}_cl_{}".format(side_a,number_a_l))[1]        
        
            # 6.8.3 Creacion de controles Bend
            cmds.parent(armbend_cluster_a,shoulder_jnt)
            cmds.parent(armbend_cluster_e,elbow_jnt)
            
            uparm_bend_ctr = cmds.duplicate("uparmBend_{}_ctr_0".format(side_a),n="uparmBend_{}_ctr_{}".format(side_a,number_a_l))[0]
            uparm_bend_offset = CreateOffset(uparm_bend_ctr,number_a_l)
            cmds.matchTransform(uparm_bend_offset,armbend_cluster_b,pos=True,rot=False,scl=True)
            cmds.parent(armbend_cluster_b,uparm_bend_ctr)
            cmds.parent(uparm_bend_offset,shoulder_jnt)
            
            elbow_bend_ctr = cmds.duplicate("elbowBend_{}_ctr_0".format(side_a),n="elbowBend_{}_ctr_{}".format(side_a,number_a_l))[0]
            elbow_bend_offset = CreateOffset(elbow_bend_ctr,number_a_l)
            cmds.matchTransform(elbow_bend_offset,armbend_cluster_c,pos=True,rot=False,scl=True)
            cmds.parent(armbend_cluster_c,elbow_bend_ctr)
            cmds.parent(elbow_bend_offset,char_skeleton)
            
            forearm_bend_ctr = cmds.duplicate("forearmBend_{}_ctr_0".format(side_a),n="forearmBend_{}_ctr_{}".format(side_a,number_a_l))[0]
            forearm_bend_offset = CreateOffset(forearm_bend_ctr,number_a_l)
            cmds.matchTransform(forearm_bend_offset,armbend_cluster_d,pos=True,rot=False,scl=True)
            cmds.parent(armbend_cluster_d,forearm_bend_ctr)
            cmds.parent(forearm_bend_offset,elbow_jnt)
            # 6.8.4 Creacion de las relaciones entre los controles y los huesos
            cmds.parentConstraint(elbow_jnt,elbow_bend_offset,n="shoulderElbowBendParent_{}_cns_{}".format(side_a,number_a_l))                                              
            if arm_cl_conexion_check is True:
                # 6.9 Conexiones entre modulos(clavicle)
                # 6.9.1 Constraints
                cmds.parentConstraint("clavicle_{}_skn_{}".format(side_a,arm_cl_conexion),"shoulderRollSystem_{}_grp_{}".format(side_a,number_a_l),mo=True,n="clavicleShoulderRollParent_{}_cns_{}".format(side_a,number_a_l))
                cmds.pointConstraint("clavicleEnd_{}_jnt_{}".format(side_a,arm_cl_conexion),shoulder_offset,mo=False,n="clavicleEndShoulderJntOffsetPoint_{}_cns_{}".format(side_a,number_a_l)) 
                
                #6.9.2 Configuracion del shoulderFKPCon
                shoulderfk_pcon = cmds.duplicate(shoulder_fk_offset,n="shoulderFk_{}_pcon_{}".format(side_a,number_a_l),po=True)[0]
                cmds.parent(shoulderfk_pcon,"clavicleEnd_{}_jnt_{}".format(side_a,arm_cl_conexion))
                cmds.pointConstraint(shoulderfk_pcon,shoulder_fk_offset,mo=True,n="shoulderPcontoOffsetfkPoint_{}_cns_{}".format(side_a,number_a_l))
            spine_spaces_check = win.checkBoxArmSpineSpaces.isChecked()
            spine_arm_conexion_value = win.spinArmConexion.value()
            head_arm_conexion_value = win.spinHeadArmSpaces.value()
            if spine_spaces_check is True:
                # 6.10 Configuracion de los spaces
                # 6.10.1 Configuracion de los spaces en ctrShoulderFK(chestSpace)
                cmds.addAttr(shoulder_fk_ctr,ln= "__", at="enum",en="spaces")
                cmds.setAttr ("{}.__".format(shoulder_fk_ctr),channelBox= True)
                cmds.addAttr(shoulder_fk_ctr,ln= "chestSpace",at= "double",min= 0,max=1,dv=0,k=True)
                
                shoulderfk_worldspace = cmds.duplicate(shoulder_fk_offset,n="shoulderFKworldSpace_{}_grp_{}".format(side_a,number_a_l),po=True)[0]
                shoulderfk_chestSpace = cmds.duplicate(shoulder_fk_offset,n="shoulderFKchestSpace_{}_grp_{}".format(side_a,number_a_l),po=True)[0]
                shoulder_spaces_orient_cns = cmds.orientConstraint(shoulderfk_worldspace,shoulderfk_chestSpace,shoulder_fk_offset,mo=False,n="shoulderSpacesOrient_{}_cns_{}".format(side_a,number_a_l))[0]
                cmds.parent(shoulderfk_chestSpace,"chest_c_ctr_{}".format(spine_arm_conexion_value))
                
                cmds.connectAttr("{}.chestSpace".format(shoulder_fk_ctr),"{}.{}W1".format(shoulder_spaces_orient_cns,shoulderfk_chestSpace))
                shoulder_dynparent_rev = cmds.createNode("reverse",n="shoulderFkDynParent_{}_rev_{}".format(side_a,number_a_l))
                cmds.connectAttr("{}.chestSpace".format(shoulder_fk_ctr),"{}.inputX".format(shoulder_dynparent_rev))
                cmds.connectAttr("{}.outputX".format(shoulder_dynparent_rev),"{}.{}W0".format(shoulder_spaces_orient_cns,shoulderfk_worldspace))
                
                # 6.10.2 Configuracion de los spaces en ctrHandIk
                cmds.addAttr(hand_ik_ctr,ln= "__", at="enum",en="spaces")
                cmds.setAttr ("{}.__".format(hand_ik_ctr),channelBox= True)
                cmds.addAttr(hand_ik_ctr,ln= "headSpace",at= "double",min= 0,max=1,dv=0,k=True)
                cmds.addAttr(hand_ik_ctr,ln= "chestSpace",at= "double",min= 0,max=1,dv=0,k=True)
                cmds.addAttr(hand_ik_ctr,ln= "pelvisSpace",at= "double",min= 0,max=1,dv=0,k=True)
                
                handik_worldspace = cmds.duplicate(hand_ik_offset,n="handIkWorldSpace_{}_grp_{}".format(side_a,number_a_l),po=True)[0]
                handik_headspace = cmds.duplicate(hand_ik_offset,n="handIkHeadSpace_{}_grp_{}".format(side_a,number_a_l),po=True)[0]
                handik_chestspace = cmds.duplicate(hand_ik_offset,n="handIkChestSpace_{}_grp_{}".format(side_a,number_a_l),po=True)[0]
                handik_pelvisspace = cmds.duplicate(hand_ik_offset,n="handIkPelvisSpace_{}_grp_{}".format(side_a,number_a_l),po=True)[0]
                
                hand_spaces_parent_cns = cmds.parentConstraint(handik_worldspace,
                                                               handik_headspace,
                                                               handik_chestspace,
                                                               handik_pelvisspace,
                                                               hand_ik_offset,
                                                               mo=False,
                                                               n="handIkSpacesParent_{}_cns".format(side_a))[0]
                cmds.parent(handik_headspace,"head_c_ctr_{}".format(head_arm_conexion_value))
                cmds.parent(handik_chestspace,"chest_c_ctr_{}".format(spine_arm_conexion_value))
                cmds.parent(handik_pelvisspace,"pelvis_c_ctr_{}".format(spine_arm_conexion_value))
                
                cmds.connectAttr("{}.headSpace".format(hand_ik_ctr),"{}.{}W1".format(hand_spaces_parent_cns,handik_headspace))
                cmds.connectAttr("{}.chestSpace".format(hand_ik_ctr),"{}.{}W2".format(hand_spaces_parent_cns,handik_chestspace))
                cmds.connectAttr("{}.pelvisSpace".format(hand_ik_ctr),"{}.{}W3".format(hand_spaces_parent_cns,handik_pelvisspace))
                
                handik_dynparent_sum = cmds.createNode("plusMinusAverage",n="handIkDynParent_{}_sum_{}".format(side_a,number_a_l))
                cmds.connectAttr("{}.headSpace".format(hand_ik_ctr),"{}.input2D[0].input2Dx".format(handik_dynparent_sum))
                cmds.connectAttr("{}.chestSpace".format(hand_ik_ctr),"{}.input2D[1].input2Dx".format(handik_dynparent_sum))
                cmds.connectAttr("{}.pelvisSpace".format(hand_ik_ctr),"{}.input2D[2].input2Dx".format(handik_dynparent_sum))
                
                handik_dynparent_clamp = cmds.createNode("clamp",n="handIkDynParent_{}_clamp_{}".format(side_a,number_a_l))
                cmds.setAttr("{}.maxR".format(handik_dynparent_clamp),1)
                cmds.connectAttr("{}.output2Dx".format(handik_dynparent_sum),"{}.inputR".format(handik_dynparent_clamp))
                
                handik_dynparent_rev = cmds.createNode("reverse",n="handIkDynParent_{}_rev_{}".format(side_a,number_a_l))
                cmds.connectAttr("{}.outputR".format(handik_dynparent_clamp),"{}.inputX".format(handik_dynparent_rev))
                cmds.connectAttr("{}.outputX".format(handik_dynparent_rev),"{}.{}W0".format(hand_spaces_parent_cns,handik_worldspace))
                # 6.10.3 Configuracion de los spaces en el ctrArmPole
                cmds.addAttr(arm_pole_ctr,ln= "__", at="enum",en="spaces")
                cmds.setAttr ("{}.__".format(arm_pole_ctr),channelBox= True)
                cmds.addAttr(arm_pole_ctr,ln= "handSpace",at= "double",min= 0,max=1,dv=0,k=True)
                cmds.addAttr(arm_pole_ctr,ln= "chestSpace",at= "double",min= 0,max=1,dv=0,k=True)
                arm_pole_worldspace = cmds.duplicate(arm_pole_offset,n="armPoleWorldSpace_{}_grp_{}".format(side_a,number_a_l),po=True)[0]
                arm_pole_handspace = cmds.duplicate(arm_pole_offset,n="armPoleHandSpace_{}_grp_{}".format(side_a,number_a_l),po=True)[0]
                arm_pole_chestspace = cmds.duplicate(arm_pole_offset,n="armPoleChestSpace_{}_grp_{}".format(side_a,number_a_l),po=True)[0]
                
                armpole_spaces_parent_cns = cmds.parentConstraint(arm_pole_worldspace,arm_pole_handspace,arm_pole_chestspace,arm_pole_offset,mo=False,n="armPoleSpacesParent_{}_cns_{}".format(side_a,number_a_l))[0]
                
                cmds.parent(arm_pole_handspace,"handIK_{}_ctr_{}".format(side_a,number_a_l))
                cmds.parent(arm_pole_chestspace,"chest_c_ctr_{}".format(spine_arm_conexion_value))
                
                cmds.connectAttr("{}.handSpace".format(arm_pole_ctr),"{}.{}W1".format(armpole_spaces_parent_cns,arm_pole_handspace))
                cmds.connectAttr("{}.chestSpace".format(arm_pole_ctr),"{}.{}W2".format(armpole_spaces_parent_cns,arm_pole_chestspace))
                
                armpole_dynparent_sum = cmds.createNode("plusMinusAverage",n="armPoleDynParent_{}_sum_{}".format(side_a,number_a_l))
                cmds.connectAttr("{}.handSpace".format(arm_pole_ctr),"{}.input2D[0].input2Dx".format(armpole_dynparent_sum))
                cmds.connectAttr("{}.chestSpace".format(arm_pole_ctr),"{}.input2D[1].input2Dx".format(armpole_dynparent_sum))
                
                armpole_dynparent_clamp = cmds.createNode("clamp",n="armPoleDynParent_{}_clamp_{}".format(side_a,number_a_l))
                cmds.setAttr("{}.maxR".format(armpole_dynparent_clamp),1)
                cmds.connectAttr("{}.output2Dx".format(armpole_dynparent_sum),"{}.inputR".format(armpole_dynparent_clamp))
                
                armpole_dynparent_rev = cmds.createNode("reverse",n="armPoleDynParent_{}_rev_{}".format(side_a,number_a_l))
                cmds.connectAttr("{}.outputR".format(armpole_dynparent_clamp),"{}.inputX".format(armpole_dynparent_rev))
                cmds.connectAttr("{}.outputX".format(armpole_dynparent_rev),"{}.{}W0".format(armpole_spaces_parent_cns,arm_pole_worldspace))
            
            # Cerrar rig
            cmds.connectAttr("{}.visBends".format(arm_settings_ctr),"{}.visibility".format(uparm_bend_ctr))
            cmds.connectAttr("{}.visBends".format(arm_settings_ctr),"{}.visibility".format(elbow_bend_ctr))
            cmds.connectAttr("{}.visBends".format(arm_settings_ctr),"{}.visibility".format(forearm_bend_ctr))
            Hide("shoulderNonRoll_{}_grp_{}".format(side_a,number_a_l))
            Hide(shoulder_twist_ik)
            Hide("forearmRollSystem_{}_grp_{}".format(side_a,number_a_l))
            Hide(arm_main_ik)
            Hide(shoulder_twist_crv)
            Hide(forearm_twist_crv)
            Hide(stretch_shoulder_loc)
            Hide(stretch_elbow_loc)
            Hide(stretch_hand_loc)
            Hide(armbend_cluster_a)
            Hide(armbend_cluster_b)
            Hide(armbend_cluster_c)
            Hide(armbend_cluster_d)
            Hide(armbend_cluster_e)
            last_shoulder_twist_jnt = cmds.rename(last_shoulder_twist_jnt,"{}_{}_jnt_{}".format(last_shoulder_twist_jnt.split("_")[0],side_a,number_a_l))
            last_forearm_twist_jnt =  cmds.rename(last_forearm_twist_jnt,"{}_{}_jnt_{}".format(last_forearm_twist_jnt.split("_")[0],side_a,number_a_l))
            LockScaleVis(hand_ik_ctr)
            LockScaleRotVis(arm_pole_ctr)
            LockScaleRotVis(uparm_bend_ctr)
            LockScaleRotVis(elbow_bend_ctr)
            LockScaleRotVis(forearm_bend_ctr)
            LockScaleTransVis(shoulder_fk_ctr)
            LockScaleTransVis(elbow_fk_ctr)
            LockScaleTransVis(hand_fk_ctr)
            LockAll(arm_settings_ctr)
            createArmSnap(number_a_l,side_a)   
                       
        win.armLeftButton.clicked.connect(BuildLeftArm)
        
        def BuildRightArm():
            number_uparm_joints = win.spinBoxUparmNumberJoints.value()
            number_forearm_joints = win.spinBoxForearmNumberJoints.value()
            side_a = "r"
            shoulder = "shoulder_{}_loc_{}".format(side_a,number_a_r)
            elbow = "elbow_{}_loc_{}".format(side_a,number_a_r)
            hand = "hand_{}_loc_{}".format(side_a,number_a_r)
            hand_end = "handEnd_{}_loc_{}".format(side_a,number_a_r)
            shoulder_roll_r_system = cmds.group(n="shoulderRollSystem_r_grp_{}".format(number_a_r),em=1,p=arm_r_rig)
            shoulder_non_roll_r = cmds.group(n="shoulderNonRoll_r_grp_{}".format(number_a_r),em=1,p=shoulder_roll_r_system)
            forearm_roll_r_system = cmds.group(n="forearmRollSystem_r_grp_{}".format(number_a_r),em=1,p=arm_r_rig)
            elbow_non_roll_r = cmds.group(n="elbowNonRoll_r_grp_{}".format(number_a_r),em=1,p=forearm_roll_r_system)
            hand_non_roll_r = cmds.group(n="handNonRoll_r_grp_{}".format(number_a_r),em=1,p=forearm_roll_r_system)
            for axis in "XYZ":
                cmds.connectAttr("{}.globalScale".format(control_base),"{}.scale{}".format(shoulder_roll_r_system,axis))
            # 6.1 Creacion de los huesos y reorientacion de locators
            del_cons = cmds.aimConstraint(elbow,
                                            shoulder,
                                            offset=(0,0,0),
                                            weight=1,
                                            aimVector=(1,0,0),
                                            upVector=(0,1,0),
                                            worldUpType="scene")[0]
            cmds.delete(del_cons)
            del_cons = cmds.aimConstraint(hand,
                                          elbow,
                                          offset=(0,0,0),
                                          weight=1,
                                          aimVector=(1,0,0),
                                          upVector=(0,1,0),
                                          worldUpType="scene")[0]
            cmds.delete(del_cons)
            del_cons = cmds.aimConstraint(hand_end,
                                          hand,
                                          offset=(0,0,0),
                                          weight=1,
                                          aimVector=(1,0,0),
                                          upVector=(0,1,0),
                                          worldUpType="scene")[0]
            cmds.delete(del_cons)
            del_cons = cmds.aimConstraint(hand,
                                          hand_end,
                                          offset=(0,0,0),
                                          weight=1,
                                          aimVector=(-1,0,0),
                                          upVector=(0,1,0),
                                          worldUpType="scene")[0]
            cmds.delete(del_cons)
            cmds.select(cl=1)
            shoulder_jnt = cmds.joint(n="shoulder_{}_jnt_{}".format(side_a,number_a_r))
            cmds.matchTransform(shoulder_jnt,shoulder,pos=True,rot=False,scl=True)
            for axis in "XYZ":
                shoulder_rotate = cmds.getAttr("{}.rotate{}".format(shoulder,axis))
                cmds.setAttr("{}.rotate{}".format(shoulder,axis),0)
                cmds.setAttr("{}.jointOrient{}".format(shoulder_jnt,axis),shoulder_rotate)
            
            cmds.select(cl=1)
            elbow_jnt = cmds.joint(n="elbow_{}_jnt_{}".format(side_a,number_a_r))
            cmds.matchTransform(elbow_jnt,elbow,pos=True,rot=False,scl=True)
            for axis in "XYZ":
                elbow_rotate = cmds.getAttr("{}.rotate{}".format(elbow,axis))
                cmds.setAttr("{}.rotate{}".format(elbow,axis),0)
                cmds.setAttr("{}.jointOrient{}".format(elbow_jnt,axis),elbow_rotate)
            cmds.parent(elbow_jnt,shoulder_jnt)
            
            cmds.select(cl=1)
            arm_end_jnt = cmds.joint(n="armEnd_{}_jnt_{}".format(side_a,number_a_r))
            cmds.matchTransform(arm_end_jnt,hand,pos=True,rot=False,scl=True)
            for axis in "XYZ":
                arm_end_rotate = cmds.getAttr("{}.rotate{}".format(hand,axis))
                cmds.setAttr("{}.jointOrient{}".format(arm_end_jnt,axis),arm_end_rotate)
            cmds.parent(arm_end_jnt,elbow_jnt)
            
            cmds.select(cl=1)
            hand_jnt = cmds.joint(n="hand_{}_skn_{}".format(side_a,number_a_r))
            cmds.matchTransform(hand_jnt,hand,pos=True,rot=False,scl=True)
            for axis in "XYZ":
                hand_rotate = cmds.getAttr("{}.rotate{}".format(hand,axis))
                cmds.setAttr("{}.rotate{}".format(hand,axis),0)
                cmds.setAttr("{}.jointOrient{}".format(hand_jnt,axis),hand_rotate)
            
            cmds.select(cl=1)
            hand_end_jnt = cmds.joint(n="handEnd_{}_jnt_{}".format(side_a,number_a_r))
            hand_end_pos = cmds.xform(hand_end,q=True,matrix=True,ws=True)
            cmds.matchTransform(hand_end_jnt,hand_end,pos=True,rot=False,scl=True)
            for axis in "XYZ":
                hand_end_rotate = cmds.getAttr("{}.rotate{}".format(hand_end,axis))
                cmds.setAttr("{}.rotate{}".format(hand_end,axis),0)
                cmds.setAttr("{}.jointOrient{}".format(hand_end_jnt,axis),hand_end_rotate)
            cmds.parent(hand_end_jnt,hand_jnt)
            
            shoulder_offset = CreateOffset(shoulder_jnt,number_a_r)
            cmds.parent(shoulder_offset,char_skeleton)
            
            
            if "l" in side_a:
                cmds.setAttr("{}.preferredAngleY".format(elbow_jnt),-90)
            if "r" in side_a:
                cmds.setAttr("{}.preferredAngleY".format(elbow_jnt),90)
                
            hand_offset = CreateOffset(hand_jnt,number_a_r)
            cmds.parent(hand_offset,char_skeleton)
            cmds.pointConstraint(arm_end_jnt,hand_offset,mo=False,n="armEndPoint_{}_cns_{}".format(side_a,number_a_r))
            # 6.2 Creacion del Ik Handle del la cadena principal
            arm_main_ik = cmds.ikHandle( sj=shoulder_jnt, ee=arm_end_jnt, s="sticky",n="armMainikHandle_{}_ik_{}".format(side_a,number_a_r),sol="ikRPsolver")[0]
            for axis in "XYZ":
                cmds.setAttr("{}.poleVector{}".format(arm_main_ik,axis),0)
            if "l" in side_a:
                cmds.parent(arm_main_ik,arm_l_rig)
            if "r" in side_a:
                cmds.parent(arm_main_ik,arm_r_rig)
        
            # 6.3.1 Configuracion de la cadena NonRoll de shoulder
            shoulder_non_roll = cmds.duplicate(shoulder_jnt,po=True,n="shoulderNonRoll_{}_jnt_{}".format(side_a,number_a_r))[0]
            shoulder_end_non_roll = cmds.duplicate(elbow_jnt,po=True,n="shoulderEndNonRoll_{}_jnt_{}".format(side_a,number_a_r))[0]
            cmds.parent(shoulder_end_non_roll,shoulder_non_roll)
            
            shoulder_nonroll_ik = cmds.ikHandle( sj=shoulder_non_roll, ee=shoulder_end_non_roll, s="sticky",n="shoulderNonRollikHandle_{}_ik_{}".format(side_a,number_a_r),sol="ikRPsolver")[0]
            for axis in "XYZ":
                cmds.setAttr("{}.poleVector{}".format(shoulder_nonroll_ik,axis),0)
            if "l" in side_a:
                cmds.parent(shoulder_non_roll,shoulder_non_roll_l)
                cmds.parent(shoulder_nonroll_ik,shoulder_non_roll_l)
            if "r" in side_a:
                cmds.parent(shoulder_non_roll,shoulder_non_roll_r)
                cmds.parent(shoulder_nonroll_ik,shoulder_non_roll_r)
            
            cmds.pointConstraint(shoulder_jnt,shoulder_non_roll,mo=False,n="shouldertoNonPoint_{}_cns_{}".format(side_a,number_a_r))
            cmds.pointConstraint(elbow_jnt,shoulder_nonroll_ik,mo=False,n="shoulderEndtiIkPoint_{}_cns_{}".format(side_a,number_a_r))
            
            # 6.3.2 Configuracion de la cadena NonRoll del elbow
            elbow_non_roll = cmds.duplicate(elbow_jnt,po=True,n="elbowNonRoll_{}_jnt_{}".format(side_a,number_a_r))[0]
            elbow_end_non_roll = cmds.duplicate(arm_end_jnt,po=True,n="elbowEndNonRoll_{}_jnt_{}".format(side_a,number_a_r))[0]
            cmds.parent(elbow_end_non_roll,elbow_non_roll)
            
            elbow_nonroll_ik = cmds.ikHandle( sj=elbow_non_roll, ee=elbow_end_non_roll, s="sticky",n="elbowNonRollikHandle_{}_ik_{}".format(side_a,number_a_r),sol="ikRPsolver")[0]
            for axis in "XYZ":
                cmds.setAttr("{}.poleVector{}".format(elbow_nonroll_ik,axis),0)
            if "l" in side_a:
                cmds.parent(elbow_non_roll,elbow_non_roll_l)
                cmds.parent(elbow_nonroll_ik,elbow_non_roll_l)
            if "r" in side_a:
                cmds.parent(elbow_non_roll,elbow_non_roll_r)
                cmds.parent(elbow_nonroll_ik,elbow_non_roll_r)
            
            cmds.pointConstraint(elbow_jnt,elbow_non_roll,mo=False,n="elbowtoNonPoint_{}_cns_{}".format(side_a,number_a_r))
            cmds.pointConstraint(hand_jnt,elbow_nonroll_ik,mo=False,n="handtiIkNonPoint_{}_cns_{}".format(side_a,number_a_r))
            
            elbow_twist_value = cmds.duplicate(elbow_jnt,po=True,n="elbowTwistValue_{}_jnt_{}".format(side_a,number_a_r))[0]
            cmds.parent(elbow_twist_value,elbow_jnt)
            cmds.aimConstraint(hand_jnt,
                                elbow_twist_value,
                                offset=(0,0,0),
                                weight=1,
                                aimVector=(1,0,0),
                                upVector=(0,1,0),
                                worldUpType="objectrotation",
                                worldUpVector=(0,1,0),
                                worldUpObject=elbow_non_roll,
                                n="handtoElbowNonAim_{}_cns_{}".format(side_a,number_a_r))
            
            if "l" in side_a:
                cmds.parentConstraint(shoulder_non_roll,elbow_non_roll_l,mo=True,n="shoulderNontoElbowNonGrpParent_l_cns_{}".format(number_a_r))
            if "r" in side_a:
                cmds.parentConstraint(shoulder_non_roll,elbow_non_roll_r,mo=True,n="shoulderNontoElbowNonGrpParent_r_cns_{}".format(number_a_r))
            
            # 6.3.3 Confuguracion de la cadena Non Roll Hand
            hand_non_roll = cmds.duplicate(hand_jnt,po=True,n="handNonRoll_{}_jnt_{}".format(side_a,number_a_r))[0]
            hand_end_non_roll = cmds.duplicate(hand_end_jnt,po=True,n="handEndNonRoll_{}_jnt_{}".format(side_a,number_a_r))[0]
            cmds.parent(hand_end_non_roll,hand_non_roll)
            
            hand_nonroll_ik = cmds.ikHandle( sj=hand_non_roll, ee=hand_end_non_roll, s="sticky",n="handNonRollikHandle_{}_ik_{}".format(side_a,number_a_r),sol="ikRPsolver")[0]
            for axis in "XYZ":
                cmds.setAttr("{}.poleVector{}".format(hand_nonroll_ik,axis),0)
                
            if "l" in side_a:
                cmds.parent(hand_non_roll,hand_non_roll_l)
                cmds.parent(hand_nonroll_ik,hand_non_roll_l)
            if "r" in side_a:
                cmds.parent(hand_non_roll,hand_non_roll_r)
                cmds.parent(hand_nonroll_ik,hand_non_roll_r)
            
            cmds.pointConstraint(hand_jnt,hand_non_roll)
            cmds.pointConstraint(hand_end_jnt,hand_nonroll_ik)
            
            hand_twist_value = cmds.duplicate(hand_jnt,po=True,n="handTwistValue_{}_jnt_{}".format(side_a,number_a_r))[0]
            cmds.parent(hand_twist_value,hand_jnt)
            cmds.aimConstraint(hand_end_jnt,
                                hand_twist_value,
                                offset=(0,0,0),
                                weight=1,
                                aimVector=(1,0,0),
                                upVector=(0,1,0),
                                worldUpType="objectrotation",
                                worldUpVector=(0,1,0),
                                worldUpObject=hand_non_roll,
                                n="handEndtoHandTwistNonAim_{}_cns_{}".format(side_a,number_a_r))
            
            
            if "l" in side_a:
                cmds.parentConstraint(elbow_jnt,hand_non_roll_l,mo=True,n="elbowtohandNonGrpParent_l_cns_{}".format(number_a_r))
            if "r" in side_a:
                cmds.parentConstraint(elbow_jnt,hand_non_roll_r,mo=True,n="elbowtohandNonGrpParent_r_cns_{}".format(number_a_r))        
        
            # 6.4.1 Creacion de la cadena twist del shoulder
            shoulder_twist_list = JointChain(shoulder,elbow,"shoulderTwist",number_uparm_joints)
            new_shoulder_twist_list=[] 
            for shoulder_twist in shoulder_twist_list:
                shoulder_twist_jnt = cmds.rename(shoulder_twist,"{}_{}_skn_{}".format(shoulder_twist,side_a,number_a_r))
                new_shoulder_twist_list.append(shoulder_twist_jnt)
            first_shoulder_twist_jnt = new_shoulder_twist_list[0]
            cmds.parent(first_shoulder_twist_jnt,"shoulderRollSystem_{}_grp_{}".format(side_a,number_a_r))
            last_shoulder_twist_jnt = new_shoulder_twist_list[-1]
            ikhandle_shoulder_twist_list = cmds.ikHandle(sj=first_shoulder_twist_jnt,
                                                         ee=last_shoulder_twist_jnt,
                                                         sol="ikSplineSolver",
                                                         scv=False,
                                                         pcv=False,
                                                         n="shoulderTwistikHandle_{}_ik_{}".format(side_a,number_a_r))
            shoulder_twist_ik = ikhandle_shoulder_twist_list[0]
            shoulder_twist_crv = ikhandle_shoulder_twist_list[2]
            shoulder_twist_crv = cmds.rename(shoulder_twist_crv,"shoulderTwist_{}_crv_{}".format(side_a,number_a_r))
            cmds.parent(shoulder_twist_ik,"shoulderRollSystem_{}_grp_{}".format(side_a,number_a_r))
            cmds.parent(shoulder_twist_crv,"{}ArmRig_{}_grp".format(name,side_a))
            
            elbow_twist_mult = cmds.createNode("multiplyDivide",n="elbowTwistValue_{}_mult_{}".format(side_a,number_a_r))
            cmds.connectAttr("{}.rotateX".format(elbow_twist_value),"{}.input1X".format(elbow_twist_mult))
            cmds.setAttr("{}.input2X".format(elbow_twist_mult),-1)
            cmds.connectAttr("{}.outputX".format(elbow_twist_mult),"{}.twist".format(shoulder_twist_ik))
        
            # 6.4.2 Creacion de la cadena twist del forearm
            forearm_twist_list = JointChain(elbow,hand,"forearmTwist",number_forearm_joints)
            new_forearm_twist_list=[] 
            for forearm_twist in forearm_twist_list:
                forearm_twist_jnt = cmds.rename(forearm_twist,"{}_{}_skn_{}".format(forearm_twist,side_a,number_a_r))
                new_forearm_twist_list.append(forearm_twist_jnt)
            first_forearm_twist_jnt = new_forearm_twist_list[0]
            cmds.parent(first_forearm_twist_jnt,elbow_jnt)
            last_forearm_twist_jnt = new_forearm_twist_list[-1]
            ikhandle_forearm_twist_list = cmds.ikHandle(sj=first_forearm_twist_jnt,
                                                         ee=last_forearm_twist_jnt,
                                                         sol="ikSplineSolver",
                                                         scv=False,
                                                         pcv=False,
                                                         n="forearmTwistikHandle_{}_ik_{}".format(side_a,number_a_r))
            forearm_twist_ik = ikhandle_forearm_twist_list[0]
            forearm_twist_crv = ikhandle_forearm_twist_list[2]
            forearm_twist_crv = cmds.rename(forearm_twist_crv,"forearmTwist_{}_crv_{}".format(side_a,number_a_r))
            cmds.parent(forearm_twist_ik,"forearmRollSystem_{}_grp_{}".format(side_a,number_a_r))
            cmds.parent(forearm_twist_crv,"{}ArmRig_{}_grp".format(name,side_a))
            forearm_twist_mult = cmds.createNode("multiplyDivide",n="forearmTwistValue_{}_mult_{}".format(side_a,number_a_r))
            cmds.connectAttr("{}.rotateX".format(hand_twist_value),"{}.input1X".format(forearm_twist_mult))
            cmds.setAttr("{}.input2X".format(forearm_twist_mult),-1)
            cmds.connectAttr("{}.outputX".format(forearm_twist_mult),"{}.twist".format(forearm_twist_ik))    
        
            #6.5.1 Creacion del control HandIK
            hand_ik_ctr = cmds.duplicate("handIK_{}_ctr_0".format(side_a),n="handIK_{}_ctr_{}".format(side_a,number_a_r))[0]
            hand_ik_offset = CreateOffset(hand_ik_ctr,number_a_r)
            hand_pos = cmds.xform(hand_jnt,q=True,matrix=True,ws=True)
            cmds.xform(hand_ik_offset,matrix=hand_pos,ws=True)
            cmds.parent(hand_ik_offset,control_center)
            
            AttrSeparator(hand_ik_ctr)    
            cmds.addAttr(hand_ik_ctr,ln= "elbow",at= "double",dv=1,k=True)
            cmds.addAttr(hand_ik_ctr,ln= "autoStretch",at= "double",max=1,min=0,dv=1,k=True)
        
            # 6.5.2 Creacion del control armPole
            arm_pole_ctr = cmds.duplicate("armPole_{}_ctr_0".format(side_a),n="armPole_{}_ctr_{}".format(side_a,number_a_r))[0]
            arm_pole_offset = CreateOffset(arm_pole_ctr,number_a_r)
            pole_loc = PoleVector(sel=[shoulder_jnt,elbow_jnt,arm_end_jnt],side=side_a)
            pole_desplace_distance = cmds.getAttr("{}.translateX".format(elbow_jnt))
            pole_loc_child = cmds.duplicate(pole_loc,n="PoleVectorChild_{}_loc_{}".format(side_a,number_a_r))[0]
            cmds.parent(pole_loc_child,pole_loc)
            cmds.setAttr("{}.translateX".format(pole_loc_child),pole_desplace_distance)
            pole_pos = cmds.xform(pole_loc_child,q=True,t=True,ws=True)
            cmds.xform(arm_pole_offset,t=pole_pos,ws=True)
            cmds.parent(arm_pole_offset,control_center)
            cmds.delete(pole_loc)
            
            AttrSeparator(arm_pole_ctr)
            cmds.addAttr(arm_pole_ctr,ln= "pinElbow",at= "double",max=1,min=0,dv=0,k=True)
        
            #6.5.3 Creacion del control armSettings
            arm_settings_ctr = cmds.duplicate("armSettings_{}_ctr_0".format(side_a),n="armSettings_{}_ctr_{}".format(side_a,number_a_r))[0]
            arm_settings_offset = CreateOffset(arm_settings_ctr,number_a_r)
            cmds.xform(arm_settings_offset,matrix=hand_pos,ws=True)
            arm_settings_desplace_distance = cmds.getAttr("{}.translateX".format(hand_end_jnt))
            refresh_pos_arm_set = cmds.getAttr("{}.translateX".format(arm_settings_offset))
            cmds.setAttr("{}.translateX".format(arm_settings_offset),refresh_pos_arm_set+arm_settings_desplace_distance+arm_settings_desplace_distance)
            cmds.parent(arm_settings_offset,control_center)
            
            AttrSeparator(arm_settings_ctr)
            cmds.addAttr(arm_settings_ctr,ln= "armIK",at= "double",max=1,min=0,dv=0,k=True)
            cmds.addAttr(arm_settings_ctr,ln= "autoSquash",at= "double",max=1,min=0,dv=0,k=True)
            cmds.addAttr(arm_settings_ctr,ln= "visBends",at= "double",max=1,min=0,dv=1,k=True)
            cmds.addAttr(arm_settings_ctr,ln= "visFingers",at= "double",max=1,min=0,dv=1,k=True)
        
            #6.5.4 Creacion del control shoulderFK
            shoulder_fk_ctr = cmds.duplicate("shoulderFK_{}_ctr_0".format(side_a),n="shoulderFK_{}_ctr_{}".format(side_a,number_a_r))[0]
            shoulder_fk_offset = CreateOffset(shoulder_fk_ctr,number_a_r)
            shoulder_pos = cmds.xform(shoulder_jnt,q=True,matrix=True,ws=True)
            cmds.xform(shoulder_fk_offset,matrix=shoulder_pos,ws=True)
            cmds.parent(shoulder_fk_offset,"center_c_ctr_1")
            
            AttrSeparator(shoulder_fk_ctr)
            cmds.addAttr(shoulder_fk_ctr,ln= "stretch",at= "double",dv=1,k=True)
            
            #6.5.5 Creacion del control elbowFK
            elbow_fk_ctr = cmds.duplicate("elbowFK_{}_ctr_0".format(side_a),n="elbowFK_{}_ctr_{}".format(side_a,number_a_r))[0]
            elbow_fk_offset = CreateOffset(elbow_fk_ctr,number_a_r)
            elbow_pos = cmds.xform(elbow_jnt,q=True,matrix=True,ws=True)
            cmds.xform(elbow_fk_offset,matrix=elbow_pos,ws=True)
            cmds.parent(elbow_fk_offset,shoulder_fk_ctr)
            
            AttrSeparator(elbow_fk_ctr)
            cmds.addAttr(elbow_fk_ctr,ln= "stretch",at= "double",dv=1,k=True)
            
            #6.5.6 Creacion del control handFK
            hand_fk_ctr = cmds.duplicate("handFK_{}_ctr_0".format(side_a),n="handFK_{}_ctr_{}".format(side_a,number_a_r))[0]
            hand_fk_offset = CreateOffset(hand_fk_ctr,number_a_r)
            hand_pos = cmds.xform(hand_jnt,q=True,matrix=True,ws=True)
            cmds.xform(hand_fk_offset,matrix=hand_pos,ws=True)
            cmds.parent(hand_fk_offset,elbow_fk_ctr)
        
            #6.6.1 Creacion de los joints PAC
            shoulder_pac = cmds.duplicate(shoulder_jnt,n="shoulderPAC_{}_jnt_{}".format(side_a,number_a_r),po=True)[0]
            cmds.parent(shoulder_pac,shoulder_fk_ctr)
            
            elbow_pac = cmds.duplicate(elbow_jnt,n="elbowPAC_{}_jnt_{}".format(side_a,number_a_r),po=True)[0]
            cmds.parent(elbow_pac,elbow_fk_ctr)
            
            hand_fk_pac = cmds.duplicate(hand_jnt,n="handFkPAC_{}_jnt_{}".format(side_a,number_a_r),po=True)[0]
            cmds.parent(hand_fk_pac,hand_fk_ctr)
            
            hand_ik_pac = cmds.duplicate(hand_jnt,n="handIkPAC_{}_jnt_{}".format(side_a,number_a_r),po=True)[0]
            cmds.parent(hand_ik_pac,hand_ik_ctr)
           
           #6.6.2 Relaciones basicas entre controles, huesos e ikHandles
            cmds.pointConstraint(hand_ik_pac,arm_main_ik,n="PacIkHandPoint_{}_cns_{}".format(side_a,number_a_r))
            cmds.poleVectorConstraint(arm_pole_ctr,arm_main_ik,w=1,n="PoleIkPole_{}_cns_{}".format(side_a,number_a_r))
            orient_shoulder_cns = cmds.orientConstraint(shoulder_pac,shoulder_jnt,mo=False,n="PacShoulderOrient_{}_cns_{}".format(side_a,number_a_r))[0]
            cmds.cycleCheck(e=False)
            orient_elbow_cns = cmds.orientConstraint(elbow_pac,elbow_jnt,mo=False,n="PacElbowOrient_{}_cns_{}".format(side_a,number_a_r))[0]
            cmds.parentConstraint(hand_jnt,arm_settings_offset,mo=True,n="handSettingsParent_{}_cns_{}".format(side_a,number_a_r))
            orient_hand_cns = cmds.orientConstraint(hand_fk_pac,hand_ik_pac,hand_jnt,n="HandPACFkIkOrient_{}_cns_{}".format(side_a,number_a_r))[0]
        
            #6.6.3 Conexiones para realizar el switch FK/IK
            cmds.connectAttr("{}.armIK".format(arm_settings_ctr),"{}.ikBlend".format(arm_main_ik))
            cmds.connectAttr("{}.armIK".format(arm_settings_ctr),"{}.{}W1".format(orient_hand_cns,hand_ik_pac))
            reverse_switch_armik = cmds.createNode("reverse",n="armIk_{}_rev_{}".format(side_a,number_a_r))
            cmds.connectAttr("{}.armIK".format(arm_settings_ctr),"{}.inputX".format(reverse_switch_armik))
            cmds.connectAttr("{}.outputX".format(reverse_switch_armik),"{}.{}W0".format(orient_hand_cns,hand_fk_pac))
            cmds.connectAttr("{}.outputX".format(reverse_switch_armik),"{}.{}W0".format(orient_elbow_cns,elbow_pac))
            cmds.cycleCheck(e=True)
            cmds.connectAttr("{}.outputX".format(reverse_switch_armik),"{}.{}W0".format(orient_shoulder_cns,shoulder_pac))
            cmds.connectAttr("{}.armIK".format(arm_settings_ctr),"{}.visibility".format(hand_ik_offset))
            cmds.connectAttr("{}.armIK".format(arm_settings_ctr),"{}.visibility".format(arm_pole_offset))
            cmds.connectAttr("{}.outputX".format(reverse_switch_armik),"{}.visibility".format(shoulder_fk_offset))
            
            #6.6.4 Otras conexiones
            cmds.connectAttr("{}.elbow".format(hand_ik_ctr),"{}.twist".format(arm_main_ik))
            
            # 6.7 Configuracion del Squash/Stretch
            # 6.7.1 Creacion de locators para medir las distancias
            stretch_shoulder_loc = cmds.spaceLocator(n="stretchShoulder_{}_loc_{}".format(side_a,number_a_r))[0]
            stretch_elbow_loc = cmds.spaceLocator(n="stretchElbow_{}_loc_{}".format(side_a,number_a_r))[0]
            stretch_hand_loc = cmds.spaceLocator(n="stretchHand_{}_loc_{}".format(side_a,number_a_r))[0]
            shoulder_t = cmds.xform(shoulder_jnt,q=True,t=True,ws=True)
            elbow_t = cmds.xform(elbow_jnt,q=True,t=True,ws=True)
            hand_t = cmds.xform(hand_jnt,q=True,t=True,ws=True)
            cmds.xform(stretch_shoulder_loc,t=shoulder_t,ws=True)
            cmds.xform(stretch_elbow_loc,t=elbow_t,ws=True)
            cmds.xform(stretch_hand_loc,t=hand_t,ws=True)
            arm_cl_conexion_check = win.checkBoxArmClavicleConexion.isChecked()
            arm_cl_conexion = win.spinArmClavicleConexion.value()
            if arm_cl_conexion_check is True:
                cmds.parent(stretch_shoulder_loc,"clavicleEnd_{}_jnt_{}".format(side_a,arm_cl_conexion))
            else:
                cmds.parent(stretch_shoulder_loc,shoulder_fk_ctr)
            cmds.parent(stretch_elbow_loc, arm_pole_ctr)
            cmds.parent(stretch_hand_loc, hand_ik_ctr)
        
            # 6.7.2 Conectar los locators con nodos distance
            uparm_distance = cmds.createNode("distanceBetween",n="uparm_{}_dist_{}".format(side_a,number_a_r))
            cmds.connectAttr("{}.worldPosition[0]".format(stretch_shoulder_loc),"{}.point1".format(uparm_distance))
            cmds.connectAttr("{}.worldPosition[0]".format(stretch_elbow_loc),"{}.point2".format(uparm_distance))
            lowarm_distance = cmds.createNode("distanceBetween",n="lowarm_{}_dist_{}".format(side_a,number_a_r))
            cmds.connectAttr("{}.worldPosition[0]".format(stretch_elbow_loc),"{}.point1".format(lowarm_distance))
            cmds.connectAttr("{}.worldPosition[0]".format(stretch_hand_loc),"{}.point2".format(lowarm_distance))
            entire_arm_distance = cmds.createNode("distanceBetween",n="entireArm_{}_dist_{}".format(side_a,number_a_r))
            cmds.connectAttr("{}.worldPosition[0]".format(stretch_shoulder_loc),"{}.point1".format(entire_arm_distance))
            cmds.connectAttr("{}.worldPosition[0]".format(stretch_hand_loc),"{}.point2".format(entire_arm_distance))
           
            # 6.7.3 Configurar el stretchIK y normalizarlo
            arm_normal_stretch_div = cmds.createNode("multiplyDivide",n="armNormalStretch_{}_div_{}".format(side_a,number_a_r))
            cmds.setAttr("{}.operation".format(arm_normal_stretch_div),2)
            cmds.connectAttr("{}.distance".format(entire_arm_distance),"{}.input1X".format(arm_normal_stretch_div))
            etire_arm_distance_value = cmds.getAttr("{}.distance".format(entire_arm_distance))
            cmds.setAttr("{}.input2X".format(arm_normal_stretch_div),etire_arm_distance_value)
            
            arm_stretch_clamp = cmds.createNode("clamp",n="armStretch_{}_clamp_{}".format(side_a,number_a_r))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.minR".format(arm_stretch_clamp))
            cmds.setAttr("{}.maxR".format(arm_stretch_clamp),999)
            cmds.connectAttr("{}.outputX".format(arm_normal_stretch_div),"{}.inputR".format(arm_stretch_clamp))
            
            uparm_stretch_div = cmds.createNode("multiplyDivide",n="upArmStretch_{}_div_{}".format(side_a,number_a_r))
            cmds.setAttr("{}.operation".format(uparm_stretch_div),2)
            cmds.connectAttr("{}.distance".format(uparm_distance),"{}.input1X".format(uparm_stretch_div))
            uparm_distance_value = cmds.getAttr("{}.distance".format(uparm_distance))
            cmds.setAttr("{}.input2X".format(uparm_stretch_div),uparm_distance_value)
            
            lowarm_stretch_div = cmds.createNode("multiplyDivide",n="lowArmStretch_{}_div_{}".format(side_a,number_a_r))
            cmds.setAttr("{}.operation".format(lowarm_stretch_div),2)
            cmds.connectAttr("{}.distance".format(lowarm_distance),"{}.input1X".format(lowarm_stretch_div))
            lowarm_distance_value = cmds.getAttr("{}.distance".format(lowarm_distance))
            cmds.setAttr("{}.input2X".format(lowarm_stretch_div),lowarm_distance_value)
            
            arm_ikstretch_blend = cmds.createNode("blendColors",n="armIkStretch_{}_blend_{}".format(side_a,number_a_r))
            cmds.connectAttr("{}.outputX".format(uparm_stretch_div),"{}.color1G".format(arm_ikstretch_blend))
            cmds.connectAttr("{}.outputX".format(lowarm_stretch_div),"{}.color1B".format(arm_ikstretch_blend))
            cmds.connectAttr("{}.outputR".format(arm_stretch_clamp),"{}.color2G".format(arm_ikstretch_blend))
            cmds.connectAttr("{}.outputR".format(arm_stretch_clamp),"{}.color2B".format(arm_ikstretch_blend))
            
            arm_finalstretch_blend = cmds.createNode("blendColors",n= "armFinalStretch_{}_blend_{}".format(side_a,number_a_r))
            cmds.connectAttr("{}.armIK".format(arm_settings_ctr),"{}.blender".format(arm_finalstretch_blend))
            cmds.connectAttr("{}.outputG".format(arm_ikstretch_blend),"{}.color1G".format(arm_finalstretch_blend))            
            cmds.connectAttr("{}.outputB".format(arm_ikstretch_blend),"{}.color1B".format(arm_finalstretch_blend))
            cmds.setAttr("{}.color2G".format(arm_finalstretch_blend),1)
            cmds.setAttr("{}.color2B".format(arm_finalstretch_blend),1)
        
            # 6.7.4 Configurar el autoStretch 
            arm_stretchiness_blend = cmds.createNode("blendColors",n="armStretchiness_{}_blend_{}".format(side_a,number_a_r))
            cmds.connectAttr("{}.outputG".format(arm_finalstretch_blend),"{}.color1G".format(arm_stretchiness_blend))
            cmds.connectAttr("{}.outputB".format(arm_finalstretch_blend),"{}.color1B".format(arm_stretchiness_blend))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.color2G".format(arm_stretchiness_blend))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.color2B".format(arm_stretchiness_blend))
            
            arm_stretch_global_div = cmds.createNode("multiplyDivide",n="armStretchByGlobal_{}_div_{}".format(side_a,number_a_r))
            cmds.setAttr("{}.operation".format(arm_stretch_global_div),2)
            cmds.connectAttr("{}.outputG".format(arm_stretchiness_blend),"{}.input1X".format(arm_stretch_global_div))
            cmds.connectAttr("{}.outputB".format(arm_stretchiness_blend),"{}.input1Y".format(arm_stretch_global_div))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.input2X".format(arm_stretch_global_div))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.input2Y".format(arm_stretch_global_div))
            
            handik_autostretch_override_sum = cmds.createNode("plusMinusAverage",n="handIkAutostretchOverride_{}_sum_{}".format(side_a,number_a_r))
            cmds.connectAttr("{}.outputX".format(reverse_switch_armik),"{}.input2D[0].input2Dx".format(handik_autostretch_override_sum))
            cmds.connectAttr("{}.autoStretch".format(hand_ik_ctr),"{}.input2D[1].input2Dx".format(handik_autostretch_override_sum))
            
            handik_finalstretchiness_clamp = cmds.createNode("clamp",n="handIkFinalStretchiness_{}_clamp_{}".format(side_a,number_a_r))
            cmds.setAttr("{}.maxR".format(handik_finalstretchiness_clamp),1)
            cmds.connectAttr("{}.output2D.output2Dx".format(handik_autostretch_override_sum),"{}.inputR".format(handik_finalstretchiness_clamp))
            cmds.connectAttr("{}.outputR".format(handik_finalstretchiness_clamp),"{}.blender".format(arm_stretchiness_blend))
            
            # 6.7.5 Conectar con las escalas de los huesos
            cmds.connectAttr("{}.outputX".format(arm_stretch_global_div),"{}.scaleX".format(shoulder_jnt))
            cmds.connectAttr("{}.outputY".format(arm_stretch_global_div),"{}.scaleX".format(elbow_jnt))
        
            # 6.7.6 Configurar el stretch FK
            shoulderfk_stretchglobal_mult = cmds.createNode("multiplyDivide",n="shoulderFkStretchByGlobal_{}_mult_{}".format(side_a,number_a_r))
            cmds.connectAttr("{}.stretch".format(shoulder_fk_ctr),"{}.input1X".format(shoulderfk_stretchglobal_mult))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.input2X".format(shoulderfk_stretchglobal_mult))
            cmds.connectAttr("{}.outputX".format(shoulderfk_stretchglobal_mult),"{}.color2G".format(arm_finalstretch_blend))
            
            cmds.pointConstraint(elbow_jnt,elbow_fk_offset,n="elbowToOffsetPoint_{}_cns_{}".format(side_a,number_a_r))
            
            elbowfk_stretchglobal_mult = cmds.createNode("multiplyDivide",n="elbowFkStretchByGlobal_{}_mult_{}".format(side_a,number_a_r))
            cmds.connectAttr("{}.stretch".format(elbow_fk_ctr),"{}.input1X".format(elbowfk_stretchglobal_mult))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.input2X".format(elbowfk_stretchglobal_mult))
            cmds.connectAttr("{}.outputX".format(elbowfk_stretchglobal_mult),"{}.color2B".format(arm_finalstretch_blend))
            
            cmds.pointConstraint(arm_end_jnt,hand_fk_offset,n="armEndToHandOffsetPoint_{}_cns_{}".format(side_a,number_a_r))
        
            # 6.7.7 Conectar los joints del twistShoulderChain con el stetch
            shoulder_twiststretch_ci = cmds.createNode("curveInfo",n="shoulderTwistStretch_{}_ci_{}".format(side_a,number_a_r))
            shoulder_twist_crv_shape = cmds.listRelatives(shoulder_twist_crv,s=True)[0]
            cmds.connectAttr("{}.worldSpace[0]".format(shoulder_twist_crv_shape),"{}.inputCurve".format(shoulder_twiststretch_ci))
            
            shoulder_ikcurvelength_div = cmds.createNode("multiplyDivide",n="shoulderIkCurveLength_{}_div_{}".format(side_a,number_a_r))
            cmds.setAttr("{}.operation".format(shoulder_ikcurvelength_div),2)
            cmds.connectAttr("{}.arcLength".format(shoulder_twiststretch_ci),"{}.input1X".format(shoulder_ikcurvelength_div))
            shoulder_ikcurvelength_value = cmds.getAttr("{}.arcLength".format(shoulder_twiststretch_ci))
            cmds.setAttr("{}.input2X".format(shoulder_ikcurvelength_div),shoulder_ikcurvelength_value)
            
            
            shoulder_lengthbyglobal_div = cmds.createNode("multiplyDivide",n="shoulderLengthByGlobal_{}_div_{}".format(side_a,number_a_r))
            cmds.setAttr("{}.operation".format(shoulder_lengthbyglobal_div),2)
            cmds.connectAttr("{}.outputX".format(shoulder_ikcurvelength_div),"{}.input1X".format(shoulder_lengthbyglobal_div))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.input2X".format(shoulder_lengthbyglobal_div))
            
            n_twit_shoulder = len(new_shoulder_twist_list) 
            new_shoulder_twist_list_stretch = new_shoulder_twist_list[0:n_twit_shoulder-1]
            for shoulder_twist_joints in new_shoulder_twist_list_stretch:
                cmds.connectAttr("{}.outputX".format(shoulder_lengthbyglobal_div),"{}.scaleX".format(shoulder_twist_joints))
        
            #6.7.8 Conectar los joints del twistForearmChain con el stretch 
            forearm_twiststretch_ci = cmds.createNode("curveInfo",n="forearmTwistStretch_{}_ci_{}".format(side_a,number_a_r))
            forearm_twist_crv_shape = cmds.listRelatives(forearm_twist_crv,s=True)[0]
            cmds.connectAttr("{}.worldSpace[0]".format(forearm_twist_crv_shape),"{}.inputCurve".format(forearm_twiststretch_ci))
            
            forearm_ikcurvelength_div = cmds.createNode("multiplyDivide",n="forearmIkCurveLength_{}_div_{}".format(side_a,number_a_r))
            cmds.setAttr("{}.operation".format(forearm_ikcurvelength_div),2)
            cmds.connectAttr("{}.arcLength".format(forearm_twiststretch_ci),"{}.input1X".format(forearm_ikcurvelength_div))
            forearm_ikcurvelength_value = cmds.getAttr("{}.arcLength".format(forearm_twiststretch_ci))
            cmds.setAttr("{}.input2X".format(forearm_ikcurvelength_div),forearm_ikcurvelength_value)
            
            forearm_lengthbyglobal_div = cmds.createNode("multiplyDivide",n="forarmLengthByGlobal_{}_div_{}".format(side_a,number_a_r))
            cmds.setAttr("{}.operation".format(forearm_lengthbyglobal_div),2)
            cmds.connectAttr("{}.outputX".format(forearm_ikcurvelength_div),"{}.input1X".format(forearm_lengthbyglobal_div))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.input2X".format(forearm_lengthbyglobal_div))
            
            n_twit_forearm = len(new_forearm_twist_list) 
            new_forearm_twist_list_stretch = new_forearm_twist_list[0:n_twit_forearm-1]
            for forearm_twist_joints in new_forearm_twist_list_stretch:
                cmds.connectAttr("{}.outputX".format(forearm_lengthbyglobal_div),"{}.scaleX".format(forearm_twist_joints)) 
        
            # 6.7.9 Conectar el pinElbow 
            pinelbow_byik_mult = cmds.createNode("multiplyDivide",n="pinElbowByIk_{}_mult_{}".format(side_a,number_a_r))
            cmds.connectAttr("{}.pinElbow".format(arm_pole_ctr),"{}.input1X".format(pinelbow_byik_mult))
            cmds.connectAttr("{}.armIK".format(arm_settings_ctr),"{}.input2X".format(pinelbow_byik_mult))
            cmds.connectAttr("{}.outputX".format(pinelbow_byik_mult),"{}.blender".format(arm_ikstretch_blend))
            cmds.connectAttr("{}.outputX".format(pinelbow_byik_mult),"{}.input2D[2].input2Dx".format(handik_autostretch_override_sum))
            
            # 6.7.10 Reposicionar el elbowStretchLoc en el ctrArmPole
            arm_pole_pos = cmds.xform(arm_pole_ctr,q=True,t=True,ws=True)
            cmds.xform(stretch_elbow_loc,t=arm_pole_pos,ws=True)
        
            # 6.7.11 Configuracion del autoSquash
            shoulder_lengthbyglobal_inv_div = cmds.createNode("multiplyDivide",n="shoulderLengthByGlobalInv_{}_div_{}".format(side_a,number_a_r))
            cmds.setAttr("{}.operation".format(shoulder_lengthbyglobal_inv_div),2)
            cmds.connectAttr("{}.outputX".format(shoulder_lengthbyglobal_div),"{}.input2X".format(shoulder_lengthbyglobal_inv_div))
            cmds.setAttr("{}.input1X".format(shoulder_lengthbyglobal_inv_div),1)
            
            forearm_lengthbyglobal_inv_div = cmds.createNode("multiplyDivide",n="forearmLengthByGlobalInv_{}_div_{}".format(side_a,number_a_r))
            cmds.setAttr("{}.operation".format(forearm_lengthbyglobal_inv_div),2)
            cmds.connectAttr("{}.outputX".format(forearm_lengthbyglobal_div),"{}.input2X".format(forearm_lengthbyglobal_inv_div))
            cmds.setAttr("{}.input1X".format(forearm_lengthbyglobal_inv_div),1)
            
            
            arm_autosquash_blend =cmds.createNode("blendColors",n="armAutoSquash_{}_blend_{}".format(side_a,number_a_r))
            cmds.connectAttr( "{}.autoSquash".format(arm_settings_ctr),"{}.blender".format(arm_autosquash_blend))
            cmds.connectAttr("{}.outputX".format(shoulder_lengthbyglobal_inv_div),"{}.color1R".format(arm_autosquash_blend))
            cmds.connectAttr("{}.outputX".format(forearm_lengthbyglobal_inv_div),"{}.color1B".format(arm_autosquash_blend))
            cmds.setAttr("{}.color2R".format(arm_autosquash_blend),1)
            cmds.setAttr("{}.color2B".format(arm_autosquash_blend),1)
            for joints in new_shoulder_twist_list:
                cmds.connectAttr("{}.outputR".format(arm_autosquash_blend),"{}.scaleY".format(joints))
                cmds.connectAttr("{}.outputR".format(arm_autosquash_blend),"{}.scaleZ".format(joints))
            for joints in new_forearm_twist_list:
                cmds.connectAttr("{}.outputB".format(arm_autosquash_blend),"{}.scaleY".format(joints))
                cmds.connectAttr("{}.outputB".format(arm_autosquash_blend),"{}.scaleZ".format(joints))
        
            # 6.8 Creacion de sistema bend
            # 6.8.1 Reconstruccion de curvas
            shoulder_twist_crv = cmds.rebuildCurve(shoulder_twist_crv,ch=1,rpo=1,rt=0,end=1,kr=0,kcp=0,kep=1,kt=0,s=1,d=3,tol=0.01)[0]
            forearm_twist_crv = cmds.rebuildCurve(forearm_twist_crv,ch=1,rpo=1,rt=0,end=1,kr=0,kcp=0,kep=1,kt=0,s=1,d=3,tol=0.01)[0]
            
            # 6.8.2 Creacion de clusters
            armbend_cluster_a =cmds.cluster("{}.cv[0]".format(shoulder_twist_crv),n="armBendA_{}_cl_{}".format(side_a,number_a_r))[1]
            armbend_cluster_b =cmds.cluster("{}.cv[1:2]".format(shoulder_twist_crv),n="armBendB_{}_cl_{}".format(side_a,number_a_r))[1]
            armbend_cluster_c =cmds.cluster("{}.cv[3]".format(shoulder_twist_crv),"{}.cv[0]".format(forearm_twist_crv),n="armBendC_{}_cl_{}".format(side_a,number_a_r))[1]
            armbend_cluster_d =cmds.cluster("{}.cv[1:2]".format(forearm_twist_crv),n="armBendD_{}_cl_{}".format(side_a,number_a_r))[1]
            armbend_cluster_e =cmds.cluster("{}.cv[3]".format(forearm_twist_crv),n="armBendE_{}_cl_{}".format(side_a,number_a_r))[1]        
        
            # 6.8.3 Creacion de controles Bend
            cmds.parent(armbend_cluster_a,shoulder_jnt)
            cmds.parent(armbend_cluster_e,elbow_jnt)
            
            uparm_bend_ctr = cmds.duplicate("uparmBend_{}_ctr_0".format(side_a),n="uparmBend_{}_ctr_{}".format(side_a,number_a_r))[0]
            uparm_bend_offset = CreateOffset(uparm_bend_ctr,number_a_r)
            cmds.matchTransform(uparm_bend_offset,armbend_cluster_b,pos=True,rot=False,scl=True)
            cmds.parent(armbend_cluster_b,uparm_bend_ctr)
            cmds.parent(uparm_bend_offset,shoulder_jnt)
            
            elbow_bend_ctr = cmds.duplicate("elbowBend_{}_ctr_0".format(side_a),n="elbowBend_{}_ctr_{}".format(side_a,number_a_r))[0]
            elbow_bend_offset = CreateOffset(elbow_bend_ctr,number_a_r)
            cmds.matchTransform(elbow_bend_offset,armbend_cluster_c,pos=True,rot=False,scl=True)
            cmds.parent(armbend_cluster_c,elbow_bend_ctr)
            cmds.parent(elbow_bend_offset,char_skeleton)
            
            forearm_bend_ctr = cmds.duplicate("forearmBend_{}_ctr_0".format(side_a),n="forearmBend_{}_ctr_{}".format(side_a,number_a_r))[0]
            forearm_bend_offset = CreateOffset(forearm_bend_ctr,number_a_r)
            cmds.matchTransform(forearm_bend_offset,armbend_cluster_d,pos=True,rot=False,scl=True)
            cmds.parent(armbend_cluster_d,forearm_bend_ctr)
            cmds.parent(forearm_bend_offset,elbow_jnt)
            # 6.8.4 Creacion de las relaciones entre los controles y los huesos
            cmds.parentConstraint(elbow_jnt,elbow_bend_offset,n="shoulderElbowBendParent_{}_cns_{}".format(side_a,number_a_r))                                              
            if arm_cl_conexion_check is True:
                # 6.9 Conexiones entre modulos(clavicle)
                # 6.9.1 Constraints
                cmds.parentConstraint("clavicle_{}_skn_{}".format(side_a,arm_cl_conexion),"shoulderRollSystem_{}_grp_{}".format(side_a,number_a_r),mo=True,n="clavicleShoulderRollParent_{}_cns_{}".format(side_a,number_a_r))
                cmds.pointConstraint("clavicleEnd_{}_jnt_{}".format(side_a,arm_cl_conexion),shoulder_offset,mo=False,n="clavicleEndShoulderJntOffsetPoint_{}_cns_{}".format(side_a,number_a_r)) 
                
                #6.9.2 Configuracion del shoulderFKPCon
                shoulderfk_pcon = cmds.duplicate(shoulder_fk_offset,n="shoulderFk_{}_pcon_{}".format(side_a,number_a_r),po=True)[0]
                cmds.parent(shoulderfk_pcon,"clavicleEnd_{}_jnt_{}".format(side_a,arm_cl_conexion))
                cmds.pointConstraint(shoulderfk_pcon,shoulder_fk_offset,mo=True,n="shoulderPcontoOffsetfkPoint_{}_cns_{}".format(side_a,number_a_r))
            spine_spaces_check = win.checkBoxArmSpineSpaces.isChecked()
            spine_arm_conexion_value = win.spinArmConexion.value()
            head_arm_conexion_value = win.spinHeadArmSpaces.value()
            if spine_spaces_check is True:
                # 6.10 Configuracion de los spaces
                # 6.10.1 Configuracion de los spaces en ctrShoulderFK(chestSpace)
                cmds.addAttr(shoulder_fk_ctr,ln= "__", at="enum",en="spaces")
                cmds.setAttr ("{}.__".format(shoulder_fk_ctr),channelBox= True)
                cmds.addAttr(shoulder_fk_ctr,ln= "chestSpace",at= "double",min= 0,max=1,dv=0,k=True)
                
                shoulderfk_worldspace = cmds.duplicate(shoulder_fk_offset,n="shoulderFKworldSpace_{}_grp_{}".format(side_a,number_a_r),po=True)[0]
                shoulderfk_chestSpace = cmds.duplicate(shoulder_fk_offset,n="shoulderFKchestSpace_{}_grp_{}".format(side_a,number_a_r),po=True)[0]
                shoulder_spaces_orient_cns = cmds.orientConstraint(shoulderfk_worldspace,shoulderfk_chestSpace,shoulder_fk_offset,mo=False,n="shoulderSpacesOrient_{}_cns_{}".format(side_a,number_a_r))[0]
                cmds.parent(shoulderfk_chestSpace,"chest_c_ctr_{}".format(spine_arm_conexion_value))
                
                cmds.connectAttr("{}.chestSpace".format(shoulder_fk_ctr),"{}.{}W1".format(shoulder_spaces_orient_cns,shoulderfk_chestSpace))
                shoulder_dynparent_rev = cmds.createNode("reverse",n="shoulderFkDynParent_{}_rev_{}".format(side_a,number_a_r))
                cmds.connectAttr("{}.chestSpace".format(shoulder_fk_ctr),"{}.inputX".format(shoulder_dynparent_rev))
                cmds.connectAttr("{}.outputX".format(shoulder_dynparent_rev),"{}.{}W0".format(shoulder_spaces_orient_cns,shoulderfk_worldspace))
                
                # 6.10.2 Configuracion de los spaces en ctrHandIk
                cmds.addAttr(hand_ik_ctr,ln= "__", at="enum",en="spaces")
                cmds.setAttr ("{}.__".format(hand_ik_ctr),channelBox= True)
                cmds.addAttr(hand_ik_ctr,ln= "headSpace",at= "double",min= 0,max=1,dv=0,k=True)
                cmds.addAttr(hand_ik_ctr,ln= "chestSpace",at= "double",min= 0,max=1,dv=0,k=True)
                cmds.addAttr(hand_ik_ctr,ln= "pelvisSpace",at= "double",min= 0,max=1,dv=0,k=True)
                
                handik_worldspace = cmds.duplicate(hand_ik_offset,n="handIkWorldSpace_{}_grp_{}".format(side_a,number_a_r),po=True)[0]
                handik_headspace = cmds.duplicate(hand_ik_offset,n="handIkHeadSpace_{}_grp_{}".format(side_a,number_a_r),po=True)[0]
                handik_chestspace = cmds.duplicate(hand_ik_offset,n="handIkChestSpace_{}_grp_{}".format(side_a,number_a_r),po=True)[0]
                handik_pelvisspace = cmds.duplicate(hand_ik_offset,n="handIkPelvisSpace_{}_grp_{}".format(side_a,number_a_r),po=True)[0]
                
                hand_spaces_parent_cns = cmds.parentConstraint(handik_worldspace,
                                                               handik_headspace,
                                                               handik_chestspace,
                                                               handik_pelvisspace,
                                                               hand_ik_offset,
                                                               mo=False,
                                                               n="handIkSpacesParent_{}_cns".format(side_a))[0]
                cmds.parent(handik_headspace,"head_c_ctr_{}".format(head_arm_conexion_value))
                cmds.parent(handik_chestspace,"chest_c_ctr_{}".format(spine_arm_conexion_value))
                cmds.parent(handik_pelvisspace,"pelvis_c_ctr_{}".format(spine_arm_conexion_value))
                
                cmds.connectAttr("{}.headSpace".format(hand_ik_ctr),"{}.{}W1".format(hand_spaces_parent_cns,handik_headspace))
                cmds.connectAttr("{}.chestSpace".format(hand_ik_ctr),"{}.{}W2".format(hand_spaces_parent_cns,handik_chestspace))
                cmds.connectAttr("{}.pelvisSpace".format(hand_ik_ctr),"{}.{}W3".format(hand_spaces_parent_cns,handik_pelvisspace))
                
                handik_dynparent_sum = cmds.createNode("plusMinusAverage",n="handIkDynParent_{}_sum_{}".format(side_a,number_a_r))
                cmds.connectAttr("{}.headSpace".format(hand_ik_ctr),"{}.input2D[0].input2Dx".format(handik_dynparent_sum))
                cmds.connectAttr("{}.chestSpace".format(hand_ik_ctr),"{}.input2D[1].input2Dx".format(handik_dynparent_sum))
                cmds.connectAttr("{}.pelvisSpace".format(hand_ik_ctr),"{}.input2D[2].input2Dx".format(handik_dynparent_sum))
                
                handik_dynparent_clamp = cmds.createNode("clamp",n="handIkDynParent_{}_clamp_{}".format(side_a,number_a_r))
                cmds.setAttr("{}.maxR".format(handik_dynparent_clamp),1)
                cmds.connectAttr("{}.output2Dx".format(handik_dynparent_sum),"{}.inputR".format(handik_dynparent_clamp))
                
                handik_dynparent_rev = cmds.createNode("reverse",n="handIkDynParent_{}_rev_{}".format(side_a,number_a_r))
                cmds.connectAttr("{}.outputR".format(handik_dynparent_clamp),"{}.inputX".format(handik_dynparent_rev))
                cmds.connectAttr("{}.outputX".format(handik_dynparent_rev),"{}.{}W0".format(hand_spaces_parent_cns,handik_worldspace))
                # 6.10.3 Configuracion de los spaces en el ctrArmPole
                cmds.addAttr(arm_pole_ctr,ln= "__", at="enum",en="spaces")
                cmds.setAttr ("{}.__".format(arm_pole_ctr),channelBox= True)
                cmds.addAttr(arm_pole_ctr,ln= "handSpace",at= "double",min= 0,max=1,dv=0,k=True)
                cmds.addAttr(arm_pole_ctr,ln= "chestSpace",at= "double",min= 0,max=1,dv=0,k=True)
                arm_pole_worldspace = cmds.duplicate(arm_pole_offset,n="armPoleWorldSpace_{}_grp_{}".format(side_a,number_a_r),po=True)[0]
                arm_pole_handspace = cmds.duplicate(arm_pole_offset,n="armPoleHandSpace_{}_grp_{}".format(side_a,number_a_r),po=True)[0]
                arm_pole_chestspace = cmds.duplicate(arm_pole_offset,n="armPoleChestSpace_{}_grp_{}".format(side_a,number_a_r),po=True)[0]
                
                armpole_spaces_parent_cns = cmds.parentConstraint(arm_pole_worldspace,arm_pole_handspace,arm_pole_chestspace,arm_pole_offset,mo=False,n="armPoleSpacesParent_{}_cns_{}".format(side_a,number_a_r))[0]
                
                cmds.parent(arm_pole_handspace,"handIK_{}_ctr_{}".format(side_a,number_a_r))
                cmds.parent(arm_pole_chestspace,"chest_c_ctr_{}".format(spine_arm_conexion_value))
                
                cmds.connectAttr("{}.handSpace".format(arm_pole_ctr),"{}.{}W1".format(armpole_spaces_parent_cns,arm_pole_handspace))
                cmds.connectAttr("{}.chestSpace".format(arm_pole_ctr),"{}.{}W2".format(armpole_spaces_parent_cns,arm_pole_chestspace))
                
                armpole_dynparent_sum = cmds.createNode("plusMinusAverage",n="armPoleDynParent_{}_sum_{}".format(side_a,number_a_r))
                cmds.connectAttr("{}.handSpace".format(arm_pole_ctr),"{}.input2D[0].input2Dx".format(armpole_dynparent_sum))
                cmds.connectAttr("{}.chestSpace".format(arm_pole_ctr),"{}.input2D[1].input2Dx".format(armpole_dynparent_sum))
                
                armpole_dynparent_clamp = cmds.createNode("clamp",n="armPoleDynParent_{}_clamp_{}".format(side_a,number_a_r))
                cmds.setAttr("{}.maxR".format(armpole_dynparent_clamp),1)
                cmds.connectAttr("{}.output2Dx".format(armpole_dynparent_sum),"{}.inputR".format(armpole_dynparent_clamp))
                
                armpole_dynparent_rev = cmds.createNode("reverse",n="armPoleDynParent_{}_rev_{}".format(side_a,number_a_r))
                cmds.connectAttr("{}.outputR".format(armpole_dynparent_clamp),"{}.inputX".format(armpole_dynparent_rev))
                cmds.connectAttr("{}.outputX".format(armpole_dynparent_rev),"{}.{}W0".format(armpole_spaces_parent_cns,arm_pole_worldspace))
        
            # Cerrar rig
            cmds.connectAttr("{}.visBends".format(arm_settings_ctr),"{}.visibility".format(uparm_bend_ctr))
            cmds.connectAttr("{}.visBends".format(arm_settings_ctr),"{}.visibility".format(elbow_bend_ctr))
            cmds.connectAttr("{}.visBends".format(arm_settings_ctr),"{}.visibility".format(forearm_bend_ctr))
            Hide("shoulderNonRoll_{}_grp_{}".format(side_a,number_a_r))
            Hide(shoulder_twist_ik)
            Hide("forearmRollSystem_{}_grp_{}".format(side_a,number_a_r))
            Hide(arm_main_ik)
            Hide(shoulder_twist_crv)
            Hide(forearm_twist_crv)
            Hide(stretch_shoulder_loc)
            Hide(stretch_elbow_loc)
            Hide(stretch_hand_loc)
            Hide(armbend_cluster_a)
            Hide(armbend_cluster_b)
            Hide(armbend_cluster_c)
            Hide(armbend_cluster_d)
            Hide(armbend_cluster_e)
            last_shoulder_twist_jnt = cmds.rename(last_shoulder_twist_jnt,"{}_{}_jnt_{}".format(last_shoulder_twist_jnt.split("_")[0],side_a,number_a_r))
            last_forearm_twist_jnt =  cmds.rename(last_forearm_twist_jnt,"{}_{}_jnt_{}".format(last_forearm_twist_jnt.split("_")[0],side_a,number_a_r))
            LockScaleVis(hand_ik_ctr)
            LockScaleRotVis(arm_pole_ctr)
            LockScaleRotVis(uparm_bend_ctr)
            LockScaleRotVis(elbow_bend_ctr)
            LockScaleRotVis(forearm_bend_ctr)
            LockScaleTransVis(shoulder_fk_ctr)
            LockScaleTransVis(elbow_fk_ctr)
            LockScaleTransVis(hand_fk_ctr)
            LockAll(arm_settings_ctr)
            createArmSnap(number_a_r,side_a)             
        win.armRightButton.clicked.connect(BuildRightArm)
        
        def BuildLeftLeg():
            number_upleg_joints = win.spinBoxUplegNumberJoints.value()
            number_lowleg_joints = win.spinBoxLowlegNumberJoints.value()
            side_l = "l"
            hip = "hip_{}_loc_{}".format(side_l,number_l_l)
            knee = "knee_{}_loc_{}".format(side_l,number_l_l)
            foot = "foot_{}_loc_{}".format(side_l,number_l_l)
            ball = "ball_{}_loc_{}".format(side_l,number_l_l)
            toe = "toe_{}_loc_{}".format(side_l,number_l_l)
            heel = "heelPos_{}_loc_{}".format(side_l,number_l_l)
            bank_ext = "bankExtPos_{}_loc_{}".format(side_l,number_l_l)
            bank_int = "bankIntPos_{}_loc_{}".format(side_l,number_l_l)
            # 6.1 Creacion de los huesos y reorientacion de locators
            del_cons = cmds.aimConstraint(knee,
                                         hip,
                                         offset=(0,0,0),
                                         weight=1,
                                         aimVector=(1,0,0),
                                         upVector=(0,1,0),
                                         worldUpType="scene")[0]
            cmds.delete(del_cons)
            del_cons = cmds.aimConstraint(foot,
                                          knee,
                                          offset=(0,0,0),
                                          weight=1,
                                          aimVector=(1,0,0),
                                          upVector=(0,1,0),
                                          worldUpType="scene")[0]
            cmds.delete(del_cons)
            del_cons = cmds.aimConstraint(knee,
                                          foot,
                                          offset=(0,0,0),
                                          weight=1,
                                          aimVector=(-1,0,0),
                                          upVector=(0,1,0),
                                          worldUpType="scene")[0]
            cmds.delete(del_cons)
            
            cmds.select(cl=1)
            hip_jnt = cmds.joint(n="hip_{}_jnt_{}".format(side_l,number_l_l))
            hip_pos = cmds.xform(hip,q=True,matrix=True,ws=True)
            cmds.xform(hip_jnt,matrix=hip_pos,ws=True)
            hip_rot = cmds.getAttr("{}.rotateZ".format(hip_jnt))
            cmds.setAttr("{}.rotateZ".format(hip_jnt),0)
            cmds.setAttr("{}.jointOrientZ".format(hip_jnt),hip_rot)
            
            knee_jnt = cmds.joint(n="knee_{}_jnt_{}".format(side_l,number_l_l))
            knee_pos = cmds.xform(knee,q=True,matrix=True,ws=True)
            cmds.xform(knee_jnt,matrix=knee_pos,ws=True)
            
            leg_end_jnt = cmds.joint(n="legEnd_{}_jnt_{}".format(side_l,number_l_l))
            foot_pos = cmds.xform(foot,q=True,matrix=True,ws=True)
            cmds.xform(leg_end_jnt,matrix=foot_pos,ws=True)
            cmds.setAttr("{}.preferredAngleY".format(knee_jnt),90)
            hip_jnt_offset = CreateOffset(hip_jnt,number_l_l)
            cmds.parent(hip_jnt_offset,char_skeleton)
            
            # 8.1.2 Creacion de la cadena del pie:
            cmds.xform(foot,ro=(0,-90,0),ws=True)
            cmds.xform(ball,ro=(0,-90,0),ws=True)
            cmds.xform(toe,ro=(0,-90,0),ws=True)
            cmds.select(cl=1)
            foot_jnt = cmds.joint(n="foot_{}_skn_{}".format(side_l,number_l_l))
            cmds.matchTransform(foot_jnt,foot,pos=True,rot=True,scl=False)
            for axis in "XYZ":
                foot_rot = cmds.getAttr("{}.rotate{}".format(foot_jnt,axis))
                cmds.setAttr("{}.rotate{}".format(foot_jnt,axis),0)
                cmds.setAttr("{}.jointOrient{}".format(foot_jnt,axis),foot_rot)
            ball_jnt = cmds.joint(n="ball_{}_skn_{}".format(side_l,number_l_l))
            cmds.matchTransform(ball_jnt,ball,pos=True,rot=True,scl=False)
            for axis in "XYZ":
                ball_rot = cmds.getAttr("{}.rotate{}".format(ball_jnt,axis))
                cmds.setAttr("{}.rotate{}".format(ball_jnt,axis),0)
                cmds.setAttr("{}.jointOrient{}".format(ball_jnt,axis),ball_rot)
            toe_jnt = cmds.joint(n="toe_{}_jnt_{}".format(side_l,number_l_l))
            cmds.matchTransform(toe_jnt,toe,pos=True,rot=True,scl=False)
            foot_offset = CreateOffset(foot_jnt,number_l_l)
            cmds.parent(foot_offset,char_skeleton)
            cmds.pointConstraint(leg_end_jnt,foot_offset,n="legEndFootPoint_{}_cns_{}".format(side_l,number_l_l))    
        
            #8.2 Creacion del ikHandle del la cadena principal
            leg_main_ik = cmds.ikHandle( sj=hip_jnt, ee=leg_end_jnt, s="sticky",n="legMainikHandle_{}_ik_{}".format(side_l,number_l_l),sol="ikRPsolver")[0]
            if "l" in side_l:
                cmds.parent(leg_main_ik,leg_l_rig)
            if "r" in side_l:
                cmds.parent(leg_main_ik,leg_r_rig)
            for axis in "XYZ":
                cmds.setAttr("{}.poleVector{}".format(leg_main_ik,axis),0)
            
            # 8.3.1 Configuracion de la cadena NonRoll del Hip
            hip_non_roll = cmds.duplicate(hip_jnt,po=True,n="hipNonRoll_{}_jnt_{}".format(side_l,number_l_l))[0]
            hip_non_roll_end =  cmds.duplicate(knee_jnt,po=True,n="hipNonRollEnd_{}_jnt_{}".format(side_l,number_l_l))[0]
            cmds.setAttr("{}.jointOrientX".format(hip_non_roll),0)
            cmds.parent(hip_non_roll_end,hip_non_roll)
            hip_non_roll_ik = cmds.ikHandle(sj=hip_non_roll, ee=hip_non_roll_end, s="sticky",n="hipNonRollikHandle_{}_ik_{}".format(side_l,number_l_l),sol="ikRPsolver")[0]
            for axis in "XYZ":
                cmds.setAttr("{}.poleVector{}".format(hip_non_roll_ik,axis),0)
            
            if "l" in side_l:
                upleg_roll_system = cmds.group(n="uplegRollSystem_{}_grp_{}".format(side_l,number_l_l),em=1,p=leg_l_rig)
            if "r" in side_l:
                upleg_roll_system = cmds.group(n="uplegRollSystem_{}_grp_{}".format(side_l,number_r_l),em=1,p=leg_r_rig)
            for axis in "XYZ":
                cmds.connectAttr("{}.globalScale".format(control_base),"{}.scale{}".format(upleg_roll_system,axis))
            
            hip_non_roll_grp = cmds.group(n="hipNonRoll_{}_grp_{}".format(side_l,number_l_l),em=1,p=upleg_roll_system)
            
            cmds.parent(hip_non_roll_ik,hip_non_roll_grp)
            cmds.parent(hip_non_roll,hip_non_roll_grp)
            
            cmds.pointConstraint(hip_jnt,hip_non_roll,n="hipNonRollPoint_{}_cns_{}".format(side_l,number_l_l))
            cmds.pointConstraint(knee_jnt,hip_non_roll_ik,n="hipIkNonRollPoint_{}_cns_{}".format(side_l,number_l_l))
        
            # 8.3.2 Configuracion de la cadena NonRoll del Knee
            knee_non_roll = cmds.duplicate(knee_jnt,po=True,n="kneeNonRoll_{}_jnt_{}".format(side_l,number_l_l))[0]
            knee_non_roll_end =  cmds.duplicate(leg_end_jnt,po=True,n="kneeNonRollEnd_{}_jnt_{}".format(side_l,number_l_l))[0]
            cmds.setAttr("{}.jointOrientX".format(knee_non_roll),0)
            cmds.parent(knee_non_roll_end,knee_non_roll)
            knee_non_roll_ik = cmds.ikHandle(sj=knee_non_roll, ee=knee_non_roll_end, s="sticky",n="kneeNonRollikHandle_{}_ik_{}".format(side_l,number_l_l),sol="ikRPsolver")[0]
            for axis in "XYZ":
                cmds.setAttr("{}.poleVector{}".format(knee_non_roll_ik,axis),0)
            if "l" in side_l:
                lowleg_roll_system = cmds.group(n="lowlegRollSystem_{}_grp_{}".format(side_l,number_l_l),em=1,p=leg_l_rig)
            if "r" in side_l:
                lowleg_roll_system = cmds.group(n="lowlegRollSystem_{}_grp_{}".format(side_l,number_r_l),em=1,p=leg_r_rig)
            knee_non_roll_grp = cmds.group(n="kneeNonRoll_{}_grp_{}".format(side_l,number_l_l),em=1,p=lowleg_roll_system)
            
            cmds.parent(knee_non_roll,knee_non_roll_grp)
            cmds.parent(knee_non_roll_ik,knee_non_roll_grp)
            
            cmds.pointConstraint(knee_jnt,knee_non_roll,n="kneeNonRollPoint_{}_cns_{}".format(side_l,number_l_l))
            cmds.pointConstraint(foot_jnt,knee_non_roll_ik,n="kneeNonRollIkPoint_{}_cns_{}".format(side_l,number_l_l))
            
            knee_twist_value = cmds.duplicate(knee_jnt,po=True,n="kneeTwistValue_{}_jnt_{}".format(side_l,number_l_l))[0]
            cmds.parent(knee_twist_value,knee_jnt)
            cmds.aimConstraint(foot_jnt,
                                knee_twist_value,
                                offset=(0,0,0),
                                weight=1,
                                aimVector=(1,0,0),
                                upVector=(0,1,0),
                                worldUpType="objectrotation",
                                worldUpVector=(0,1,0),
                                worldUpObject=knee_non_roll,
                                n="foottoKneeNonAim_{}_cns_{}".format(side_l,number_l_l))
            cmds.parentConstraint(hip_non_roll,knee_non_roll_grp,mo=True,n="hipNonToKneeNonRollGrpParent_{}_cns_{}".format(side_l,number_l_l))
        
            # 8.3.3 Configuracion de la cadena NonRoll del Foot
            foot_non_roll = cmds.duplicate(leg_end_jnt,po=True,n="footNonRoll_{}_jnt_{}".format(side_l,number_l_l))[0] 
            foot_non_roll_end = cmds.duplicate(leg_end_jnt,po=True,n="footNonRollEnd_{}_jnt_{}".format(side_l,number_l_l))[0]
            cmds.setAttr("{}.jointOrientX".format(foot_non_roll),0)
            cmds.parent(foot_non_roll_end,foot_non_roll)
            cmds.setAttr("{}.translateX".format(foot_non_roll_end),1)
            foot_non_roll_ik = cmds.ikHandle(sj=foot_non_roll, ee=foot_non_roll_end, s="sticky",n="footNonRollikHandle_{}_ik_{}".format(side_l,number_l_l),sol="ikRPsolver")[0]
            for axis in "XYZ":
                cmds.setAttr("{}.poleVector{}".format(foot_non_roll_ik,axis),0)
            
            foot_non_roll_grp = cmds.group(n="footNonRoll_{}_grp_{}".format(side_l,number_l_l),em=1,p=lowleg_roll_system)
            cmds.parent(foot_non_roll,foot_non_roll_grp)
            cmds.parent(foot_non_roll_ik,foot_non_roll_grp)
            
            cmds.pointConstraint(foot_jnt,foot_non_roll,n="footNonRollPoint_{}_cns_{}".format(side_l,number_l_l))
            foot_nonroll_ikhandle_pcon = cmds.group(n="footNonRollIkHandle_{}_pcon_{}".format(side_l,number_l_l),em=1,p=foot_jnt)
            cmds.matchTransform(foot_nonroll_ikhandle_pcon,foot_non_roll_end,pos=True,rot=False,scl=False)
            cmds.pointConstraint(foot_nonroll_ikhandle_pcon,foot_non_roll_ik,n="footNonRollIkHandlePconPoint_{}_cns_{}".format(side_l,number_l_l))
            
            foot_twist_value = cmds.duplicate(foot_jnt,po=True,n="footTwistValue_{}_jnt_{}".format(side_l,number_l_l))[0]
            cmds.parent(foot_twist_value,foot_jnt)
            cmds.setAttr("{}.jointOrientY".format(foot_twist_value),90)
            cmds.aimConstraint(foot_non_roll_end,
                                foot_twist_value,
                                offset=(0,0,0),
                                weight=1,
                                aimVector=(1,0,0),
                                upVector=(0,1,0),
                                worldUpType="objectrotation",
                                worldUpVector=(0,1,0),
                                worldUpObject=foot_non_roll,
                                n="foottoKneeNonAim_{}_cns_{}".format(side_l,number_l_l))
            cmds.parentConstraint(knee_jnt,foot_non_roll_grp,mo=True,n="kneeToFootNonRollGrpParent_{}_cns_{}".format(side_l,number_l_l)) 
        
            # 8.4.1 Creacion de la cadena twist del Upleg
            upleg_twist_list = JointChain(hip,knee,"uplegTwist",number_upleg_joints)
            new_upleg_twist_list = []
            for upleg_twist in upleg_twist_list:
                upleg_twist_jnt = cmds.rename(upleg_twist,"{}_{}_skn_{}".format(upleg_twist,side_l,number_l_l))
                new_upleg_twist_list.append(upleg_twist_jnt)
            first_upleg_twist = new_upleg_twist_list[0] 
            cmds.parent(first_upleg_twist,upleg_roll_system)
            last_upleg_twist = new_upleg_twist_list[-1]
            ikhandle_upleg_twist_list = cmds.ikHandle(sj=first_upleg_twist,
                                                         ee=last_upleg_twist,
                                                         sol="ikSplineSolver",
                                                         scv=False,
                                                         pcv=False,
                                                         n="uplegTwistikHandle_{}_ik_{}".format(side_l,number_l_l))
            upleg_twist_ik = ikhandle_upleg_twist_list[0]
            upleg_twist_crv = ikhandle_upleg_twist_list[2]
            upleg_twist_crv = cmds.rename(upleg_twist_crv,"uplegTwist_{}_crv_{}".format(side_l,number_l_l))
            cmds.parent(upleg_twist_ik,upleg_roll_system)
            if "l" in side_l:
                cmds.parent(upleg_twist_crv,leg_l_rig)
            if "r" in side_l:
                cmds.parent(upleg_twist_crv,leg_r_rig)
            upleg_twistvalue_mult = cmds.createNode("multiplyDivide",n="uplegTwistValue_{}_mult_{}".format(side_l,number_l_l))
            cmds.connectAttr("{}.rotateX".format(knee_twist_value),"{}.input1X".format(upleg_twistvalue_mult))
            cmds.setAttr("{}.input2X".format(upleg_twistvalue_mult),-1)
            cmds.connectAttr("{}.outputX".format(upleg_twistvalue_mult),"{}.twist".format(upleg_twist_ik))
            
            #8.4.2 Creacion de la cadena twist del Lowleg
            lowleg_twist_list = JointChain(knee,foot,"lowlegTwist",number_lowleg_joints)
            new_lowleg_twist_list = []
            for lowleg_twist in lowleg_twist_list:
                lowleg_twist_jnt = cmds.rename(lowleg_twist,"{}_{}_skn_{}".format(lowleg_twist,side_l,number_l_l))
                new_lowleg_twist_list.append(lowleg_twist_jnt)
            first_lowleg_twist = new_lowleg_twist_list[0]
            cmds.parent(first_lowleg_twist,knee_jnt)
            last_lowleg_twist = new_lowleg_twist_list[-1]
            ikhandle_lowleg_twist_list = cmds.ikHandle(sj=first_lowleg_twist,
                                                         ee=last_lowleg_twist,
                                                         sol="ikSplineSolver",
                                                         scv=False,
                                                         pcv=False,
                                                         n="lowlegTwistikHandle_{}_ik_{}".format(side_l,number_l_l))
            lowleg_twist_ik = ikhandle_lowleg_twist_list[0]
            lowleg_twist_crv = ikhandle_lowleg_twist_list[2]
            lowleg_twist_crv = cmds.rename(lowleg_twist_crv,"lowlegTwist_{}_crv_{}".format(side_l,number_l_l))
            cmds.parent(lowleg_twist_ik,lowleg_roll_system)
            if "l" in side_l:
                cmds.parent(lowleg_twist_crv,leg_l_rig)
            if "r" in side_l:
                cmds.parent(lowleg_twist_crv,leg_r_rig)
            lowleg_twistvalue_mult = cmds.createNode("multiplyDivide",n="lowlegTwistValue_{}_mult_{}".format(side_l,number_l_l))        
            cmds.connectAttr("{}.rotateX".format(foot_twist_value),"{}.input1X".format(lowleg_twistvalue_mult))
            cmds.setAttr("{}.input2X".format(lowleg_twistvalue_mult),-1)
            cmds.connectAttr("{}.outputX".format(lowleg_twistvalue_mult),"{}.twist".format(lowleg_twist_ik))
        
            # 8.5.1 Creacion del control FootIK
            foot_ik_ctr = cmds.duplicate("footIK_{}_ctr_0".format(side_l),n="footIK_{}_ctr_{}".format(side_l,number_l_l))[0]
            foot_ik_offset = CreateOffset(foot_ik_ctr,number_l_l)
            cmds.matchTransform(foot_ik_offset,foot_jnt,pos=True,rot=False,scl=False)
            cmds.parent(foot_ik_offset,foot_jnt)
            for axis in "XZ":
                cmds.setAttr("{}.rotate{}".format(foot_ik_offset,axis),0)
            cmds.setAttr("{}.rotateY".format(foot_ik_offset),90)
            if "r" in side_l:
                cmds.setAttr("{}.rotateX".format(hip_fk_offset),-180)
            cmds.parent(foot_ik_offset,control_center)
            AttrSeparator(foot_ik_ctr)    
            cmds.addAttr(foot_ik_ctr,ln= "knee",at= "double",dv=0,k=True)
            cmds.addAttr(foot_ik_ctr,ln= "autoStretch",at= "double",max=1,min=0,dv=1,k=True)
            cmds.addAttr(foot_ik_ctr,ln= "footRoll",at= "double",dv=0,k=True)
            cmds.addAttr(foot_ik_ctr,ln= "toeBreak",at= "double",dv=45,k=True)
            cmds.addAttr(foot_ik_ctr,ln= "releaseAngle",at= "double",dv=120,k=True)
            cmds.addAttr(foot_ik_ctr,ln= "footTilt",at= "double",dv=0,k=True)
            cmds.addAttr(foot_ik_ctr,ln= "toeRoll",at= "double",dv=0,k=True)
            cmds.addAttr(foot_ik_ctr,ln= "toeSlide",at= "double",dv=0,k=True)
            cmds.addAttr(foot_ik_ctr,ln= "heelRoll",at= "double",dv=0,k=True)
            cmds.addAttr(foot_ik_ctr,ln= "ballRoll",at= "double",dv=0,k=True)
        
            # 8.5.2 Creacion del control legPole
            leg_pole_ctr = cmds.duplicate("legPole_{}_ctr_0".format(side_l),n="legPole_{}_ctr_{}".format(side_l,number_l_l))[0]
            leg_pole_offset = CreateOffset(leg_pole_ctr,number_l_l)
            leg_pole_loc = PoleVector(sel=[hip_jnt,knee_jnt,leg_end_jnt],side=side_l)
            del_loc = cmds.duplicate(leg_pole_loc,n="del_loc")[0]
            cmds.parent(del_loc,leg_pole_loc)
            pole_distance = cmds.getAttr("{}.translateX".format(knee_jnt))
            cmds.setAttr("{}.translateX".format(del_loc),pole_distance)
            cmds.matchTransform(leg_pole_offset,del_loc,pos=True,rot=False,scl=False)
            cmds.delete(leg_pole_loc)
            cmds.parent(leg_pole_offset,control_center)
            AttrSeparator(leg_pole_ctr)
            cmds.addAttr(leg_pole_ctr,ln= "pinKnee",at= "double",max=1,min=0,dv=0,k=True)
        
            # 8.5.3 Creacion del control hip
            hip_ctr = cmds.duplicate("hip_{}_ctr_0".format(side_l),"hip_{}_ctr_{}".format(side_l,number_l_l))[0]
            hip_offset = CreateOffset(hip_ctr,number_l_l)
            cmds.matchTransform(hip_offset,hip_jnt,pos=True,rot=False,scl=False)
            spine_leg_conexion = win.checkBoxLegSpineConexion.isChecked()
            spine_leg_conexion_value = win.spinLegSpineConexion.value()
            if spine_leg_conexion is True:
                cmds.parent(hip_offset,"pelvis_c_ctr_{}".format(spine_leg_conexion_value))
            else:
                cmds.parent(hip_offset,control_center)
        
            # 8.5.4 Creacion del control legSettings
            leg_settings_ctr = cmds.duplicate("legSettings_{}_ctr_0".format(side_l),n="legSettings_{}_ctr_{}".format(side_l,number_l_l))[0]
            leg_settings_offset = CreateOffset(leg_settings_ctr,number_l_l)
            cmds.matchTransform(leg_settings_offset,foot_jnt,pos=True,rot=False,scl=False)
            leg_settings_pos = cmds.getAttr("{}.translateX".format(ball_jnt))
            cmds.setAttr("{}.translateZ".format(leg_settings_offset),0-leg_settings_pos)
            cmds.parent(leg_settings_offset,control_center)
            AttrSeparator(leg_settings_ctr)
            cmds.addAttr(leg_settings_ctr,ln= "legIK",at= "double",max=1,min=0,dv=1,k=True)
            cmds.addAttr(leg_settings_ctr,ln= "autoSquash",at= "double",max=1,min=0,dv=1,k=True)
            cmds.addAttr(leg_settings_ctr,ln= "visBends",at= "double",max=1,min=0,dv=1,k=True)
        
            # 8.5.5 Creacion del control hipFK
            hip_fk_ctr = cmds.duplicate("hipFK_{}_ctr_0".format(side_l),n="hipFK_{}_ctr_{}".format(side_l,number_l_l))[0]
            hip_fk_offset = CreateOffset(hip_fk_ctr,number_l_l)
            cmds.matchTransform(hip_fk_offset,hip_jnt,pos=True,rot=False,scl=False)
            cmds.parent(hip_fk_offset,hip_jnt)
            for axis in "XY":
                cmds.setAttr("{}.rotate{}".format(hip_fk_offset,axis),0)
            cmds.setAttr("{}.rotateZ".format(hip_fk_offset),90)
            if "r" in side_l:
                cmds.setAttr("{}.rotateX".format(hip_fk_offset),-180)
            cmds.parent(hip_fk_offset,control_center)
            AttrSeparator(hip_fk_ctr)
            cmds.addAttr(hip_fk_ctr,ln= "stretch",at= "double",dv=1,k=True)
           
            # 8.5.6 Creacion del control kneeFK
            knee_fk_ctr = cmds.duplicate("kneeFK_{}_ctr_0".format(side_l),n="kneeFK_{}_ctr_{}".format(side_l,number_l_l))[0]
            knee_fk_offset = CreateOffset(knee_fk_ctr,number_l_l)
            cmds.matchTransform(knee_fk_offset,knee_jnt,pos=True,rot=False,scl=False)
            cmds.parent(knee_fk_offset,knee_jnt)
            for axis in "XY":
                cmds.setAttr("{}.rotate{}".format(knee_fk_offset,axis),0)
            cmds.setAttr("{}.rotateZ".format(knee_fk_offset),90)
            if "r" in side_l:
                cmds.setAttr("{}.rotateX".format(knee_fk_offset),-180)
            cmds.parent(knee_fk_offset,hip_fk_ctr)
            AttrSeparator(knee_fk_ctr)
            cmds.addAttr(knee_fk_ctr,ln= "stretch",at= "double",dv=1,k=True)
            
            # 8.5.6 Creacion del control footFK
            foot_fk_ctr = cmds.duplicate("footFK_{}_ctr_0".format(side_l),n="footFK_{}_ctr_{}".format(side_l,number_l_l))[0]
            foot_fk_offset = CreateOffset(foot_fk_ctr,number_l_l)
            cmds.matchTransform(foot_fk_offset,foot_jnt,pos=True,rot=False,scl=False)
            cmds.parent(foot_fk_offset,foot_jnt)
            for axis in "XZ":
                cmds.setAttr("{}.rotate{}".format(foot_fk_offset,axis),0)
            cmds.setAttr("{}.rotateY".format(foot_fk_offset),90)
            if "r" in side_l:
                cmds.setAttr("{}.rotateX".format(foot_fk_offset),-180)
            cmds.parent(foot_fk_offset,knee_fk_ctr)   
        
            # 8.5.8 Creacion del control toe
            toe_ctr = cmds.duplicate("toe_{}_ctr_0".format(side_l),n="toe_{}_ctr_{}".format(side_l,number_l_l))[0]
            toe_offset = CreateOffset(toe_ctr,number_l_l)
            cmds.matchTransform(toe_offset,ball_jnt,pos=True,rot=False,scl=False)
            cmds.parent(toe_offset,ball_jnt)
            for axis in "XZ":
                cmds.setAttr("{}.rotate{}".format(toe_offset,axis),0)
            cmds.setAttr("{}.rotateY".format(toe_offset),90)
            cmds.parent(toe_offset,control_center)
        
            # 8.6.1 Configuracion del footroll system: Creacion y emparentamiento de locators
            ankle = cmds.duplicate(foot,n="ankle_{}_pcon_{}".format(side_l,number_l_l))[0]
            cmds.xform(ankle,ro=(0,0,0),ws=True)
            if "r" in side_l:
                cmds.setAttr("{}.rotateX".format(ankle),-180)
            ball_pivot = cmds.duplicate(ball,n="ballPivot_{}_loc_{}".format(side_l,number_l_l))[0]
            cmds.xform(ball_pivot,ro=(0,0,0),ws=True)
            if "r" in side_l:
                cmds.setAttr("{}.rotateX".format(ball_pivot),-180)
            ball_pivot_param = cmds.duplicate(ball_pivot,n="ballPivotParam_{}_loc_{}".format(side_l,number_l_l))[0]
            toe_pivot = cmds.duplicate(toe,n="toePivot_{}_loc_{}".format(side_l,number_l_l))[0]
            cmds.xform(toe_pivot,ro=(0,0,0),ws=True)
            if "r" in side_l:
                cmds.setAttr("{}.rotateX".format(toe_pivot),-180)
            toe_pivot_param = cmds.duplicate(toe_pivot,n="toePivotParam_{}_loc_{}".format(side_l,number_l_l))[0]
            heel_pivot = cmds.duplicate(heel,n="heelPivot_{}_loc_{}".format(side_l,number_l_l))[0]
            if "r" in side_l:
                cmds.setAttr("{}.rotateX".format(heel_pivot),-180)
            heel_param = cmds.duplicate(heel_pivot,n="heelPivotParam_{}_loc_{}".format(side_l,number_l_l))[0]
            bank_int_pivot = cmds.duplicate(bank_int,n="bankIntPivot_{}_loc_{}".format(side_l,number_l_l))[0]
            if "r" in side_l:
                cmds.setAttr("{}.rotateX".format(bank_int_pivot),-180)
            bank_ext_pivot = cmds.duplicate(bank_ext,n="bankExtPivot_{}_loc_{}".format(side_l,number_l_l))[0]
            if "r" in side_l:
                cmds.setAttr("{}.rotateX".format(bank_ext_pivot),-180)
            
            cmds.parent(ankle,ball_pivot)
            cmds.parent(ball_pivot,ball_pivot_param)
            cmds.parent(ball_pivot_param,toe_pivot)
            cmds.parent(toe_pivot,toe_pivot_param)
            cmds.parent(toe_pivot_param,heel_pivot)
            cmds.parent(heel_pivot,heel_param)
            cmds.parent(heel_param,bank_int_pivot)
            cmds.parent(bank_int_pivot,bank_ext_pivot)
            cmds.parent(bank_ext_pivot,foot_ik_ctr)
        
            # 8.6.2 Configuracion del ctrToe
            footfk_toepivot_cns = cmds.parentConstraint(foot_fk_ctr,toe_pivot,toe_offset,mo=True,n="footFKToePivotParent_{}_cns_{}".format(side_l,number_l_l))[0]
            leg_ik_rev = cmds.createNode("reverse",n="legIk_{}_rev_{}".format(side_l,number_l_l))
            cmds.connectAttr("{}.legIK".format(leg_settings_ctr),"{}.inputX".format(leg_ik_rev))
            cmds.connectAttr("{}.outputX".format(leg_ik_rev),"{}.{}W0".format(footfk_toepivot_cns,foot_fk_ctr))
            cmds.connectAttr("{}.legIK".format(leg_settings_ctr),"{}.{}W1".format(footfk_toepivot_cns,toe_pivot))                 
        
            # 8.6.3 Configuracion del FootTilt
            bank_ext_clamp = cmds.createNode("clamp",n="bankExt_{}_clamp_{}".format(side_l,number_l_l))
            cmds.setAttr("{}.maxR".format(bank_ext_clamp),999)
            cmds.connectAttr("{}.footTilt".format(foot_ik_ctr),"{}.inputR".format(bank_ext_clamp))
            
            bank_ext_mult = cmds.createNode("multiplyDivide",n="bankExt_{}_mult_{}".format(side_l,number_l_l))
            if "l" in side_l:
                cmds.setAttr("{}.input2X".format(bank_ext_mult),-1)
            if "r" in side_l:
                cmds.setAttr("{}.input2X".format(bank_ext_mult),1)
            cmds.connectAttr("{}.outputR".format(bank_ext_clamp),"{}.input1X".format(bank_ext_mult))
            cmds.connectAttr("{}.outputX".format(bank_ext_mult),"{}.rotateZ".format(bank_ext_pivot))
            
            bank_int_clamp = cmds.createNode("clamp",n="bankInt_{}_clamp_{}".format(side_l,number_l_l))
            cmds.setAttr("{}.minR".format(bank_int_clamp),-999)
            cmds.connectAttr("{}.footTilt".format(foot_ik_ctr),"{}.inputR".format(bank_int_clamp))
            
            bank_int_mult = cmds.createNode("multiplyDivide",n="bankInt_{}_mult_{}".format(side_l,number_l_l))
            cmds.setAttr("{}.input2X".format(bank_int_mult),-1)
            cmds.connectAttr("{}.outputR".format(bank_int_clamp),"{}.input1X".format(bank_int_mult))
            cmds.connectAttr("{}.outputX".format(bank_int_mult),"{}.rotateZ".format(bank_int_pivot))
        
            # 8.6.4 Configuracion del heelPivot
            heel_roll_clamp = cmds.createNode("clamp",n="heelRoll_{}_clamp_{}".format(side_l,number_l_l))
            cmds.setAttr("{}.minR".format(heel_roll_clamp),-999)
            cmds.connectAttr("{}.footRoll".format(foot_ik_ctr),"{}.inputR".format(heel_roll_clamp))
            cmds.connectAttr("{}.outputR".format(heel_roll_clamp),"{}.rotateX".format(heel_pivot))
            
            # 8.6.5 Configuracion del toePivot
            toe_roll_clamp = cmds.createNode("clamp",n="toeRoll_{}_clamp_{}".format(side_l,number_l_l))
            cmds.setAttr("{}.maxR".format(toe_roll_clamp),999)
            cmds.connectAttr("{}.toeBreak".format(foot_ik_ctr),"{}.minR".format(toe_roll_clamp))
            cmds.connectAttr("{}.footRoll".format(foot_ik_ctr),"{}.inputR".format(toe_roll_clamp))
            
            toe_roll_sub = cmds.createNode("plusMinusAverage",n="toeRoll_{}_sub_{}".format(side_l,number_l_l))
            cmds.setAttr("{}.operation".format(toe_roll_sub),2)
            cmds.connectAttr("{}.outputR".format(toe_roll_clamp),"{}.input2D[0].input2Dx".format(toe_roll_sub))
            cmds.connectAttr("{}.toeBreak".format(foot_ik_ctr),"{}.input2D[1].input2Dx".format(toe_roll_sub))
            
            cmds.connectAttr("{}.output2D.output2Dx".format(toe_roll_sub),"{}.rotateX".format(toe_pivot))
        
            #8.6.6 Configuracion del ballPivot
            angle_toe_break_sub = cmds.createNode("plusMinusAverage",n="angleToeBreak_{}_sub_{}".format(side_l,number_l_l))
            cmds.setAttr("{}.operation".format(angle_toe_break_sub),2)
            cmds.connectAttr("{}.releaseAngle".format(foot_ik_ctr),"{}.input2D[0].input2Dx".format(angle_toe_break_sub))
            cmds.connectAttr("{}.toeBreak".format(foot_ik_ctr),"{}.input2D[1].input2Dx".format(angle_toe_break_sub))
            
            toe_break_resta_div = cmds.createNode("multiplyDivide",n="toeBreakResta_{}_div_{}".format(side_l,number_l_l))
            cmds.setAttr("{}.operation".format(toe_break_resta_div),2)
            cmds.connectAttr("{}.toeBreak".format(foot_ik_ctr),"{}.input1X".format(toe_break_resta_div))
            cmds.connectAttr("{}.output2Dx".format(angle_toe_break_sub),"{}.input2X".format(toe_break_resta_div))
            
            toe_factor_mult = cmds.createNode("multiplyDivide",n="toeFactor_{}_mult_{}".format(side_l,number_l_l))
            cmds.connectAttr("{}.output2Dx".format(toe_roll_sub),"{}.input1X".format(toe_factor_mult))
            cmds.connectAttr("{}.outputX".format(toe_break_resta_div),"{}.input2X".format(toe_factor_mult))
            
            toe_roll_clamped = cmds.createNode("clamp",n="toeRollClamped_{}_clamp_{}".format(side_l,number_l_l))
            cmds.connectAttr("{}.toeBreak".format(foot_ik_ctr),"{}.maxR".format(toe_roll_clamped))
            cmds.connectAttr("{}.outputX".format(toe_factor_mult),"{}.inputR".format(toe_roll_clamped))
            
            ball_roll_clamp = cmds.createNode("clamp",n="ballRoll_{}_clamp_{}".format(side_l,number_l_l))
            cmds.connectAttr("{}.toeBreak".format(foot_ik_ctr),"{}.maxR".format(ball_roll_clamp))
            cmds.connectAttr("{}.footRoll".format(foot_ik_ctr),"{}.inputR".format(ball_roll_clamp))
            
            ball_roll_release_sub = cmds.createNode("plusMinusAverage",n="ballRollRelease_{}_sub_{}".format(side_l,number_l_l))
            cmds.setAttr("{}.operation".format(ball_roll_release_sub),2)
            cmds.connectAttr("{}.outputR".format(ball_roll_clamp),"{}.input2D[0].input2Dx".format(ball_roll_release_sub))
            cmds.connectAttr("{}.outputR".format(toe_roll_clamped),"{}.input2D[1].input2Dx".format(ball_roll_release_sub))
            
            cmds.connectAttr("{}.output2Dx".format(ball_roll_release_sub),"{}.rotateX".format(ball_pivot))
        
            # 8.6.7 Configuracion del heelRoll, ballRoll, toeRoll, toeSlide
            cmds.connectAttr("{}.heelRoll".format(foot_ik_ctr),"{}.rotateX".format(heel_param))
            cmds.connectAttr("{}.ballRoll".format(foot_ik_ctr),"{}.rotateX".format(ball_pivot_param))
            cmds.connectAttr("{}.toeRoll".format(foot_ik_ctr),"{}.rotateX".format(toe_pivot_param))
            cmds.connectAttr("{}.toeSlide".format(foot_ik_ctr),"{}.rotateY".format(toe_pivot_param))
            
            Hide(bank_ext_pivot)
        
            # 8.7.1 Creacion de los joints PAC
            hip_pac = cmds.duplicate(hip_jnt,po=True,n="hipPac_{}_jnt_{}".format(side_l,number_l_l))[0]
            hip_pac_offset = CreateOffset(hip_pac,number_l_l)
            cmds.parent(hip_pac_offset,hip_fk_ctr)
            
            knee_pac = cmds.duplicate(knee_jnt,po=True,n="kneePac_{}_jnt_{}".format(side_l,number_l_l))[0]
            knee_pac_offest = CreateOffset(knee_pac,number_l_l)
            cmds.parent(knee_pac_offest,knee_fk_ctr)
            
            foot_fk_pac = cmds.duplicate(foot_jnt,po=True,n="footFkPac_{}_jnt_{}".format(side_l,number_l_l))[0]
            foot_fk_pac_offest = CreateOffset(foot_fk_pac,number_l_l)
            cmds.parent(foot_fk_pac_offest,foot_fk_ctr)
            
            foot_ik_pac = cmds.duplicate(foot_jnt,po=True,n="footIkPac_{}_jnt_{}".format(side_l,number_l_l))[0]
            foot_ik_pac_offest = CreateOffset(foot_ik_pac,number_l_l)
            cmds.parent(foot_ik_pac_offest,ankle)
            
            ball_pac = cmds.duplicate(ball_jnt,po=True,n="ballPac_{}_jnt_{}".format(side_l,number_l_l))[0]
            ball_pac_offest = CreateOffset(ball_pac,number_l_l)
            cmds.parent(ball_pac_offest,toe_ctr)
        
            # 8.7.2 Relaciones basicas entre controles, huesos e ikHandles
            cmds.pointConstraint(foot_ik_pac,leg_main_ik,mo=False,n="footIkPacHandlePoint_{}_cns_{}".format(side_l,number_l_l))
            cmds.poleVectorConstraint(leg_pole_ctr,leg_main_ik,n="poleVectorIkHandlePole_{}_cns_{}".format(side_l,number_l_l))
            cmds.orientConstraint(hip_pac,hip_jnt,mo=True,n="hipPacOrient_{}_cns_{}".format(side_l,number_l_l))
            cmds.cycleCheck(e=False)
            cmds.orientConstraint(knee_pac,knee_jnt,mo=True,n="kneePacOrient_{}_cns_{}".format(side_l,number_l_l))
            ball_pac_cns = cmds.orientConstraint(ball_pac,ball_jnt,mo=True,n="ballPacOrient_{}_cns_{}".format(side_l,number_l_l))[0]
            cmds.setAttr("{}.interpType".format(ball_pac_cns),2)
            cmds.pointConstraint(hip_ctr,hip_jnt,mo=True,n="hipPoint_{}_cns_{}".format(side_l,number_l_l))
            cmds.parentConstraint(foot_jnt,leg_settings_ctr,mo=True,n="footLegSettingsPoint_{}_cns_{}".format(side_l,number_l_l))
            foot_fk_ik_orient_cns = cmds.orientConstraint(foot_fk_pac,foot_ik_pac,foot_jnt,mo=True,n="footFkIkOrient_{}_cns_{}".format(side_l,number_l_l))[0]
        
            # 8.7.3 Conexiones para realizar el switch FK/IK
            cmds.connectAttr("{}.legIK".format(leg_settings_ctr),"{}.ikBlend".format(leg_main_ik))
            cmds.connectAttr("{}.legIK".format(leg_settings_ctr),"{}.{}W1".format(foot_fk_ik_orient_cns,foot_ik_pac))
            cmds.connectAttr("{}.outputX".format(leg_ik_rev),"{}.{}W0".format(foot_fk_ik_orient_cns,foot_fk_pac))
            cmds.cycleCheck(e=True)
            cmds.connectAttr("{}.legIK".format(leg_settings_ctr),"{}.visibility".format(foot_ik_offset))
            cmds.connectAttr("{}.legIK".format(leg_settings_ctr),"{}.visibility".format(leg_pole_offset))
            cmds.connectAttr("{}.outputX".format(leg_ik_rev),"{}.visibility".format(hip_fk_offset))
            
            # 8.7.4 Otras conexiones
            cmds.connectAttr("{}.knee".format(foot_ik_ctr),"{}.twist".format(leg_main_ik))
        
            # 8.8.1 Configuracion del squash/Stretch: Creacion de lo locators para medir las distancias.
            hip_stretch = cmds.duplicate(hip,n="hipStretch_{}_loc_{}".format(side_l,number_l_l))[0]
            cmds.xform(hip_stretch,ro=(0,0,0),ws=True)
            cmds.parent(hip_stretch,hip_ctr)
            
            knee_stretch = cmds.duplicate(knee,n="kneeStretch_{}_loc_{}".format(side_l,number_l_l))[0]
            cmds.xform(knee_stretch,ro=(0,0,0),ws=True)
            cmds.parent(knee_stretch,leg_pole_ctr)
            
            foot_stretch = cmds.spaceLocator(n="footStretch_{}_loc_{}".format(side_l,number_l_l))[0]
            cmds.matchTransform(foot_stretch,foot_ik_ctr,pos=True,rot=False,scl=False)
            cmds.parent(foot_stretch,ball_pivot)
        
            # 8.8.2 Conectar los locators con los nodos distance
            upleg_distance = cmds.createNode("distanceBetween",n="upleg_{}_dist_{}".format(side_l,number_l_l))
            cmds.connectAttr("{}.worldPosition[0]".format(hip_stretch),"{}.point1".format(upleg_distance))
            cmds.connectAttr("{}.worldPosition[0]".format(knee_stretch),"{}.point2".format(upleg_distance))
            
            lowleg_distance = cmds.createNode("distanceBetween",n="lowleg_{}_dist_{}".format(side_l,number_l_l))
            cmds.connectAttr("{}.worldPosition[0]".format(knee_stretch),"{}.point1".format(lowleg_distance))
            cmds.connectAttr("{}.worldPosition[0]".format(foot_stretch),"{}.point2".format(lowleg_distance))
            
            entire_leg_distance = cmds.createNode("distanceBetween",n="entireLeg_{}_dist_{}".format(side_l,number_l_l))
            cmds.connectAttr("{}.worldPosition[0]".format(hip_stretch),"{}.point1".format(entire_leg_distance))
            cmds.connectAttr("{}.worldPosition[0]".format(foot_stretch),"{}.point2".format(entire_leg_distance))
        
            # 8.8.3 Configurar el stretch IK y normalizarlo
            leg_normal_stretch_div = cmds.createNode("multiplyDivide",n="legNormalStretch_{}_div_{}".format(side_l,number_l_l))
            cmds.setAttr("{}.operation".format(leg_normal_stretch_div),2)
            cmds.connectAttr("{}.distance".format(entire_leg_distance),"{}.input1X".format(leg_normal_stretch_div))
            entire_leg_dist_value = cmds.getAttr("{}.distance".format(entire_leg_distance))
            cmds.setAttr("{}.input2X".format(leg_normal_stretch_div),entire_leg_dist_value)
            
            leg_stretch_clamp = cmds.createNode("clamp",n="legStretch_{}_clamp_{}".format(side_l,number_l_l))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.minR".format(leg_stretch_clamp))
            cmds.setAttr("{}.maxR".format(leg_stretch_clamp),999)
            cmds.connectAttr("{}.outputX".format(leg_normal_stretch_div),"{}.inputR".format(leg_stretch_clamp))
            
            upleg_stretch_div = cmds.createNode("multiplyDivide",n="uplegStretch_{}_div_{}".format(side_l,number_l_l))
            cmds.setAttr("{}.operation".format(upleg_stretch_div),2)
            cmds.connectAttr("{}.distance".format(upleg_distance),"{}.input1X".format(upleg_stretch_div))
            upleg_dist_value = cmds.getAttr("{}.distance".format(upleg_distance))
            cmds.setAttr("{}.input2X".format(upleg_stretch_div),upleg_dist_value)
            
            lowleg_stretch_div = cmds.createNode("multiplyDivide",n="lowlegStretch_{}_div_{}".format(side_l,number_l_l))
            cmds.setAttr("{}.operation".format(lowleg_stretch_div),2)
            cmds.connectAttr("{}.distance".format(lowleg_distance),"{}.input1X".format(lowleg_stretch_div))
            lowleg_dist_value = cmds.getAttr("{}.distance".format(lowleg_distance))
            cmds.setAttr("{}.input2X".format(lowleg_stretch_div),lowleg_dist_value)
            
            leg_ikstretch_blend = cmds.createNode("blendColors",n="legIkStretch_{}_blend_{}".format(side_l,number_l_l))
            cmds.connectAttr("{}.outputX".format(upleg_stretch_div),"{}.color1G".format(leg_ikstretch_blend))
            cmds.connectAttr("{}.outputX".format(lowleg_stretch_div),"{}.color1B".format(leg_ikstretch_blend))
            cmds.connectAttr("{}.outputR".format(leg_stretch_clamp),"{}.color2G".format(leg_ikstretch_blend))
            cmds.connectAttr("{}.outputR".format(leg_stretch_clamp),"{}.color2B".format(leg_ikstretch_blend))
            
            leg_final_stretch_blend = cmds.createNode("blendColors",n="legFinalStretch_{}_blend_{}".format(side_l,number_l_l))
            cmds.connectAttr("{}.legIK".format(leg_settings_ctr),"{}.blender".format(leg_final_stretch_blend))
            cmds.connectAttr("{}.outputG".format(leg_ikstretch_blend),"{}.color1G".format(leg_final_stretch_blend))
            cmds.connectAttr("{}.outputB".format(leg_ikstretch_blend),"{}.color1B".format(leg_final_stretch_blend))
            cmds.setAttr("{}.color2G".format(leg_final_stretch_blend),1)
            cmds.setAttr("{}.color2B".format(leg_final_stretch_blend),1)
        
            # 8.8.4 Cofigurar el autoStretch
            leg_stretchiness_blend = cmds.createNode("blendColors",n="legStretchiness_{}_blend_{}".format(side_l,number_l_l))
            cmds.connectAttr("{}.outputG".format(leg_final_stretch_blend),"{}.color1G".format(leg_stretchiness_blend))
            cmds.connectAttr("{}.outputB".format(leg_final_stretch_blend),"{}.color1B".format(leg_stretchiness_blend))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.color2G".format(leg_stretchiness_blend))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.color2B".format(leg_stretchiness_blend))
            
            leg_stretch_by_global_div = cmds.createNode("multiplyDivide",n="legStretchByGlobal_{}_div_{}".format(side_l,number_l_l))
            cmds.setAttr("{}.operation".format(leg_stretch_by_global_div),2)
            cmds.connectAttr("{}.outputG".format(leg_stretchiness_blend),"{}.input1X".format(leg_stretch_by_global_div))
            cmds.connectAttr("{}.outputB".format(leg_stretchiness_blend),"{}.input1Y".format(leg_stretch_by_global_div))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.input2X".format(leg_stretch_by_global_div))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.input2Y".format(leg_stretch_by_global_div))
            
            footik_autostretch_override_sum = cmds.createNode("plusMinusAverage",n="footIkAutoStretchOverride_{}_sum_{}".format(side_l,number_l_l))
            cmds.connectAttr("{}.outputX".format(leg_ik_rev),"{}.input2D[0].input2Dx".format(footik_autostretch_override_sum))
            cmds.connectAttr("{}.autoStretch".format(foot_ik_ctr),"{}.input2D[1].input2Dx".format(footik_autostretch_override_sum))
            
            footik_finalstretchiness_clamp = cmds.createNode("clamp",n="footIkFinalStretchiness_{}_clamp_{}".format(side_l,number_l_l))
            cmds.setAttr("{}.maxR".format(footik_finalstretchiness_clamp),1)
            cmds.connectAttr("{}.output2Dx".format(footik_autostretch_override_sum),"{}.inputR".format(footik_finalstretchiness_clamp))
            cmds.connectAttr("{}.outputR".format(footik_finalstretchiness_clamp),"{}.blender".format(leg_stretchiness_blend))
            
            # 8.8.5 Conectar con las escalas de los huesos
            cmds.connectAttr("{}.outputX".format(leg_stretch_by_global_div),"{}.scaleX".format(hip_jnt))
            cmds.connectAttr("{}.outputY".format(leg_stretch_by_global_div),"{}.scaleX".format(knee_jnt))
            
            # 8.8.6 Configurar el stretch Fk
            hipfk_stretchbyglobal_mult = cmds.createNode("multiplyDivide",n="hipFkStretchByGlobal_{}_mult_{}".format(side_l,number_l_l))
            cmds.connectAttr("{}.stretch".format(hip_fk_ctr),"{}.input1X".format(hipfk_stretchbyglobal_mult))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.input2X".format(hipfk_stretchbyglobal_mult))
            cmds.connectAttr("{}.outputX".format(hipfk_stretchbyglobal_mult),"{}.color2G".format(leg_final_stretch_blend))
            cmds.cycleCheck(e=False)
            cmds.pointConstraint(knee_jnt,knee_fk_offset,n="kneeToFkOffsetPoint_{}_cns_{}".format(side_l,number_l_l))
            
            kneefk_stretchbyglobal_mult = cmds.createNode("multiplyDivide",n="kneeFkStretchByGlobal_{}_mult_{}".format(side_l,number_l_l))
            cmds.connectAttr("{}.stretch".format(knee_fk_ctr),"{}.input1X".format(kneefk_stretchbyglobal_mult))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.input2X".format(kneefk_stretchbyglobal_mult))
            cmds.connectAttr("{}.outputX".format(kneefk_stretchbyglobal_mult),"{}.color2B".format(leg_final_stretch_blend))
            
            cmds.pointConstraint(leg_end_jnt,foot_fk_offset,n="legEndToFkOffsetPoint_{}_cns_{}".format(side_l,number_l_l))
        
        
            # 8.8.7 Conectar los joints del twistUplegChain con el stretch
            upleg_twist_stretch_ci = cmds.createNode("curveInfo",n="uplegTwistStretch_{}_ci_{}".format(side_l,number_l_l))
            cmds.connectAttr("{}.worldSpace[0]".format(upleg_twist_crv),"{}.inputCurve".format(upleg_twist_stretch_ci))
            
            upleg_ikcurvelength_div = cmds.createNode("multiplyDivide",n="uplegIkCurveLength_{}_div_{}".format(side_l,number_l_l))
            cmds.setAttr("{}.operation".format(upleg_ikcurvelength_div),2)
            cmds.connectAttr("{}.arcLength".format(upleg_twist_stretch_ci),"{}.input1X".format(upleg_ikcurvelength_div))
            upleg_curvelength = cmds.getAttr("{}.arcLength".format(upleg_twist_stretch_ci))
            cmds.setAttr("{}.input2X".format(upleg_ikcurvelength_div),upleg_curvelength)
            
            upleg_lengthbyglobal_div = cmds.createNode("multiplyDivide",n="uplegLengthByGlobal_{}_div_{}".format(side_l,number_l_l))
            cmds.setAttr("{}.operation".format(upleg_lengthbyglobal_div),2) 
            cmds.connectAttr("{}.outputX".format(upleg_ikcurvelength_div),"{}.input1X".format(upleg_lengthbyglobal_div))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.input2X".format(upleg_lengthbyglobal_div))
            
            n_jnt_upleg_twist = len(new_upleg_twist_list)
            upleg_twist_stretch_list = new_upleg_twist_list[0:n_jnt_upleg_twist-1]
            for upleg_twist_stretch_jnt in upleg_twist_stretch_list:
                cmds.connectAttr("{}.outputX".format(upleg_lengthbyglobal_div),"{}.scaleX".format(upleg_twist_stretch_jnt))
        
            # 8.8.8 Conectar los joints del twistLowLegChain con el stretch.
            lowleg_twist_stretch_ci = cmds.createNode("curveInfo",n="lowlegTwistStretch_{}_ci_{}".format(side_l,number_l_l))
            cmds.connectAttr("{}.worldSpace[0]".format(lowleg_twist_crv),"{}.inputCurve".format(lowleg_twist_stretch_ci))
            
            lowleg_ikcurvelength_div = cmds.createNode("multiplyDivide",n="lowlegIkCurveLength_{}_div_{}".format(side_l,number_l_l))
            cmds.setAttr("{}.operation".format(lowleg_ikcurvelength_div),2)
            cmds.connectAttr("{}.arcLength".format(lowleg_twist_stretch_ci),"{}.input1X".format(lowleg_ikcurvelength_div))
            lowleg_curvelength = cmds.getAttr("{}.arcLength".format(lowleg_twist_stretch_ci))
            cmds.setAttr("{}.input2X".format(lowleg_ikcurvelength_div),lowleg_curvelength)
            
            lowleg_lengthbyglobal_div = cmds.createNode("multiplyDivide",n="lowlegLengthByGlobal_{}_div_{}".format(side_l,number_l_l))
            cmds.setAttr("{}.operation".format(lowleg_lengthbyglobal_div),2) 
            cmds.connectAttr("{}.outputX".format(lowleg_ikcurvelength_div),"{}.input1X".format(lowleg_lengthbyglobal_div))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.input2X".format(lowleg_lengthbyglobal_div))
            
            n_jnt_lowleg_twist = len(new_lowleg_twist_list)
            lowleg_twist_stretch_list = new_lowleg_twist_list[0:n_jnt_lowleg_twist-1]
            for lowleg_twist_stretch_jnt in lowleg_twist_stretch_list:
                cmds.connectAttr("{}.outputX".format(lowleg_lengthbyglobal_div),"{}.scaleX".format(lowleg_twist_stretch_jnt))
            cmds.cycleCheck(e=True)
        
            # 8.8.9 Conectar el pinKnee
            pinknee_byik_mult = cmds.createNode("multiplyDivide",n="pinKneeByIk_{}_mult_{}".format(side_l,number_l_l))
            cmds.connectAttr("{}.pinKnee".format(leg_pole_ctr),"{}.input1X".format(pinknee_byik_mult))
            cmds.connectAttr("{}.legIK".format(leg_settings_ctr),"{}.input2X".format(pinknee_byik_mult))
            cmds.connectAttr("{}.outputX".format(pinknee_byik_mult),"{}.blender".format(leg_ikstretch_blend))
            cmds.connectAttr("{}.outputX".format(pinknee_byik_mult),"{}.input2D[2].input2Dx".format(footik_autostretch_override_sum))
            
            # 8.8.10 Reposicionar el kneeStretchLoc en el ctrLegPole
            cmds.matchTransform(knee_stretch,leg_pole_ctr,pos=True,rot=False,scl=False)
            
            Hide(knee_stretch)
            # 8.8.11 Configuracion del autoSquash
            legstretch_byglobal_inv_div = cmds.createNode("multiplyDivide",n="legStretchByGlobalInv_{}_div_{}".format(side_l,number_l_l))
            cmds.setAttr("{}.operation".format(legstretch_byglobal_inv_div),2)
            cmds.connectAttr("{}.outputX".format(leg_stretch_by_global_div),"{}.input2X".format(legstretch_byglobal_inv_div))
            cmds.connectAttr("{}.outputY".format(leg_stretch_by_global_div),"{}.input2Y".format(legstretch_byglobal_inv_div))
            cmds.setAttr("{}.input1X".format(legstretch_byglobal_inv_div),1)
            cmds.setAttr("{}.input1Y".format(legstretch_byglobal_inv_div),1)
            
            leg_autosquash_blend = cmds.createNode("blendColors",n="legAutoSquash_{}_blend_{}".format(side_l,number_l_l))
            cmds.connectAttr("{}.autoSquash".format(leg_settings_ctr),"{}.blender".format(leg_autosquash_blend))
            cmds.connectAttr("{}.outputX".format(legstretch_byglobal_inv_div),"{}.color1G".format(leg_autosquash_blend))
            cmds.connectAttr("{}.outputY".format(legstretch_byglobal_inv_div),"{}.color1B".format(leg_autosquash_blend))
            cmds.setAttr("{}.color2G".format(leg_autosquash_blend),1)
            cmds.setAttr("{}.color2B".format(leg_autosquash_blend),1)
            
            for upleg_twist_jnt in new_upleg_twist_list:
                cmds.connectAttr("{}.outputG".format(leg_autosquash_blend),"{}.scaleY".format(upleg_twist_jnt))
                cmds.connectAttr("{}.outputG".format(leg_autosquash_blend),"{}.scaleZ".format(upleg_twist_jnt))
            
            for lowleg_twist_jnt in new_lowleg_twist_list:
                cmds.connectAttr("{}.outputB".format(leg_autosquash_blend),"{}.scaleY".format(lowleg_twist_jnt))
                cmds.connectAttr("{}.outputB".format(leg_autosquash_blend),"{}.scaleZ".format(lowleg_twist_jnt))
        
            # 8.9.1 Creacion del sistema bend: Reconstruccion de las curvas
            upleg_twist_crv = cmds.rebuildCurve(upleg_twist_crv,ch=1,rpo=1,rt=0,end=1,kr=0,kcp=0,kep=1,kt=0,s=1,d=3,tol=0.01)[0] 
            lowleg_twist_crv = cmds.rebuildCurve(lowleg_twist_crv,ch=1,rpo=1,rt=0,end=1,kr=0,kcp=0,kep=1,kt=0,s=1,d=3,tol=0.01)[0]
            
            # 8.9.2 Creacion de los clusters
            legbend_cluster_a =cmds.cluster("{}.cv[0]".format(upleg_twist_crv),n="legBendA_{}_cl_{}".format(side_l,number_l_l))[1]
            legbend_cluster_b =cmds.cluster("{}.cv[1:2]".format(upleg_twist_crv),n="legBendB_{}_cl_{}".format(side_l,number_l_l))[1]
            legbend_cluster_c =cmds.cluster("{}.cv[3]".format(upleg_twist_crv),"{}.cv[0]".format(lowleg_twist_crv),n="lowBendC_{}_cl_{}".format(side_l,number_l_l))[1]
            legbend_cluster_d =cmds.cluster("{}.cv[1:2]".format(lowleg_twist_crv),n="legBendD_{}_cl_{}".format(side_l,number_l_l))[1]
            legbend_cluster_e =cmds.cluster("{}.cv[3]".format(lowleg_twist_crv),n="legBendE_{}_cl_{}".format(side_l,number_l_l))[1]
        
            # 8.9.3 Creacion de controles Bend
            cmds.parent(legbend_cluster_a,hip_jnt)
            cmds.parent(legbend_cluster_e,foot_jnt)
            
            upleg_bend_ctr = cmds.duplicate("uplegBend_{}_ctr_0".format(side_l),n="uplegBend_{}_ctr_{}".format(side_l,number_l_l))[0]
            upleg_bend_offset = CreateOffset(upleg_bend_ctr,number_l_l)
            cmds.matchTransform(upleg_bend_offset,legbend_cluster_b,pos=True,rot=False,scl=False)
            cmds.parent(legbend_cluster_b,upleg_bend_ctr)
            cmds.parent(upleg_bend_offset,hip_jnt)
            
            knee_bend_ctr = cmds.duplicate("kneeBend_{}_ctr_0".format(side_l),n="kneeBend_{}_ctr_{}".format(side_l,number_l_l))[0]
            knee_bend_offset = CreateOffset(knee_bend_ctr,number_l_l)
            cmds.matchTransform(knee_bend_offset,legbend_cluster_c,pos=True,rot=False,scl=False)
            cmds.parent(legbend_cluster_c,knee_bend_ctr)
            cmds.parent(knee_bend_offset,char_skeleton)
            
            lowleg_bend_ctr = cmds.duplicate("lowlegBend_{}_ctr_0".format(side_l),n="lowlegBend_{}_ctr_{}".format(side_l,number_l_l))[0]
            lowleg_bend_offset = CreateOffset(lowleg_bend_ctr,number_l_l)
            cmds.matchTransform(lowleg_bend_offset,legbend_cluster_d,pos=True,rot=False,scl=False)
            cmds.parent(legbend_cluster_d,lowleg_bend_ctr)
            cmds.parent(lowleg_bend_offset,knee_jnt)
            
            # 8.9.4 Creacion de las relaciones entre los controles y los huesos
            cmds.parentConstraint(knee_jnt,knee_bend_offset,mo=True,n="KneeBendParent_{}_cns_{}".format(side_l,number_l_l))
            
            if spine_leg_conexion is True:
                # 8.10.1 Conexion entre modulos(pelvis): Emparentamientos
                cmds.parent(hip_jnt_offset,"pelvis_c_skn_{}".format(spine_leg_conexion_value))
                       
            # 8.10.2 Configuracion del hipFKPCon
            hip_fk_pcon = cmds.duplicate(hip_fk_offset,po=True,n="hipFk_{}_pcon_{}".format(side_l,number_l_l))
            cmds.parent(hip_fk_pcon,hip_ctr)
            cmds.pointConstraint(hip_fk_pcon,hip_fk_offset,n="hipFkPconPoint_{}_cns_{}".format(side_l,number_l_l))
            
            # 8.10.3 Parent Constraint
            cmds.parentConstraint(hip_ctr,upleg_roll_system,mo=True,n="hipUplegRollSystem_{}_cns_{}".format(side_l,number_l_l))
            
            leg_spaces_bool = win.checkBoxLegSpaces.isChecked()
            leg_space_spine_value = win.spinLegConexion.value()
            
            if leg_spaces_bool is True:
                # 8.11.1 Configuracion de los spaces en ctrHipFk
                cmds.addAttr(hip_fk_ctr,ln= "__", at="enum",en="spaces")
                cmds.setAttr ("{}.__".format(hip_fk_ctr),channelBox= True)    
                cmds.addAttr(hip_fk_ctr,ln= "pelvisSpace",at= "double",min= 0,max=1,dv=0,k=True)
                
                hip_fk_worldspace = cmds.duplicate(hip_fk_offset,po=True,n="hipFkWorldSpace_{}_grp_{}".format(side_l,number_l_l))[0]
                hip_fk_pelvisspace = cmds.duplicate(hip_fk_offset,po=True,n="hipFkPelvisSpace_{}_grp_{}".format(side_l,number_l_l))[0]
                
                hip_fk_spaces_cns = cmds.orientConstraint(hip_fk_worldspace,hip_fk_pelvisspace,hip_fk_offset,mo=False,n="hipFkSpacesOrient_{}_cns_{}".format(side_l,number_l_l))[0]
                cmds.parent(hip_fk_pelvisspace,"pelvis_c_ctr_{}".format(leg_space_spine_value))
                
                cmds.connectAttr("{}.pelvisSpace".format(hip_fk_ctr),"{}.{}W1".format(hip_fk_spaces_cns,hip_fk_pelvisspace))
                hip_fk_dynparent_rev = cmds.createNode("reverse",n="hipFkDynParent_{}_rev_{}".format(side_l,number_l_l))
                cmds.connectAttr("{}.pelvisSpace".format(hip_fk_ctr),"{}.inputX".format(hip_fk_dynparent_rev))
                cmds.connectAttr("{}.outputX".format(hip_fk_dynparent_rev),"{}.{}W0".format(hip_fk_spaces_cns,hip_fk_worldspace))
        
                # 8.11.2 Configuracion de los spaces en ctrFootIK
                cmds.addAttr(foot_ik_ctr,ln= "__", at="enum",en="spaces")
                cmds.setAttr ("{}.__".format(foot_ik_ctr),channelBox= True)    
                cmds.addAttr(foot_ik_ctr,ln= "pelvisSpace",at= "double",min= 0,max=1,dv=0,k=True)
                
                foot_ik_worldspace = cmds.duplicate(foot_ik_offset,po=True,n="footIkWorldSpace_{}_grp_{}".format(side_l,number_l_l))[0]
                foot_ik_pelvisspace = cmds.duplicate(foot_ik_offset,po=True,n="footIkPelvisSpace_{}_grp_{}".format(side_l,number_l_l))[0]
                
                foot_ik_spaces_cns = cmds.parentConstraint(foot_ik_worldspace,foot_ik_pelvisspace,foot_ik_offset,mo=False,n="footIkSpacesParent_{}_cns_{}".format(side_l,number_l_l))[0]
                cmds.parent(foot_ik_pelvisspace,"pelvis_c_ctr_{}".format(leg_space_spine_value))
                
                cmds.connectAttr("{}.pelvisSpace".format(foot_ik_ctr),"{}.{}W1".format(foot_ik_spaces_cns,foot_ik_pelvisspace))
                foot_ik_dynparent_rev = cmds.createNode("reverse",n="footIkDynParent_{}_rev_{}".format(side_l,number_l_l))
                cmds.connectAttr("{}.pelvisSpace".format(foot_ik_ctr),"{}.inputX".format(foot_ik_dynparent_rev))
                cmds.connectAttr("{}.outputX".format(foot_ik_dynparent_rev),"{}.{}W0".format(foot_ik_spaces_cns,foot_ik_worldspace))
                # 8.11.3 Configuracion de los atributos de los spaces en el ctrLegPole
                cmds.addAttr(leg_pole_ctr,ln= "__", at="enum",en="spaces")
                cmds.setAttr ("{}.__".format(leg_pole_ctr),channelBox= True)    
                cmds.addAttr(leg_pole_ctr,ln= "footSpace",at= "double",min= 0,max=1,dv=0,k=True)
                cmds.addAttr(leg_pole_ctr,ln= "pelvisSpace",at= "double",min= 0,max=1,dv=0,k=True)
                
                leg_pole_worldspace = cmds.duplicate(leg_pole_offset,po=True,n="legPoleWorldSpace_{}_grp_{}".format(side_l,number_l_l))[0]
                leg_pole_footspace = cmds.duplicate(leg_pole_offset,po=True,n="legPoleFootSpace_{}_grp_{}".format(side_l,number_l_l))[0]
                leg_pole_pelvisspace = cmds.duplicate(leg_pole_offset,po=True,n="legPolePelvisSpace_{}_grp_{}".format(side_l,number_l_l))[0]
                
                leg_pole_spaces_cns = cmds.parentConstraint(leg_pole_worldspace,leg_pole_footspace,leg_pole_pelvisspace,leg_pole_offset,mo=False,n="legPoleSpacesParent_{}_cns_{}".format(side_l,number_l_l))[0]
                
                cmds.parent(leg_pole_footspace,foot_ik_ctr)
                cmds.parent(leg_pole_pelvisspace,"pelvis_c_ctr_{}".format(leg_space_spine_value))
                
                cmds.connectAttr("{}.footSpace".format(leg_pole_ctr),"{}.{}W1".format(leg_pole_spaces_cns,leg_pole_footspace))
                cmds.connectAttr("{}.pelvisSpace".format(leg_pole_ctr),"{}.{}W2".format(leg_pole_spaces_cns,leg_pole_pelvisspace))
                
                leg_pole_dynparent_sum = cmds.createNode("plusMinusAverage",n="legPoleDynParent_{}_sum_{}".format(side_l,number_l_l))
                cmds.connectAttr("{}.footSpace".format(leg_pole_ctr),"{}.input2D[0].input2Dx".format(leg_pole_dynparent_sum))
                cmds.connectAttr("{}.pelvisSpace".format(leg_pole_ctr),"{}.input2D[1].input2Dx".format(leg_pole_dynparent_sum))
                
                leg_pole_dynparent_clamp = cmds.createNode("clamp",n="legPoleDynParent_{}_clamp_{}".format(side_l,number_l_l))
                cmds.setAttr("{}.maxR".format(leg_pole_dynparent_clamp),1)
                cmds.connectAttr("{}.output2Dx".format(leg_pole_dynparent_sum),"{}.inputR".format(leg_pole_dynparent_clamp))
                
                leg_pole_dynparent_rev = cmds.createNode("reverse",n="legPoleDynParent_{}_rev_{}".format(side_l,number_l_l))
                cmds.connectAttr("{}.outputR".format(leg_pole_dynparent_clamp),"{}.inputX".format(leg_pole_dynparent_rev))
                cmds.connectAttr("{}.outputX".format(leg_pole_dynparent_rev),"{}.{}W0".format(leg_pole_spaces_cns,leg_pole_worldspace))
        
            # Cerrar rig
            cmds.connectAttr("{}.visBends".format(leg_settings_ctr),"{}.visibility".format(upleg_bend_ctr))
            cmds.connectAttr("{}.visBends".format(leg_settings_ctr),"{}.visibility".format(knee_bend_ctr))
            cmds.connectAttr("{}.visBends".format(leg_settings_ctr),"{}.visibility".format(lowleg_bend_ctr))
            Hide(leg_main_ik)
            Hide(hip_non_roll_grp)
            Hide(upleg_twist_ik)
            Hide(lowleg_roll_system)
            Hide(upleg_twist_crv)
            Hide(lowleg_twist_crv)
            Hide(hip_stretch)
            Hide(legbend_cluster_a)
            Hide(legbend_cluster_b)
            Hide(legbend_cluster_c)
            Hide(legbend_cluster_d)
            Hide(legbend_cluster_e)
            last_upleg_twist = cmds.rename(last_upleg_twist,"{}_{}_jnt_{}".format(last_upleg_twist.split("_")[0],side_l,number_l_l))
            last_lowleg_twist = cmds.rename(last_lowleg_twist,"{}_{}_jnt_{}".format(last_lowleg_twist.split("_")[0],side_l,number_l_l))
            LockScaleVis(foot_ik_ctr)
            LockScaleRotVis(hip_ctr)
            LockScaleRotVis(leg_pole_ctr)
            LockScaleRotVis(upleg_bend_ctr)
            LockScaleRotVis(knee_bend_ctr)
            LockScaleRotVis(lowleg_bend_ctr)
            LockScaleTransVis(toe_ctr)
            LockScaleTransVis(hip_fk_ctr)
            LockScaleTransVis(knee_fk_ctr)
            LockScaleTransVis(foot_fk_ctr)
            LockAll(leg_settings_ctr)
            createLegSnap(number_l_l,side_l)
                                            
        win.legLeftButton.clicked.connect(BuildLeftLeg)    
            
        def BuildRightLeg():
            number_upleg_joints = win.spinBoxUplegNumberJoints.value()
            number_lowleg_joints = win.spinBoxLowlegNumberJoints.value()
            side_l = "r"
            hip = "hip_{}_loc_{}".format(side_l,number_l_r)
            knee = "knee_{}_loc_{}".format(side_l,number_l_r)
            foot = "foot_{}_loc_{}".format(side_l,number_l_r)
            ball = "ball_{}_loc_{}".format(side_l,number_l_r)
            toe = "toe_{}_loc_{}".format(side_l,number_l_r)
            heel = "heelPos_{}_loc_{}".format(side_l,number_l_r)
            bank_ext = "bankExtPos_{}_loc_{}".format(side_l,number_l_r)
            bank_int = "bankIntPos_{}_loc_{}".format(side_l,number_l_r)
            # 6.1 Creacion de los huesos y reorientacion de locators
            del_cons = cmds.aimConstraint(knee,
                                         hip,
                                         offset=(0,0,0),
                                         weight=1,
                                         aimVector=(1,0,0),
                                         upVector=(0,1,0),
                                         worldUpType="scene")[0]
            cmds.delete(del_cons)
            del_cons = cmds.aimConstraint(foot,
                                          knee,
                                          offset=(0,0,0),
                                          weight=1,
                                          aimVector=(1,0,0),
                                          upVector=(0,1,0),
                                          worldUpType="scene")[0]
            cmds.delete(del_cons)
            del_cons = cmds.aimConstraint(knee,
                                          foot,
                                          offset=(0,0,0),
                                          weight=1,
                                          aimVector=(-1,0,0),
                                          upVector=(0,1,0),
                                          worldUpType="scene")[0]
            cmds.delete(del_cons)
            
            cmds.select(cl=1)
            hip_jnt = cmds.joint(n="hip_{}_jnt_{}".format(side_l,number_l_r))
            hip_pos = cmds.xform(hip,q=True,matrix=True,ws=True)
            cmds.xform(hip_jnt,matrix=hip_pos,ws=True)
            hip_rot = cmds.getAttr("{}.rotateZ".format(hip_jnt))
            cmds.setAttr("{}.rotateZ".format(hip_jnt),0)
            cmds.setAttr("{}.jointOrientZ".format(hip_jnt),hip_rot)
            
            knee_jnt = cmds.joint(n="knee_{}_jnt_{}".format(side_l,number_l_r))
            knee_pos = cmds.xform(knee,q=True,matrix=True,ws=True)
            cmds.xform(knee_jnt,matrix=knee_pos,ws=True)
            
            leg_end_jnt = cmds.joint(n="legEnd_{}_jnt_{}".format(side_l,number_l_r))
            foot_pos = cmds.xform(foot,q=True,matrix=True,ws=True)
            cmds.xform(leg_end_jnt,matrix=foot_pos,ws=True)
            cmds.setAttr("{}.preferredAngleY".format(knee_jnt),90)
            hip_jnt_offset = CreateOffset(hip_jnt,number_l_r)
            cmds.parent(hip_jnt_offset,char_skeleton)
            
            # 8.1.2 Creacion de la cadena del pie:
            cmds.xform(foot,ro=(0,-90,0),ws=True)
            cmds.xform(ball,ro=(0,-90,0),ws=True)
            cmds.xform(toe,ro=(0,-90,0),ws=True)
            cmds.select(cl=1)
            foot_jnt = cmds.joint(n="foot_{}_skn_{}".format(side_l,number_l_r))
            cmds.matchTransform(foot_jnt,foot,pos=True,rot=True,scl=False)
            for axis in "XYZ":
                foot_rot = cmds.getAttr("{}.rotate{}".format(foot_jnt,axis))
                cmds.setAttr("{}.rotate{}".format(foot_jnt,axis),0)
                cmds.setAttr("{}.jointOrient{}".format(foot_jnt,axis),foot_rot)
            ball_jnt = cmds.joint(n="ball_{}_skn_{}".format(side_l,number_l_r))
            cmds.matchTransform(ball_jnt,ball,pos=True,rot=True,scl=False)
            for axis in "XYZ":
                ball_rot = cmds.getAttr("{}.rotate{}".format(ball_jnt,axis))
                cmds.setAttr("{}.rotate{}".format(ball_jnt,axis),0)
                cmds.setAttr("{}.jointOrient{}".format(ball_jnt,axis),ball_rot)
            toe_jnt = cmds.joint(n="toe_{}_jnt_{}".format(side_l,number_l_r))
            cmds.matchTransform(toe_jnt,toe,pos=True,rot=True,scl=False)
            foot_offset = CreateOffset(foot_jnt,number_l_r)
            cmds.parent(foot_offset,char_skeleton)
            cmds.pointConstraint(leg_end_jnt,foot_offset,n="legEndFootPoint_{}_cns_{}".format(side_l,number_l_r))    
        
            #8.2 Creacion del ikHandle del la cadena principal
            leg_main_ik = cmds.ikHandle( sj=hip_jnt, ee=leg_end_jnt, s="sticky",n="legMainikHandle_{}_ik_{}".format(side_l,number_l_r),sol="ikRPsolver")[0]
            if "l" in side_l:
                cmds.parent(leg_main_ik,leg_l_rig)
            if "r" in side_l:
                cmds.parent(leg_main_ik,leg_r_rig)
            for axis in "XYZ":
                cmds.setAttr("{}.poleVector{}".format(leg_main_ik,axis),0)
            
            # 8.3.1 Configuracion de la cadena NonRoll del Hip
            hip_non_roll = cmds.duplicate(hip_jnt,po=True,n="hipNonRoll_{}_jnt_{}".format(side_l,number_l_r))[0]
            hip_non_roll_end =  cmds.duplicate(knee_jnt,po=True,n="hipNonRollEnd_{}_jnt_{}".format(side_l,number_l_r))[0]
            cmds.setAttr("{}.jointOrientX".format(hip_non_roll),0)
            cmds.parent(hip_non_roll_end,hip_non_roll)
            hip_non_roll_ik = cmds.ikHandle(sj=hip_non_roll, ee=hip_non_roll_end, s="sticky",n="hipNonRollikHandle_{}_ik_{}".format(side_l,number_l_r),sol="ikRPsolver")[0]
            for axis in "XYZ":
                cmds.setAttr("{}.poleVector{}".format(hip_non_roll_ik,axis),0)
            
            if "l" in side_l:
                upleg_roll_system = cmds.group(n="uplegRollSystem_{}_grp_{}".format(side_l,number_l_r),em=1,p=leg_l_rig)
            if "r" in side_l:
                upleg_roll_system = cmds.group(n="uplegRollSystem_{}_grp_{}".format(side_l,number_l_r),em=1,p=leg_r_rig)
            for axis in "XYZ":
                cmds.connectAttr("{}.globalScale".format(control_base),"{}.scale{}".format(upleg_roll_system,axis))
            
            hip_non_roll_grp = cmds.group(n="hipNonRoll_{}_grp_{}".format(side_l,number_l_r),em=1,p=upleg_roll_system)
            
            cmds.parent(hip_non_roll_ik,hip_non_roll_grp)
            cmds.parent(hip_non_roll,hip_non_roll_grp)
            
            cmds.pointConstraint(hip_jnt,hip_non_roll,n="hipNonRollPoint_{}_cns_{}".format(side_l,number_l_r))
            cmds.pointConstraint(knee_jnt,hip_non_roll_ik,n="hipIkNonRollPoint_{}_cns_{}".format(side_l,number_l_r))
        
            # 8.3.2 Configuracion de la cadena NonRoll del Knee
            knee_non_roll = cmds.duplicate(knee_jnt,po=True,n="kneeNonRoll_{}_jnt_{}".format(side_l,number_l_r))[0]
            knee_non_roll_end =  cmds.duplicate(leg_end_jnt,po=True,n="kneeNonRollEnd_{}_jnt_{}".format(side_l,number_l_r))[0]
            cmds.setAttr("{}.jointOrientX".format(knee_non_roll),0)
            cmds.parent(knee_non_roll_end,knee_non_roll)
            knee_non_roll_ik = cmds.ikHandle(sj=knee_non_roll, ee=knee_non_roll_end, s="sticky",n="kneeNonRollikHandle_{}_ik_{}".format(side_l,number_l_r),sol="ikRPsolver")[0]
            for axis in "XYZ":
                cmds.setAttr("{}.poleVector{}".format(knee_non_roll_ik,axis),0)
            if "l" in side_l:
                lowleg_roll_system = cmds.group(n="lowlegRollSystem_{}_grp_{}".format(side_l,number_l_l),em=1,p=leg_l_rig)
            if "r" in side_l:
                lowleg_roll_system = cmds.group(n="lowlegRollSystem_{}_grp_{}".format(side_l,number_l_r),em=1,p=leg_r_rig)
            knee_non_roll_grp = cmds.group(n="kneeNonRoll_{}_grp_{}".format(side_l,number_l_r),em=1,p=lowleg_roll_system)
            
            cmds.parent(knee_non_roll,knee_non_roll_grp)
            cmds.parent(knee_non_roll_ik,knee_non_roll_grp)
            
            cmds.pointConstraint(knee_jnt,knee_non_roll,n="kneeNonRollPoint_{}_cns_{}".format(side_l,number_l_r))
            cmds.pointConstraint(foot_jnt,knee_non_roll_ik,n="kneeNonRollIkPoint_{}_cns_{}".format(side_l,number_l_r))
            
            knee_twist_value = cmds.duplicate(knee_jnt,po=True,n="kneeTwistValue_{}_jnt_{}".format(side_l,number_l_r))[0]
            cmds.parent(knee_twist_value,knee_jnt)
            cmds.aimConstraint(foot_jnt,
                                knee_twist_value,
                                offset=(0,0,0),
                                weight=1,
                                aimVector=(1,0,0),
                                upVector=(0,1,0),
                                worldUpType="objectrotation",
                                worldUpVector=(0,1,0),
                                worldUpObject=knee_non_roll,
                                n="foottoKneeNonAim_{}_cns_{}".format(side_l,number_l_r))
            cmds.parentConstraint(hip_non_roll,knee_non_roll_grp,mo=True,n="hipNonToKneeNonRollGrpParent_{}_cns_{}".format(side_l,number_l_r))
        
            # 8.3.3 Configuracion de la cadena NonRoll del Foot
            foot_non_roll = cmds.duplicate(leg_end_jnt,po=True,n="footNonRoll_{}_jnt_{}".format(side_l,number_l_r))[0] 
            foot_non_roll_end = cmds.duplicate(leg_end_jnt,po=True,n="footNonRollEnd_{}_jnt_{}".format(side_l,number_l_r))[0]
            cmds.setAttr("{}.jointOrientX".format(foot_non_roll),0)
            cmds.parent(foot_non_roll_end,foot_non_roll)
            cmds.setAttr("{}.translateX".format(foot_non_roll_end),1)
            foot_non_roll_ik = cmds.ikHandle(sj=foot_non_roll, ee=foot_non_roll_end, s="sticky",n="footNonRollikHandle_{}_ik_{}".format(side_l,number_l_r),sol="ikRPsolver")[0]
            for axis in "XYZ":
                cmds.setAttr("{}.poleVector{}".format(foot_non_roll_ik,axis),0)
            
            foot_non_roll_grp = cmds.group(n="footNonRoll_{}_grp_{}".format(side_l,number_l_r),em=1,p=lowleg_roll_system)
            cmds.parent(foot_non_roll,foot_non_roll_grp)
            cmds.parent(foot_non_roll_ik,foot_non_roll_grp)
            
            cmds.pointConstraint(foot_jnt,foot_non_roll,n="footNonRollPoint_{}_cns_{}".format(side_l,number_l_r))
            foot_nonroll_ikhandle_pcon = cmds.group(n="footNonRollIkHandle_{}_pcon_{}".format(side_l,number_l_r),em=1,p=foot_jnt)
            cmds.matchTransform(foot_nonroll_ikhandle_pcon,foot_non_roll_end,pos=True,rot=False,scl=False)
            cmds.pointConstraint(foot_nonroll_ikhandle_pcon,foot_non_roll_ik,n="footNonRollIkHandlePconPoint_{}_cns_{}".format(side_l,number_l_r))
            
            foot_twist_value = cmds.duplicate(foot_jnt,po=True,n="footTwistValue_{}_jnt_{}".format(side_l,number_l_r))[0]
            cmds.parent(foot_twist_value,foot_jnt)
            cmds.setAttr("{}.jointOrientY".format(foot_twist_value),90)
            cmds.aimConstraint(foot_non_roll_end,
                                foot_twist_value,
                                offset=(0,0,0),
                                weight=1,
                                aimVector=(1,0,0),
                                upVector=(0,1,0),
                                worldUpType="objectrotation",
                                worldUpVector=(0,1,0),
                                worldUpObject=foot_non_roll,
                                n="foottoKneeNonAim_{}_cns_{}".format(side_l,number_l_r))
            cmds.parentConstraint(knee_jnt,foot_non_roll_grp,mo=True,n="kneeToFootNonRollGrpParent_{}_cns_{}".format(side_l,number_l_r)) 
        
            # 8.4.1 Creacion de la cadena twist del Upleg
            upleg_twist_list = JointChain(hip,knee,"uplegTwist",number_upleg_joints)
            new_upleg_twist_list = []
            for upleg_twist in upleg_twist_list:
                upleg_twist_jnt = cmds.rename(upleg_twist,"{}_{}_skn_{}".format(upleg_twist,side_l,number_l_r))
                new_upleg_twist_list.append(upleg_twist_jnt)
            first_upleg_twist = new_upleg_twist_list[0] 
            cmds.parent(first_upleg_twist,upleg_roll_system)
            last_upleg_twist = new_upleg_twist_list[-1]
            ikhandle_upleg_twist_list = cmds.ikHandle(sj=first_upleg_twist,
                                                         ee=last_upleg_twist,
                                                         sol="ikSplineSolver",
                                                         scv=False,
                                                         pcv=False,
                                                         n="uplegTwistikHandle_{}_ik_{}".format(side_l,number_l_r))
            upleg_twist_ik = ikhandle_upleg_twist_list[0]
            upleg_twist_crv = ikhandle_upleg_twist_list[2]
            upleg_twist_crv = cmds.rename(upleg_twist_crv,"uplegTwist_{}_crv_{}".format(side_l,number_l_r))
            cmds.parent(upleg_twist_ik,upleg_roll_system)
            if "l" in side_l:
                cmds.parent(upleg_twist_crv,leg_l_rig)
            if "r" in side_l:
                cmds.parent(upleg_twist_crv,leg_r_rig)
            upleg_twistvalue_mult = cmds.createNode("multiplyDivide",n="uplegTwistValue_{}_mult_{}".format(side_l,number_l_r))
            cmds.connectAttr("{}.rotateX".format(knee_twist_value),"{}.input1X".format(upleg_twistvalue_mult))
            cmds.setAttr("{}.input2X".format(upleg_twistvalue_mult),-1)
            cmds.connectAttr("{}.outputX".format(upleg_twistvalue_mult),"{}.twist".format(upleg_twist_ik))
            
            #8.4.2 Creacion de la cadena twist del Lowleg
            lowleg_twist_list = JointChain(knee,foot,"lowlegTwist",number_lowleg_joints)
            new_lowleg_twist_list = []
            for lowleg_twist in lowleg_twist_list:
                lowleg_twist_jnt = cmds.rename(lowleg_twist,"{}_{}_skn_{}".format(lowleg_twist,side_l,number_l_r))
                new_lowleg_twist_list.append(lowleg_twist_jnt)
            first_lowleg_twist = new_lowleg_twist_list[0]
            cmds.parent(first_lowleg_twist,knee_jnt)
            last_lowleg_twist = new_lowleg_twist_list[-1]
            ikhandle_lowleg_twist_list = cmds.ikHandle(sj=first_lowleg_twist,
                                                         ee=last_lowleg_twist,
                                                         sol="ikSplineSolver",
                                                         scv=False,
                                                         pcv=False,
                                                         n="lowlegTwistikHandle_{}_ik_{}".format(side_l,number_l_r))
            lowleg_twist_ik = ikhandle_lowleg_twist_list[0]
            lowleg_twist_crv = ikhandle_lowleg_twist_list[2]
            lowleg_twist_crv = cmds.rename(lowleg_twist_crv,"lowlegTwist_{}_crv_{}".format(side_l,number_l_r))
            cmds.parent(lowleg_twist_ik,lowleg_roll_system)
            if "l" in side_l:
                cmds.parent(lowleg_twist_crv,leg_l_rig)
            if "r" in side_l:
                cmds.parent(lowleg_twist_crv,leg_r_rig)
            lowleg_twistvalue_mult = cmds.createNode("multiplyDivide",n="lowlegTwistValue_{}_mult_{}".format(side_l,number_l_r))        
            cmds.connectAttr("{}.rotateX".format(foot_twist_value),"{}.input1X".format(lowleg_twistvalue_mult))
            cmds.setAttr("{}.input2X".format(lowleg_twistvalue_mult),-1)
            cmds.connectAttr("{}.outputX".format(lowleg_twistvalue_mult),"{}.twist".format(lowleg_twist_ik))
        
            # 8.5.1 Creacion del control FootIK
            foot_ik_ctr = cmds.duplicate("footIK_{}_ctr_0".format(side_l),n="footIK_{}_ctr_{}".format(side_l,number_l_r))[0]
            foot_ik_offset = CreateOffset(foot_ik_ctr,number_l_r)
            cmds.matchTransform(foot_ik_offset,foot_jnt,pos=True,rot=False,scl=False)
            cmds.parent(foot_ik_offset,foot_jnt)
            for axis in "XZ":
                cmds.setAttr("{}.rotate{}".format(foot_ik_offset,axis),0)
            cmds.setAttr("{}.rotateY".format(foot_ik_offset),90)
            cmds.parent(foot_ik_offset,control_center)
            AttrSeparator(foot_ik_ctr)    
            cmds.addAttr(foot_ik_ctr,ln= "knee",at= "double",dv=0,k=True)
            cmds.addAttr(foot_ik_ctr,ln= "autoStretch",at= "double",max=1,min=0,dv=1,k=True)
            cmds.addAttr(foot_ik_ctr,ln= "footRoll",at= "double",dv=0,k=True)
            cmds.addAttr(foot_ik_ctr,ln= "toeBreak",at= "double",dv=45,k=True)
            cmds.addAttr(foot_ik_ctr,ln= "releaseAngle",at= "double",dv=120,k=True)
            cmds.addAttr(foot_ik_ctr,ln= "footTilt",at= "double",dv=0,k=True)
            cmds.addAttr(foot_ik_ctr,ln= "toeRoll",at= "double",dv=0,k=True)
            cmds.addAttr(foot_ik_ctr,ln= "toeSlide",at= "double",dv=0,k=True)
            cmds.addAttr(foot_ik_ctr,ln= "heelRoll",at= "double",dv=0,k=True)
            cmds.addAttr(foot_ik_ctr,ln= "ballRoll",at= "double",dv=0,k=True)
        
            # 8.5.2 Creacion del control legPole
            leg_pole_ctr = cmds.duplicate("legPole_{}_ctr_0".format(side_l),n="legPole_{}_ctr_{}".format(side_l,number_l_r))[0]
            leg_pole_offset = CreateOffset(leg_pole_ctr,number_l_r)
            leg_pole_loc = PoleVector(sel=[hip_jnt,knee_jnt,leg_end_jnt],side=side_l)
            del_loc = cmds.duplicate(leg_pole_loc,n="del_loc")[0]
            cmds.parent(del_loc,leg_pole_loc)
            pole_distance = cmds.getAttr("{}.translateX".format(knee_jnt))
            cmds.setAttr("{}.translateX".format(del_loc),pole_distance)
            cmds.matchTransform(leg_pole_offset,del_loc,pos=True,rot=False,scl=False)
            cmds.delete(leg_pole_loc)
            cmds.parent(leg_pole_offset,control_center)
            AttrSeparator(leg_pole_ctr)
            cmds.addAttr(leg_pole_ctr,ln= "pinKnee",at= "double",max=1,min=0,dv=0,k=True)
        
            # 8.5.3 Creacion del control hip
            hip_ctr = cmds.duplicate("hip_{}_ctr_0".format(side_l),"hip_{}_ctr_{}".format(side_l,number_l_r))[0]
            hip_offset = CreateOffset(hip_ctr,number_l_r)
            cmds.matchTransform(hip_offset,hip_jnt,pos=True,rot=False,scl=False)
            spine_leg_conexion = win.checkBoxLegSpineConexion.isChecked()
            spine_leg_conexion_value = win.spinLegSpineConexion.value()
            if spine_leg_conexion is True:
                cmds.parent(hip_offset,"pelvis_c_ctr_{}".format(spine_leg_conexion_value))
            else:
                cmds.parent(hip_offset,control_center)
        
            # 8.5.4 Creacion del control legSettings
            leg_settings_ctr = cmds.duplicate("legSettings_{}_ctr_0".format(side_l),n="legSettings_{}_ctr_{}".format(side_l,number_l_r))[0]
            leg_settings_offset = CreateOffset(leg_settings_ctr,number_l_r)
            cmds.matchTransform(leg_settings_offset,foot_jnt,pos=True,rot=False,scl=False)
            leg_settings_pos = cmds.getAttr("{}.translateX".format(ball_jnt))
            cmds.setAttr("{}.translateZ".format(leg_settings_offset),0-leg_settings_pos)
            cmds.parent(leg_settings_offset,control_center)
            AttrSeparator(leg_settings_ctr)
            cmds.addAttr(leg_settings_ctr,ln= "legIK",at= "double",max=1,min=0,dv=1,k=True)
            cmds.addAttr(leg_settings_ctr,ln= "autoSquash",at= "double",max=1,min=0,dv=1,k=True)
            cmds.addAttr(leg_settings_ctr,ln= "visBends",at= "double",max=1,min=0,dv=1,k=True)
        
            # 8.5.5 Creacion del control hipFK
            hip_fk_ctr = cmds.duplicate("hipFK_{}_ctr_0".format(side_l),n="hipFK_{}_ctr_{}".format(side_l,number_l_r))[0]
            hip_fk_offset = CreateOffset(hip_fk_ctr,number_l_r)
            cmds.matchTransform(hip_fk_offset,hip_jnt,pos=True,rot=False,scl=False)
            cmds.parent(hip_fk_offset,hip_jnt)
            for axis in "XY":
                cmds.setAttr("{}.rotate{}".format(hip_fk_offset,axis),0)
            cmds.setAttr("{}.rotateZ".format(hip_fk_offset),90)
            if "r" in side_l:
                cmds.setAttr("{}.rotateX".format(hip_fk_offset),-180)
            cmds.parent(hip_fk_offset,control_center)
            AttrSeparator(hip_fk_ctr)
            cmds.addAttr(hip_fk_ctr,ln= "stretch",at= "double",dv=1,k=True)
           
            # 8.5.6 Creacion del control kneeFK
            knee_fk_ctr = cmds.duplicate("kneeFK_{}_ctr_0".format(side_l),n="kneeFK_{}_ctr_{}".format(side_l,number_l_r))[0]
            knee_fk_offset = CreateOffset(knee_fk_ctr,number_l_r)
            cmds.matchTransform(knee_fk_offset,knee_jnt,pos=True,rot=False,scl=False)
            cmds.parent(knee_fk_offset,knee_jnt)
            for axis in "XY":
                cmds.setAttr("{}.rotate{}".format(knee_fk_offset,axis),0)
            cmds.setAttr("{}.rotateZ".format(knee_fk_offset),90)
            if "r" in side_l:
                cmds.setAttr("{}.rotateX".format(knee_fk_offset),-180)
            cmds.parent(knee_fk_offset,hip_fk_ctr)
            AttrSeparator(knee_fk_ctr)
            cmds.addAttr(knee_fk_ctr,ln= "stretch",at= "double",dv=1,k=True)
            
            # 8.5.6 Creacion del control footFK
            foot_fk_ctr = cmds.duplicate("footFK_{}_ctr_0".format(side_l),n="footFK_{}_ctr_{}".format(side_l,number_l_r))[0]
            foot_fk_offset = CreateOffset(foot_fk_ctr,number_l_r)
            cmds.matchTransform(foot_fk_offset,foot_jnt,pos=True,rot=False,scl=False)
            cmds.parent(foot_fk_offset,foot_jnt)
            for axis in "XZ":
                cmds.setAttr("{}.rotate{}".format(foot_fk_offset,axis),0)
            cmds.setAttr("{}.rotateY".format(foot_fk_offset),90)
            if "r" in side_l:
                cmds.setAttr("{}.rotateX".format(foot_fk_offset),-180)
            cmds.parent(foot_fk_offset,knee_fk_ctr)   
        
            # 8.5.8 Creacion del control toe
            toe_ctr = cmds.duplicate("toe_{}_ctr_0".format(side_l),n="toe_{}_ctr_{}".format(side_l,number_l_r))[0]
            toe_offset = CreateOffset(toe_ctr,number_l_r)
            cmds.matchTransform(toe_offset,ball_jnt,pos=True,rot=False,scl=False)
            cmds.parent(toe_offset,ball_jnt)
            for axis in "XZ":
                cmds.setAttr("{}.rotate{}".format(toe_offset,axis),0)
            cmds.setAttr("{}.rotateY".format(toe_offset),90)
            cmds.parent(toe_offset,control_center)
        
            # 8.6.1 Configuracion del footroll system: Creacion y emparentamiento de locators
            ankle = cmds.duplicate(foot,n="ankle_{}_pcon_{}".format(side_l,number_l_r))[0]
            cmds.xform(ankle,ro=(0,0,0),ws=True)
            if "r" in side_l:
                cmds.setAttr("{}.rotateX".format(ankle),-180)
            ball_pivot = cmds.duplicate(ball,n="ballPivot_{}_loc_{}".format(side_l,number_l_r))[0]
            cmds.xform(ball_pivot,ro=(0,0,0),ws=True)
            if "r" in side_l:
                cmds.setAttr("{}.rotateX".format(ball_pivot),-180)
            ball_pivot_param = cmds.duplicate(ball_pivot,n="ballPivotParam_{}_loc_{}".format(side_l,number_l_r))[0]
            toe_pivot = cmds.duplicate(toe,n="toePivot_{}_loc_{}".format(side_l,number_l_r))[0]
            cmds.xform(toe_pivot,ro=(0,0,0),ws=True)
            if "r" in side_l:
                cmds.setAttr("{}.rotateX".format(toe_pivot),-180)
            toe_pivot_param = cmds.duplicate(toe_pivot,n="toePivotParam_{}_loc_{}".format(side_l,number_l_r))[0]
            heel_pivot = cmds.duplicate(heel,n="heelPivot_{}_loc_{}".format(side_l,number_l_r))[0]
            if "r" in side_l:
                cmds.setAttr("{}.rotateX".format(heel_pivot),-180)
            heel_param = cmds.duplicate(heel_pivot,n="heelPivotParam_{}_loc_{}".format(side_l,number_l_r))[0]
            bank_int_pivot = cmds.duplicate(bank_int,n="bankIntPivot_{}_loc_{}".format(side_l,number_l_r))[0]
            if "r" in side_l:
                cmds.setAttr("{}.rotateX".format(bank_int_pivot),-180)
            bank_ext_pivot = cmds.duplicate(bank_ext,n="bankExtPivot_{}_loc_{}".format(side_l,number_l_r))[0]
            if "r" in side_l:
                cmds.setAttr("{}.rotateX".format(bank_ext_pivot),-180)
            
            cmds.parent(ankle,ball_pivot)
            cmds.parent(ball_pivot,ball_pivot_param)
            cmds.parent(ball_pivot_param,toe_pivot)
            cmds.parent(toe_pivot,toe_pivot_param)
            cmds.parent(toe_pivot_param,heel_pivot)
            cmds.parent(heel_pivot,heel_param)
            cmds.parent(heel_param,bank_int_pivot)
            cmds.parent(bank_int_pivot,bank_ext_pivot)
            cmds.parent(bank_ext_pivot,foot_ik_ctr)
        
            # 8.6.2 Configuracion del ctrToe
            footfk_toepivot_cns = cmds.parentConstraint(foot_fk_ctr,toe_pivot,toe_offset,mo=True,n="footFKToePivotParent_{}_cns_{}".format(side_l,number_l_r))[0]
            leg_ik_rev = cmds.createNode("reverse",n="legIk_{}_rev_{}".format(side_l,number_l_r))
            cmds.connectAttr("{}.legIK".format(leg_settings_ctr),"{}.inputX".format(leg_ik_rev))
            cmds.connectAttr("{}.outputX".format(leg_ik_rev),"{}.{}W0".format(footfk_toepivot_cns,foot_fk_ctr))
            cmds.connectAttr("{}.legIK".format(leg_settings_ctr),"{}.{}W1".format(footfk_toepivot_cns,toe_pivot))                 
        
            # 8.6.3 Configuracion del FootTilt
            bank_ext_clamp = cmds.createNode("clamp",n="bankExt_{}_clamp_{}".format(side_l,number_l_r))
            cmds.setAttr("{}.maxR".format(bank_ext_clamp),999)
            cmds.connectAttr("{}.footTilt".format(foot_ik_ctr),"{}.inputR".format(bank_ext_clamp))
            
            bank_ext_mult = cmds.createNode("multiplyDivide",n="bankExt_{}_mult_{}".format(side_l,number_l_r))
            if "l" in side_l:
                cmds.setAttr("{}.input2X".format(bank_ext_mult),-1)
            if "r" in side_l:
                cmds.setAttr("{}.input2X".format(bank_ext_mult),1)
            cmds.connectAttr("{}.outputR".format(bank_ext_clamp),"{}.input1X".format(bank_ext_mult))
            cmds.connectAttr("{}.outputX".format(bank_ext_mult),"{}.rotateZ".format(bank_ext_pivot))
            
            bank_int_clamp = cmds.createNode("clamp",n="bankInt_{}_clamp_{}".format(side_l,number_l_r))
            cmds.setAttr("{}.minR".format(bank_int_clamp),-999)
            cmds.connectAttr("{}.footTilt".format(foot_ik_ctr),"{}.inputR".format(bank_int_clamp))
            
            bank_int_mult = cmds.createNode("multiplyDivide",n="bankInt_{}_mult_{}".format(side_l,number_l_r))
            cmds.setAttr("{}.input2X".format(bank_int_mult),-1)
            cmds.connectAttr("{}.outputR".format(bank_int_clamp),"{}.input1X".format(bank_int_mult))
            cmds.connectAttr("{}.outputX".format(bank_int_mult),"{}.rotateZ".format(bank_int_pivot))
        
            # 8.6.4 Configuracion del heelPivot
            heel_roll_clamp = cmds.createNode("clamp",n="heelRoll_{}_clamp_{}".format(side_l,number_l_r))
            cmds.setAttr("{}.minR".format(heel_roll_clamp),-999)
            cmds.connectAttr("{}.footRoll".format(foot_ik_ctr),"{}.inputR".format(heel_roll_clamp))
            cmds.connectAttr("{}.outputR".format(heel_roll_clamp),"{}.rotateX".format(heel_pivot))
            
            # 8.6.5 Configuracion del toePivot
            toe_roll_clamp = cmds.createNode("clamp",n="toeRoll_{}_clamp_{}".format(side_l,number_l_r))
            cmds.setAttr("{}.maxR".format(toe_roll_clamp),999)
            cmds.connectAttr("{}.toeBreak".format(foot_ik_ctr),"{}.minR".format(toe_roll_clamp))
            cmds.connectAttr("{}.footRoll".format(foot_ik_ctr),"{}.inputR".format(toe_roll_clamp))
            
            toe_roll_sub = cmds.createNode("plusMinusAverage",n="toeRoll_{}_sub_{}".format(side_l,number_l_r))
            cmds.setAttr("{}.operation".format(toe_roll_sub),2)
            cmds.connectAttr("{}.outputR".format(toe_roll_clamp),"{}.input2D[0].input2Dx".format(toe_roll_sub))
            cmds.connectAttr("{}.toeBreak".format(foot_ik_ctr),"{}.input2D[1].input2Dx".format(toe_roll_sub))
            
            cmds.connectAttr("{}.output2D.output2Dx".format(toe_roll_sub),"{}.rotateX".format(toe_pivot))
        
            #8.6.6 Configuracion del ballPivot
            angle_toe_break_sub = cmds.createNode("plusMinusAverage",n="angleToeBreak_{}_sub_{}".format(side_l,number_l_r))
            cmds.setAttr("{}.operation".format(angle_toe_break_sub),2)
            cmds.connectAttr("{}.releaseAngle".format(foot_ik_ctr),"{}.input2D[0].input2Dx".format(angle_toe_break_sub))
            cmds.connectAttr("{}.toeBreak".format(foot_ik_ctr),"{}.input2D[1].input2Dx".format(angle_toe_break_sub))
            
            toe_break_resta_div = cmds.createNode("multiplyDivide",n="toeBreakResta_{}_div_{}".format(side_l,number_l_r))
            cmds.setAttr("{}.operation".format(toe_break_resta_div),2)
            cmds.connectAttr("{}.toeBreak".format(foot_ik_ctr),"{}.input1X".format(toe_break_resta_div))
            cmds.connectAttr("{}.output2Dx".format(angle_toe_break_sub),"{}.input2X".format(toe_break_resta_div))
            
            toe_factor_mult = cmds.createNode("multiplyDivide",n="toeFactor_{}_mult_{}".format(side_l,number_l_r))
            cmds.connectAttr("{}.output2Dx".format(toe_roll_sub),"{}.input1X".format(toe_factor_mult))
            cmds.connectAttr("{}.outputX".format(toe_break_resta_div),"{}.input2X".format(toe_factor_mult))
            
            toe_roll_clamped = cmds.createNode("clamp",n="toeRollClamped_{}_clamp_{}".format(side_l,number_l_r))
            cmds.connectAttr("{}.toeBreak".format(foot_ik_ctr),"{}.maxR".format(toe_roll_clamped))
            cmds.connectAttr("{}.outputX".format(toe_factor_mult),"{}.inputR".format(toe_roll_clamped))
            
            ball_roll_clamp = cmds.createNode("clamp",n="ballRoll_{}_clamp_{}".format(side_l,number_l_r))
            cmds.connectAttr("{}.toeBreak".format(foot_ik_ctr),"{}.maxR".format(ball_roll_clamp))
            cmds.connectAttr("{}.footRoll".format(foot_ik_ctr),"{}.inputR".format(ball_roll_clamp))
            
            ball_roll_release_sub = cmds.createNode("plusMinusAverage",n="ballRollRelease_{}_sub_{}".format(side_l,number_l_r))
            cmds.setAttr("{}.operation".format(ball_roll_release_sub),2)
            cmds.connectAttr("{}.outputR".format(ball_roll_clamp),"{}.input2D[0].input2Dx".format(ball_roll_release_sub))
            cmds.connectAttr("{}.outputR".format(toe_roll_clamped),"{}.input2D[1].input2Dx".format(ball_roll_release_sub))
            
            cmds.connectAttr("{}.output2Dx".format(ball_roll_release_sub),"{}.rotateX".format(ball_pivot))
        
            # 8.6.7 Configuracion del heelRoll, ballRoll, toeRoll, toeSlide
            cmds.connectAttr("{}.heelRoll".format(foot_ik_ctr),"{}.rotateX".format(heel_param))
            cmds.connectAttr("{}.ballRoll".format(foot_ik_ctr),"{}.rotateX".format(ball_pivot_param))
            cmds.connectAttr("{}.toeRoll".format(foot_ik_ctr),"{}.rotateX".format(toe_pivot_param))
            cmds.connectAttr("{}.toeSlide".format(foot_ik_ctr),"{}.rotateY".format(toe_pivot_param))
            
            Hide(bank_ext_pivot)
        
            # 8.7.1 Creacion de los joints PAC
            hip_pac = cmds.duplicate(hip_jnt,po=True,n="hipPac_{}_jnt_{}".format(side_l,number_l_r))[0]
            hip_pac_offset = CreateOffset(hip_pac,number_l_r)
            cmds.parent(hip_pac_offset,hip_fk_ctr)
            
            knee_pac = cmds.duplicate(knee_jnt,po=True,n="kneePac_{}_jnt_{}".format(side_l,number_l_r))[0]
            knee_pac_offest = CreateOffset(knee_pac,number_l_r)
            cmds.parent(knee_pac_offest,knee_fk_ctr)
            
            foot_fk_pac = cmds.duplicate(foot_jnt,po=True,n="footFkPac_{}_jnt_{}".format(side_l,number_l_r))[0]
            foot_fk_pac_offest = CreateOffset(foot_fk_pac,number_l_r)
            cmds.parent(foot_fk_pac_offest,foot_fk_ctr)
            
            foot_ik_pac = cmds.duplicate(foot_jnt,po=True,n="footIkPac_{}_jnt_{}".format(side_l,number_l_r))[0]
            foot_ik_pac_offest = CreateOffset(foot_ik_pac,number_l_r)
            cmds.parent(foot_ik_pac_offest,ankle)
            
            ball_pac = cmds.duplicate(ball_jnt,po=True,n="ballPac_{}_jnt_{}".format(side_l,number_l_r))[0]
            ball_pac_offest = CreateOffset(ball_pac,number_l_r)
            cmds.parent(ball_pac_offest,toe_ctr)
        
            # 8.7.2 Relaciones basicas entre controles, huesos e ikHandles
            cmds.pointConstraint(foot_ik_pac,leg_main_ik,mo=False,n="footIkPacHandlePoint_{}_cns_{}".format(side_l,number_l_r))
            cmds.poleVectorConstraint(leg_pole_ctr,leg_main_ik,n="poleVectorIkHandlePole_{}_cns_{}".format(side_l,number_l_r))
            cmds.orientConstraint(hip_pac,hip_jnt,mo=True,n="hipPacOrient_{}_cns_{}".format(side_l,number_l_r))
            cmds.cycleCheck(e=False)
            cmds.orientConstraint(knee_pac,knee_jnt,mo=True,n="kneePacOrient_{}_cns_{}".format(side_l,number_l_r))
            ball_pac_cns = cmds.orientConstraint(ball_pac,ball_jnt,mo=True,n="ballPacOrient_{}_cns_{}".format(side_l,number_l_r))[0]
            cmds.setAttr("{}.interpType".format(ball_pac_cns),2)
            cmds.pointConstraint(hip_ctr,hip_jnt,mo=True,n="hipPoint_{}_cns_{}".format(side_l,number_l_r))
            cmds.parentConstraint(foot_jnt,leg_settings_ctr,mo=True,n="footLegSettingsPoint_{}_cns_{}".format(side_l,number_l_r))
            foot_fk_ik_orient_cns = cmds.orientConstraint(foot_fk_pac,foot_ik_pac,foot_jnt,mo=True,n="footFkIkOrient_{}_cns_{}".format(side_l,number_l_r))[0]
        
            # 8.7.3 Conexiones para realizar el switch FK/IK
            cmds.connectAttr("{}.legIK".format(leg_settings_ctr),"{}.ikBlend".format(leg_main_ik))
            cmds.connectAttr("{}.legIK".format(leg_settings_ctr),"{}.{}W1".format(foot_fk_ik_orient_cns,foot_ik_pac))
            cmds.connectAttr("{}.outputX".format(leg_ik_rev),"{}.{}W0".format(foot_fk_ik_orient_cns,foot_fk_pac))
            cmds.cycleCheck(e=True)
            cmds.connectAttr("{}.legIK".format(leg_settings_ctr),"{}.visibility".format(foot_ik_offset))
            cmds.connectAttr("{}.legIK".format(leg_settings_ctr),"{}.visibility".format(leg_pole_offset))
            cmds.connectAttr("{}.outputX".format(leg_ik_rev),"{}.visibility".format(hip_fk_offset))
            
            # 8.7.4 Otras conexiones
            cmds.connectAttr("{}.knee".format(foot_ik_ctr),"{}.twist".format(leg_main_ik))
        
            # 8.8.1 Configuracion del squash/Stretch: Creacion de lo locators para medir las distancias.
            hip_stretch = cmds.duplicate(hip,n="hipStretch_{}_loc_{}".format(side_l,number_l_r))[0]
            cmds.xform(hip_stretch,ro=(0,0,0),ws=True)
            cmds.parent(hip_stretch,hip_ctr)
            
            knee_stretch = cmds.duplicate(knee,n="kneeStretch_{}_loc_{}".format(side_l,number_l_r))[0]
            cmds.xform(knee_stretch,ro=(0,0,0),ws=True)
            cmds.parent(knee_stretch,leg_pole_ctr)
            
            foot_stretch = cmds.spaceLocator(n="footStretch_{}_loc_{}".format(side_l,number_l_r))[0]
            cmds.matchTransform(foot_stretch,foot_ik_ctr,pos=True,rot=False,scl=False)
            cmds.parent(foot_stretch,ball_pivot)
        
            # 8.8.2 Conectar los locators con los nodos distance
            upleg_distance = cmds.createNode("distanceBetween",n="upleg_{}_dist_{}".format(side_l,number_l_r))
            cmds.connectAttr("{}.worldPosition[0]".format(hip_stretch),"{}.point1".format(upleg_distance))
            cmds.connectAttr("{}.worldPosition[0]".format(knee_stretch),"{}.point2".format(upleg_distance))
            
            lowleg_distance = cmds.createNode("distanceBetween",n="lowleg_{}_dist_{}".format(side_l,number_l_r))
            cmds.connectAttr("{}.worldPosition[0]".format(knee_stretch),"{}.point1".format(lowleg_distance))
            cmds.connectAttr("{}.worldPosition[0]".format(foot_stretch),"{}.point2".format(lowleg_distance))
            
            entire_leg_distance = cmds.createNode("distanceBetween",n="entireLeg_{}_dist_{}".format(side_l,number_l_r))
            cmds.connectAttr("{}.worldPosition[0]".format(hip_stretch),"{}.point1".format(entire_leg_distance))
            cmds.connectAttr("{}.worldPosition[0]".format(foot_stretch),"{}.point2".format(entire_leg_distance))
        
            # 8.8.3 Configurar el stretch IK y normalizarlo
            leg_normal_stretch_div = cmds.createNode("multiplyDivide",n="legNormalStretch_{}_div_{}".format(side_l,number_l_r))
            cmds.setAttr("{}.operation".format(leg_normal_stretch_div),2)
            cmds.connectAttr("{}.distance".format(entire_leg_distance),"{}.input1X".format(leg_normal_stretch_div))
            entire_leg_dist_value = cmds.getAttr("{}.distance".format(entire_leg_distance))
            cmds.setAttr("{}.input2X".format(leg_normal_stretch_div),entire_leg_dist_value)
            
            leg_stretch_clamp = cmds.createNode("clamp",n="legStretch_{}_clamp_{}".format(side_l,number_l_r))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.minR".format(leg_stretch_clamp))
            cmds.setAttr("{}.maxR".format(leg_stretch_clamp),999)
            cmds.connectAttr("{}.outputX".format(leg_normal_stretch_div),"{}.inputR".format(leg_stretch_clamp))
            
            upleg_stretch_div = cmds.createNode("multiplyDivide",n="uplegStretch_{}_div_{}".format(side_l,number_l_r))
            cmds.setAttr("{}.operation".format(upleg_stretch_div),2)
            cmds.connectAttr("{}.distance".format(upleg_distance),"{}.input1X".format(upleg_stretch_div))
            upleg_dist_value = cmds.getAttr("{}.distance".format(upleg_distance))
            cmds.setAttr("{}.input2X".format(upleg_stretch_div),upleg_dist_value)
            
            lowleg_stretch_div = cmds.createNode("multiplyDivide",n="lowlegStretch_{}_div_{}".format(side_l,number_l_r))
            cmds.setAttr("{}.operation".format(lowleg_stretch_div),2)
            cmds.connectAttr("{}.distance".format(lowleg_distance),"{}.input1X".format(lowleg_stretch_div))
            lowleg_dist_value = cmds.getAttr("{}.distance".format(lowleg_distance))
            cmds.setAttr("{}.input2X".format(lowleg_stretch_div),lowleg_dist_value)
            
            leg_ikstretch_blend = cmds.createNode("blendColors",n="legIkStretch_{}_blend_{}".format(side_l,number_l_r))
            cmds.connectAttr("{}.outputX".format(upleg_stretch_div),"{}.color1G".format(leg_ikstretch_blend))
            cmds.connectAttr("{}.outputX".format(lowleg_stretch_div),"{}.color1B".format(leg_ikstretch_blend))
            cmds.connectAttr("{}.outputR".format(leg_stretch_clamp),"{}.color2G".format(leg_ikstretch_blend))
            cmds.connectAttr("{}.outputR".format(leg_stretch_clamp),"{}.color2B".format(leg_ikstretch_blend))
            
            leg_final_stretch_blend = cmds.createNode("blendColors",n="legFinalStretch_{}_blend_{}".format(side_l,number_l_r))
            cmds.connectAttr("{}.legIK".format(leg_settings_ctr),"{}.blender".format(leg_final_stretch_blend))
            cmds.connectAttr("{}.outputG".format(leg_ikstretch_blend),"{}.color1G".format(leg_final_stretch_blend))
            cmds.connectAttr("{}.outputB".format(leg_ikstretch_blend),"{}.color1B".format(leg_final_stretch_blend))
            cmds.setAttr("{}.color2G".format(leg_final_stretch_blend),1)
            cmds.setAttr("{}.color2B".format(leg_final_stretch_blend),1)
        
            # 8.8.4 Cofigurar el autoStretch
            leg_stretchiness_blend = cmds.createNode("blendColors",n="legStretchiness_{}_blend_{}".format(side_l,number_l_r))
            cmds.connectAttr("{}.outputG".format(leg_final_stretch_blend),"{}.color1G".format(leg_stretchiness_blend))
            cmds.connectAttr("{}.outputB".format(leg_final_stretch_blend),"{}.color1B".format(leg_stretchiness_blend))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.color2G".format(leg_stretchiness_blend))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.color2B".format(leg_stretchiness_blend))
            
            leg_stretch_by_global_div = cmds.createNode("multiplyDivide",n="legStretchByGlobal_{}_div_{}".format(side_l,number_l_r))
            cmds.setAttr("{}.operation".format(leg_stretch_by_global_div),2)
            cmds.connectAttr("{}.outputG".format(leg_stretchiness_blend),"{}.input1X".format(leg_stretch_by_global_div))
            cmds.connectAttr("{}.outputB".format(leg_stretchiness_blend),"{}.input1Y".format(leg_stretch_by_global_div))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.input2X".format(leg_stretch_by_global_div))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.input2Y".format(leg_stretch_by_global_div))
            
            footik_autostretch_override_sum = cmds.createNode("plusMinusAverage",n="footIkAutoStretchOverride_{}_sum_{}".format(side_l,number_l_r))
            cmds.connectAttr("{}.outputX".format(leg_ik_rev),"{}.input2D[0].input2Dx".format(footik_autostretch_override_sum))
            cmds.connectAttr("{}.autoStretch".format(foot_ik_ctr),"{}.input2D[1].input2Dx".format(footik_autostretch_override_sum))
            
            footik_finalstretchiness_clamp = cmds.createNode("clamp",n="footIkFinalStretchiness_{}_clamp_{}".format(side_l,number_l_r))
            cmds.setAttr("{}.maxR".format(footik_finalstretchiness_clamp),1)
            cmds.connectAttr("{}.output2Dx".format(footik_autostretch_override_sum),"{}.inputR".format(footik_finalstretchiness_clamp))
            cmds.connectAttr("{}.outputR".format(footik_finalstretchiness_clamp),"{}.blender".format(leg_stretchiness_blend))
            
            # 8.8.5 Conectar con las escalas de los huesos
            cmds.connectAttr("{}.outputX".format(leg_stretch_by_global_div),"{}.scaleX".format(hip_jnt))
            cmds.connectAttr("{}.outputY".format(leg_stretch_by_global_div),"{}.scaleX".format(knee_jnt))
            
            # 8.8.6 Configurar el stretch Fk
            hipfk_stretchbyglobal_mult = cmds.createNode("multiplyDivide",n="hipFkStretchByGlobal_{}_mult_{}".format(side_l,number_l_r))
            cmds.connectAttr("{}.stretch".format(hip_fk_ctr),"{}.input1X".format(hipfk_stretchbyglobal_mult))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.input2X".format(hipfk_stretchbyglobal_mult))
            cmds.connectAttr("{}.outputX".format(hipfk_stretchbyglobal_mult),"{}.color2G".format(leg_final_stretch_blend))
            cmds.cycleCheck(e=False)
            cmds.pointConstraint(knee_jnt,knee_fk_offset,n="kneeToFkOffsetPoint_{}_cns_{}".format(side_l,number_l_r))
            
            kneefk_stretchbyglobal_mult = cmds.createNode("multiplyDivide",n="kneeFkStretchByGlobal_{}_mult_{}".format(side_l,number_l_r))
            cmds.connectAttr("{}.stretch".format(knee_fk_ctr),"{}.input1X".format(kneefk_stretchbyglobal_mult))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.input2X".format(kneefk_stretchbyglobal_mult))
            cmds.connectAttr("{}.outputX".format(kneefk_stretchbyglobal_mult),"{}.color2B".format(leg_final_stretch_blend))
            
            cmds.pointConstraint(leg_end_jnt,foot_fk_offset,n="legEndToFkOffsetPoint_{}_cns_{}".format(side_l,number_l_r))
        
        
            # 8.8.7 Conectar los joints del twistUplegChain con el stretch
            upleg_twist_stretch_ci = cmds.createNode("curveInfo",n="uplegTwistStretch_{}_ci_{}".format(side_l,number_l_r))
            cmds.connectAttr("{}.worldSpace[0]".format(upleg_twist_crv),"{}.inputCurve".format(upleg_twist_stretch_ci))
            
            upleg_ikcurvelength_div = cmds.createNode("multiplyDivide",n="uplegIkCurveLength_{}_div_{}".format(side_l,number_l_r))
            cmds.setAttr("{}.operation".format(upleg_ikcurvelength_div),2)
            cmds.connectAttr("{}.arcLength".format(upleg_twist_stretch_ci),"{}.input1X".format(upleg_ikcurvelength_div))
            upleg_curvelength = cmds.getAttr("{}.arcLength".format(upleg_twist_stretch_ci))
            cmds.setAttr("{}.input2X".format(upleg_ikcurvelength_div),upleg_curvelength)
            
            upleg_lengthbyglobal_div = cmds.createNode("multiplyDivide",n="uplegLengthByGlobal_{}_div_{}".format(side_l,number_l_r))
            cmds.setAttr("{}.operation".format(upleg_lengthbyglobal_div),2) 
            cmds.connectAttr("{}.outputX".format(upleg_ikcurvelength_div),"{}.input1X".format(upleg_lengthbyglobal_div))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.input2X".format(upleg_lengthbyglobal_div))
            
            n_jnt_upleg_twist = len(new_upleg_twist_list)
            upleg_twist_stretch_list = new_upleg_twist_list[0:n_jnt_upleg_twist-1]
            for upleg_twist_stretch_jnt in upleg_twist_stretch_list:
                cmds.connectAttr("{}.outputX".format(upleg_lengthbyglobal_div),"{}.scaleX".format(upleg_twist_stretch_jnt))
        
            # 8.8.8 Conectar los joints del twistLowLegChain con el stretch.
            lowleg_twist_stretch_ci = cmds.createNode("curveInfo",n="lowlegTwistStretch_{}_ci_{}".format(side_l,number_l_r))
            cmds.connectAttr("{}.worldSpace[0]".format(lowleg_twist_crv),"{}.inputCurve".format(lowleg_twist_stretch_ci))
            
            lowleg_ikcurvelength_div = cmds.createNode("multiplyDivide",n="lowlegIkCurveLength_{}_div_{}".format(side_l,number_l_r))
            cmds.setAttr("{}.operation".format(lowleg_ikcurvelength_div),2)
            cmds.connectAttr("{}.arcLength".format(lowleg_twist_stretch_ci),"{}.input1X".format(lowleg_ikcurvelength_div))
            lowleg_curvelength = cmds.getAttr("{}.arcLength".format(lowleg_twist_stretch_ci))
            cmds.setAttr("{}.input2X".format(lowleg_ikcurvelength_div),lowleg_curvelength)
            
            lowleg_lengthbyglobal_div = cmds.createNode("multiplyDivide",n="lowlegLengthByGlobal_{}_div_{}".format(side_l,number_l_r))
            cmds.setAttr("{}.operation".format(lowleg_lengthbyglobal_div),2) 
            cmds.connectAttr("{}.outputX".format(lowleg_ikcurvelength_div),"{}.input1X".format(lowleg_lengthbyglobal_div))
            cmds.connectAttr("{}.globalScale".format(control_base),"{}.input2X".format(lowleg_lengthbyglobal_div))
            
            n_jnt_lowleg_twist = len(new_lowleg_twist_list)
            lowleg_twist_stretch_list = new_lowleg_twist_list[0:n_jnt_lowleg_twist-1]
            for lowleg_twist_stretch_jnt in lowleg_twist_stretch_list:
                cmds.connectAttr("{}.outputX".format(lowleg_lengthbyglobal_div),"{}.scaleX".format(lowleg_twist_stretch_jnt))
            cmds.cycleCheck(e=True)
        
            # 8.8.9 Conectar el pinKnee
            pinknee_byik_mult = cmds.createNode("multiplyDivide",n="pinKneeByIk_{}_mult_{}".format(side_l,number_l_r))
            cmds.connectAttr("{}.pinKnee".format(leg_pole_ctr),"{}.input1X".format(pinknee_byik_mult))
            cmds.connectAttr("{}.legIK".format(leg_settings_ctr),"{}.input2X".format(pinknee_byik_mult))
            cmds.connectAttr("{}.outputX".format(pinknee_byik_mult),"{}.blender".format(leg_ikstretch_blend))
            cmds.connectAttr("{}.outputX".format(pinknee_byik_mult),"{}.input2D[2].input2Dx".format(footik_autostretch_override_sum))
            
            # 8.8.10 Reposicionar el kneeStretchLoc en el ctrLegPole
            cmds.matchTransform(knee_stretch,leg_pole_ctr,pos=True,rot=False,scl=False)
            
            Hide(knee_stretch)
            # 8.8.11 Configuracion del autoSquash
            legstretch_byglobal_inv_div = cmds.createNode("multiplyDivide",n="legStretchByGlobalInv_{}_div_{}".format(side_l,number_l_r))
            cmds.setAttr("{}.operation".format(legstretch_byglobal_inv_div),2)
            cmds.connectAttr("{}.outputX".format(leg_stretch_by_global_div),"{}.input2X".format(legstretch_byglobal_inv_div))
            cmds.connectAttr("{}.outputY".format(leg_stretch_by_global_div),"{}.input2Y".format(legstretch_byglobal_inv_div))
            cmds.setAttr("{}.input1X".format(legstretch_byglobal_inv_div),1)
            cmds.setAttr("{}.input1Y".format(legstretch_byglobal_inv_div),1)
            
            leg_autosquash_blend = cmds.createNode("blendColors",n="legAutoSquash_{}_blend_{}".format(side_l,number_l_r))
            cmds.connectAttr("{}.autoSquash".format(leg_settings_ctr),"{}.blender".format(leg_autosquash_blend))
            cmds.connectAttr("{}.outputX".format(legstretch_byglobal_inv_div),"{}.color1G".format(leg_autosquash_blend))
            cmds.connectAttr("{}.outputY".format(legstretch_byglobal_inv_div),"{}.color1B".format(leg_autosquash_blend))
            cmds.setAttr("{}.color2G".format(leg_autosquash_blend),1)
            cmds.setAttr("{}.color2B".format(leg_autosquash_blend),1)
            
            for upleg_twist_jnt in new_upleg_twist_list:
                cmds.connectAttr("{}.outputG".format(leg_autosquash_blend),"{}.scaleY".format(upleg_twist_jnt))
                cmds.connectAttr("{}.outputG".format(leg_autosquash_blend),"{}.scaleZ".format(upleg_twist_jnt))
            
            for lowleg_twist_jnt in new_lowleg_twist_list:
                cmds.connectAttr("{}.outputB".format(leg_autosquash_blend),"{}.scaleY".format(lowleg_twist_jnt))
                cmds.connectAttr("{}.outputB".format(leg_autosquash_blend),"{}.scaleZ".format(lowleg_twist_jnt))
        
            # 8.9.1 Creacion del sistema bend: Reconstruccion de las curvas
            upleg_twist_crv = cmds.rebuildCurve(upleg_twist_crv,ch=1,rpo=1,rt=0,end=1,kr=0,kcp=0,kep=1,kt=0,s=1,d=3,tol=0.01)[0] 
            lowleg_twist_crv = cmds.rebuildCurve(lowleg_twist_crv,ch=1,rpo=1,rt=0,end=1,kr=0,kcp=0,kep=1,kt=0,s=1,d=3,tol=0.01)[0]
            
            # 8.9.2 Creacion de los clusters
            legbend_cluster_a =cmds.cluster("{}.cv[0]".format(upleg_twist_crv),n="legBendA_{}_cl_{}".format(side_l,number_l_r))[1]
            legbend_cluster_b =cmds.cluster("{}.cv[1:2]".format(upleg_twist_crv),n="legBendB_{}_cl_{}".format(side_l,number_l_r))[1]
            legbend_cluster_c =cmds.cluster("{}.cv[3]".format(upleg_twist_crv),"{}.cv[0]".format(lowleg_twist_crv),n="lowBendC_{}_cl_{}".format(side_l,number_l_r))[1]
            legbend_cluster_d =cmds.cluster("{}.cv[1:2]".format(lowleg_twist_crv),n="legBendD_{}_cl_{}".format(side_l,number_l_r))[1]
            legbend_cluster_e =cmds.cluster("{}.cv[3]".format(lowleg_twist_crv),n="legBendE_{}_cl_{}".format(side_l,number_l_r))[1]
        
            # 8.9.3 Creacion de controles Bend
            cmds.parent(legbend_cluster_a,hip_jnt)
            cmds.parent(legbend_cluster_e,foot_jnt)
            
            upleg_bend_ctr = cmds.duplicate("uplegBend_{}_ctr_0".format(side_l),n="uplegBend_{}_ctr_{}".format(side_l,number_l_r))[0]
            upleg_bend_offset = CreateOffset(upleg_bend_ctr,number_l_r)
            cmds.matchTransform(upleg_bend_offset,legbend_cluster_b,pos=True,rot=False,scl=False)
            cmds.parent(legbend_cluster_b,upleg_bend_ctr)
            cmds.parent(upleg_bend_offset,hip_jnt)
            
            knee_bend_ctr = cmds.duplicate("kneeBend_{}_ctr_0".format(side_l),n="kneeBend_{}_ctr_{}".format(side_l,number_l_r))[0]
            knee_bend_offset = CreateOffset(knee_bend_ctr,number_l_r)
            cmds.matchTransform(knee_bend_offset,legbend_cluster_c,pos=True,rot=False,scl=False)
            cmds.parent(legbend_cluster_c,knee_bend_ctr)
            cmds.parent(knee_bend_offset,char_skeleton)
            
            lowleg_bend_ctr = cmds.duplicate("lowlegBend_{}_ctr_0".format(side_l),n="lowlegBend_{}_ctr_{}".format(side_l,number_l_r))[0]
            lowleg_bend_offset = CreateOffset(lowleg_bend_ctr,number_l_r)
            cmds.matchTransform(lowleg_bend_offset,legbend_cluster_d,pos=True,rot=False,scl=False)
            cmds.parent(legbend_cluster_d,lowleg_bend_ctr)
            cmds.parent(lowleg_bend_offset,knee_jnt)
            
            # 8.9.4 Creacion de las relaciones entre los controles y los huesos
            cmds.parentConstraint(knee_jnt,knee_bend_offset,mo=True,n="KneeBendParent_{}_cns_{}".format(side_l,number_l_r))
            
            if spine_leg_conexion is True:
                # 8.10.1 Conexion entre modulos(pelvis): Emparentamientos
                cmds.parent(hip_jnt_offset,"pelvis_c_skn_{}".format(spine_leg_conexion_value))
                       
            # 8.10.2 Configuracion del hipFKPCon
            hip_fk_pcon = cmds.duplicate(hip_fk_offset,po=True,n="hipFk_{}_pcon_{}".format(side_l,number_l_r))
            cmds.parent(hip_fk_pcon,hip_ctr)
            cmds.pointConstraint(hip_fk_pcon,hip_fk_offset,n="hipFkPconPoint_{}_cns_{}".format(side_l,number_l_r))
            
            # 8.10.3 Parent Constraint
            cmds.parentConstraint(hip_ctr,upleg_roll_system,mo=True,n="hipUplegRollSystem_{}_cns_{}".format(side_l,number_l_r))
            
            leg_spaces_bool = win.checkBoxLegSpaces.isChecked()
            leg_space_spine_value = win.spinLegConexion.value()
            
            if leg_spaces_bool is True:
                # 8.11.1 Configuracion de los spaces en ctrHipFk
                cmds.addAttr(hip_fk_ctr,ln= "__", at="enum",en="spaces")
                cmds.setAttr ("{}.__".format(hip_fk_ctr),channelBox= True)    
                cmds.addAttr(hip_fk_ctr,ln= "pelvisSpace",at= "double",min= 0,max=1,dv=0,k=True)
                
                hip_fk_worldspace = cmds.duplicate(hip_fk_offset,po=True,n="hipFkWorldSpace_{}_grp_{}".format(side_l,number_l_r))[0]
                hip_fk_pelvisspace = cmds.duplicate(hip_fk_offset,po=True,n="hipFkPelvisSpace_{}_grp_{}".format(side_l,number_l_r))[0]
                
                hip_fk_spaces_cns = cmds.orientConstraint(hip_fk_worldspace,hip_fk_pelvisspace,hip_fk_offset,mo=False,n="hipFkSpacesOrient_{}_cns_{}".format(side_l,number_l_r))[0]
                cmds.parent(hip_fk_pelvisspace,"pelvis_c_ctr_{}".format(leg_space_spine_value))
                
                cmds.connectAttr("{}.pelvisSpace".format(hip_fk_ctr),"{}.{}W1".format(hip_fk_spaces_cns,hip_fk_pelvisspace))
                hip_fk_dynparent_rev = cmds.createNode("reverse",n="hipFkDynParent_{}_rev_{}".format(side_l,number_l_r))
                cmds.connectAttr("{}.pelvisSpace".format(hip_fk_ctr),"{}.inputX".format(hip_fk_dynparent_rev))
                cmds.connectAttr("{}.outputX".format(hip_fk_dynparent_rev),"{}.{}W0".format(hip_fk_spaces_cns,hip_fk_worldspace))
        
                # 8.11.2 Configuracion de los spaces en ctrFootIK
                cmds.addAttr(foot_ik_ctr,ln= "__", at="enum",en="spaces")
                cmds.setAttr ("{}.__".format(foot_ik_ctr),channelBox= True)    
                cmds.addAttr(foot_ik_ctr,ln= "pelvisSpace",at= "double",min= 0,max=1,dv=0,k=True)
                
                foot_ik_worldspace = cmds.duplicate(foot_ik_offset,po=True,n="footIkWorldSpace_{}_grp_{}".format(side_l,number_l_r))[0]
                foot_ik_pelvisspace = cmds.duplicate(foot_ik_offset,po=True,n="footIkPelvisSpace_{}_grp_{}".format(side_l,number_l_r))[0]
                
                foot_ik_spaces_cns = cmds.parentConstraint(foot_ik_worldspace,foot_ik_pelvisspace,foot_ik_offset,mo=False,n="footIkSpacesParent_{}_cns_{}".format(side_l,number_l_r))[0]
                cmds.parent(foot_ik_pelvisspace,"pelvis_c_ctr_{}".format(leg_space_spine_value))
                
                cmds.connectAttr("{}.pelvisSpace".format(foot_ik_ctr),"{}.{}W1".format(foot_ik_spaces_cns,foot_ik_pelvisspace))
                foot_ik_dynparent_rev = cmds.createNode("reverse",n="footIkDynParent_{}_rev_{}".format(side_l,number_l_r))
                cmds.connectAttr("{}.pelvisSpace".format(foot_ik_ctr),"{}.inputX".format(foot_ik_dynparent_rev))
                cmds.connectAttr("{}.outputX".format(foot_ik_dynparent_rev),"{}.{}W0".format(foot_ik_spaces_cns,foot_ik_worldspace))
                # 8.11.3 Configuracion de los atributos de los spaces en el ctrLegPole
                cmds.addAttr(leg_pole_ctr,ln= "__", at="enum",en="spaces")
                cmds.setAttr ("{}.__".format(leg_pole_ctr),channelBox= True)    
                cmds.addAttr(leg_pole_ctr,ln= "footSpace",at= "double",min= 0,max=1,dv=0,k=True)
                cmds.addAttr(leg_pole_ctr,ln= "pelvisSpace",at= "double",min= 0,max=1,dv=0,k=True)
                
                leg_pole_worldspace = cmds.duplicate(leg_pole_offset,po=True,n="legPoleWorldSpace_{}_grp_{}".format(side_l,number_l_r))[0]
                leg_pole_footspace = cmds.duplicate(leg_pole_offset,po=True,n="legPoleFootSpace_{}_grp_{}".format(side_l,number_l_r))[0]
                leg_pole_pelvisspace = cmds.duplicate(leg_pole_offset,po=True,n="legPolePelvisSpace_{}_grp_{}".format(side_l,number_l_r))[0]
                
                leg_pole_spaces_cns = cmds.parentConstraint(leg_pole_worldspace,leg_pole_footspace,leg_pole_pelvisspace,leg_pole_offset,mo=False,n="legPoleSpacesParent_{}_cns_{}".format(side_l,number_l_r))[0]
                
                cmds.parent(leg_pole_footspace,foot_ik_ctr)
                cmds.parent(leg_pole_pelvisspace,"pelvis_c_ctr_{}".format(leg_space_spine_value))
                
                cmds.connectAttr("{}.footSpace".format(leg_pole_ctr),"{}.{}W1".format(leg_pole_spaces_cns,leg_pole_footspace))
                cmds.connectAttr("{}.pelvisSpace".format(leg_pole_ctr),"{}.{}W2".format(leg_pole_spaces_cns,leg_pole_pelvisspace))
                
                leg_pole_dynparent_sum = cmds.createNode("plusMinusAverage",n="legPoleDynParent_{}_sum_{}".format(side_l,number_l_r))
                cmds.connectAttr("{}.footSpace".format(leg_pole_ctr),"{}.input2D[0].input2Dx".format(leg_pole_dynparent_sum))
                cmds.connectAttr("{}.pelvisSpace".format(leg_pole_ctr),"{}.input2D[1].input2Dx".format(leg_pole_dynparent_sum))
                
                leg_pole_dynparent_clamp = cmds.createNode("clamp",n="legPoleDynParent_{}_clamp_{}".format(side_l,number_l_r))
                cmds.setAttr("{}.maxR".format(leg_pole_dynparent_clamp),1)
                cmds.connectAttr("{}.output2Dx".format(leg_pole_dynparent_sum),"{}.inputR".format(leg_pole_dynparent_clamp))
                
                leg_pole_dynparent_rev = cmds.createNode("reverse",n="legPoleDynParent_{}_rev_{}".format(side_l,number_l_r))
                cmds.connectAttr("{}.outputR".format(leg_pole_dynparent_clamp),"{}.inputX".format(leg_pole_dynparent_rev))
                cmds.connectAttr("{}.outputX".format(leg_pole_dynparent_rev),"{}.{}W0".format(leg_pole_spaces_cns,leg_pole_worldspace))
            # Cerrar rig
            cmds.connectAttr("{}.visBends".format(leg_settings_ctr),"{}.visibility".format(upleg_bend_ctr))
            cmds.connectAttr("{}.visBends".format(leg_settings_ctr),"{}.visibility".format(knee_bend_ctr))
            cmds.connectAttr("{}.visBends".format(leg_settings_ctr),"{}.visibility".format(lowleg_bend_ctr))
            Hide(leg_main_ik)
            Hide(hip_non_roll_grp)
            Hide(upleg_twist_ik)
            Hide(lowleg_roll_system)
            Hide(upleg_twist_crv)
            Hide(lowleg_twist_crv)
            Hide(hip_stretch)
            Hide(legbend_cluster_a)
            Hide(legbend_cluster_b)
            Hide(legbend_cluster_c)
            Hide(legbend_cluster_d)
            Hide(legbend_cluster_e)
            last_upleg_twist = cmds.rename(last_upleg_twist,"{}_{}_jnt_{}".format(last_upleg_twist.split("_")[0],side_l,number_l_r))
            last_lowleg_twist = cmds.rename(last_lowleg_twist,"{}_{}_jnt_{}".format(last_lowleg_twist.split("_")[0],side_l,number_l_r))
            LockScaleVis(foot_ik_ctr)
            LockScaleRotVis(hip_ctr)
            LockScaleRotVis(leg_pole_ctr)
            LockScaleRotVis(upleg_bend_ctr)
            LockScaleRotVis(knee_bend_ctr)
            LockScaleRotVis(lowleg_bend_ctr)
            LockScaleTransVis(toe_ctr)
            LockScaleTransVis(hip_fk_ctr)
            LockScaleTransVis(knee_fk_ctr)
            LockScaleTransVis(foot_fk_ctr)
            LockAll(leg_settings_ctr)
            createLegSnap(number_l_r,side_l)
            
        win.legRightButton.clicked.connect(BuildRightLeg)
        
        def BuildLeftFinger():
            side_f = "l"
            parent_fin_check = win.checkBoxFingerHandConexion.isChecked()
            parent_fin_num = win.spinFingerHandConexion.value()
            
            fin_sec_a = "fingerSectionA_{}_loc_{}".format(side_f,number_f_l)
            fin_sec_b = "fingerSectionB_{}_loc_{}".format(side_f,number_f_l)
            fin_sec_c = "fingerSectionC_{}_loc_{}".format(side_f,number_f_l)
            fin_end = "fingerEnd_{}_loc_{}".format(side_f,number_f_l)
            
            
            
            del_cons = cmds.aimConstraint(fin_sec_b,
                                            fin_sec_a,
                                            offset=(0,0,0),
                                            weight=1,
                                            aimVector=(1,0,0),
                                            upVector=(0,1,0),
                                            worldUpType="scene")[0]
            cmds.delete(del_cons)
            
            del_cons = cmds.aimConstraint(fin_sec_c,
                                            fin_sec_b,
                                            offset=(0,0,0),
                                            weight=1,
                                            aimVector=(1,0,0),
                                            upVector=(0,1,0),
                                            worldUpType="scene")[0]
            cmds.delete(del_cons)
            
            del_cons = cmds.aimConstraint(fin_end,
                                            fin_sec_c,
                                            offset=(0,0,0),
                                            weight=1,
                                            aimVector=(1,0,0),
                                            upVector=(0,1,0),
                                            worldUpType="scene")[0]
            cmds.delete(del_cons)
            
            del_cons = cmds.aimConstraint(fin_sec_c,
                                            fin_end,
                                            offset=(0,0,0),
                                            weight=1,
                                            aimVector=(-1,0,0),
                                            upVector=(0,1,0),
                                            worldUpType="scene")[0]
            cmds.delete(del_cons)
            
            cmds.select(cl=True)
            fin_sec_a_jnt = cmds.joint(n="fingerSectionA_{}_skn_{}".format(side_f,number_f_l))
            fin_sec_b_jnt = cmds.joint(n="fingerSectionB_{}_skn_{}".format(side_f,number_f_l))
            fin_sec_c_jnt = cmds.joint(n="fingerSectionC_{}_skn_{}".format(side_f,number_f_l))
            fin_end_jnt = cmds.joint(n="fingerEnd_{}_jnt_{}".format(side_f,number_f_l))
            
            cmds.matchTransform(fin_sec_a_jnt,fin_sec_a,pos=True,rot=True,scl=False)
            cmds.matchTransform(fin_sec_b_jnt,fin_sec_b,pos=True,rot=True,scl=False)
            cmds.matchTransform(fin_sec_c_jnt,fin_sec_c,pos=True,rot=True,scl=False)
            cmds.matchTransform(fin_end_jnt,fin_end,pos=True,rot=True,scl=False)
            if parent_fin_check is True:
                cmds.parent(fin_sec_a_jnt,"hand_{}_skn_{}".format(side_f,parent_fin_num))
            
            fin_sec_a_ctr = cmds.circle(c=(0,0,0),nr=(90,0,0),sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=0,n="fingerSectionA_{}_ctr_{}".format(side_f,number_f_l))[0]
            fin_sec_b_ctr = cmds.circle(c=(0,0,0),nr=(90,0,0),sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=0,n="fingerSectionB_{}_ctr_{}".format(side_f,number_f_l))[0] 
            fin_sec_c_ctr = cmds.circle(c=(0,0,0),nr=(90,0,0),sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=0,n="fingerSectionC_{}_ctr_{}".format(side_f,number_f_l))[0] 
            
            cmds.matchTransform(fin_sec_a_ctr,fin_sec_a_jnt,pos=True,rot=True,scl=False)
            cmds.matchTransform(fin_sec_b_ctr,fin_sec_b_jnt,pos=True,rot=True,scl=False)
            cmds.matchTransform(fin_sec_c_ctr,fin_sec_c_jnt,pos=True,rot=True,scl=False) 
            
            fin_sec_a_offset = CreateOffset(fin_sec_a_ctr,number_f_l)
            fin_sec_b_offset = CreateOffset(fin_sec_b_ctr,number_f_l)
            fin_sec_c_offset = CreateOffset(fin_sec_c_ctr,number_f_l)
            
            cmds.parent(fin_sec_c_offset,fin_sec_b_ctr)
            cmds.parent(fin_sec_b_offset,fin_sec_a_ctr)
            if parent_fin_check is True:
                finger_hand_ik_cns = cmds.parentConstraint("handFK_{}_ctr_{}".format(side_f,parent_fin_num),"handIK_{}_ctr_{}".format(side_f,parent_fin_num),fin_sec_a_offset,mo=True,n="fingerHandIkParent_{}_cns_{}".format(side_f,number_f_l))[0]
                cmds.connectAttr("armIk_{}_rev_{}.outputX".format(side_f,parent_fin_num),"{}.handFK_{}_ctr_{}W0".format(finger_hand_ik_cns,side_f,parent_fin_num))
                cmds.connectAttr("armSettings_{}_ctr_{}.armIK".format(side_f,parent_fin_num),"{}.handIK_{}_ctr_{}W1".format(finger_hand_ik_cns,side_f,parent_fin_num))
                cmds.parent(fin_sec_a_offset,hand_rig)
                cmds.connectAttr("armSettings_{}_ctr_{}.visFingers".format(side_f,parent_fin_num),"{}.visibility".format(fin_sec_a_ctr))
                cmds.connectAttr("armSettings_{}_ctr_{}.visFingers".format(side_f,parent_fin_num),"{}.visibility".format(fin_sec_b_ctr))
                cmds.connectAttr("armSettings_{}_ctr_{}.visFingers".format(side_f,parent_fin_num),"{}.visibility".format(fin_sec_c_ctr))
            
            cmds.parentConstraint(fin_sec_a_ctr,fin_sec_a_jnt,mo=False,n="fingerSectionAParent_{}_cns_{}".format(side_f,number_f_l))
            cmds.parentConstraint(fin_sec_b_ctr,fin_sec_b_jnt,mo=False,n="fingerSectionBParent_{}_cns_{}".format(side_f,number_f_l))
            cmds.parentConstraint(fin_sec_c_ctr,fin_sec_c_jnt,mo=False,n="fingerSectionCParent_{}_cns_{}".format(side_f,number_f_l))
            LockScaleTransVis(fin_sec_a)
            LockScaleTransVis(fin_sec_b)
            LockScaleTransVis(fin_sec_c)
            LockScaleTransVis(fin_end)
        
        win.fingerLeftButton.clicked.connect(BuildLeftFinger)
        
        def BuildRightFinger():
            side_f = "r"
            parent_fin_check = win.checkBoxFingerHandConexion.isChecked()
            parent_fin_num = win.spinFingerHandConexion.value()
            
            fin_sec_a = "fingerSectionA_{}_loc_{}".format(side_f,number_f_r)
            fin_sec_b = "fingerSectionB_{}_loc_{}".format(side_f,number_f_r)
            fin_sec_c = "fingerSectionC_{}_loc_{}".format(side_f,number_f_r)
            fin_end = "fingerEnd_{}_loc_{}".format(side_f,number_f_r)
            
            
            
            del_cons = cmds.aimConstraint(fin_sec_b,
                                            fin_sec_a,
                                            offset=(0,0,0),
                                            weight=1,
                                            aimVector=(1,0,0),
                                            upVector=(0,1,0),
                                            worldUpType="scene")[0]
            cmds.delete(del_cons)
            
            del_cons = cmds.aimConstraint(fin_sec_c,
                                            fin_sec_b,
                                            offset=(0,0,0),
                                            weight=1,
                                            aimVector=(1,0,0),
                                            upVector=(0,1,0),
                                            worldUpType="scene")[0]
            cmds.delete(del_cons)
            
            del_cons = cmds.aimConstraint(fin_end,
                                            fin_sec_c,
                                            offset=(0,0,0),
                                            weight=1,
                                            aimVector=(1,0,0),
                                            upVector=(0,1,0),
                                            worldUpType="scene")[0]
            cmds.delete(del_cons)
            
            del_cons = cmds.aimConstraint(fin_sec_c,
                                            fin_end,
                                            offset=(0,0,0),
                                            weight=1,
                                            aimVector=(-1,0,0),
                                            upVector=(0,1,0),
                                            worldUpType="scene")[0]
            cmds.delete(del_cons)
            
            cmds.select(cl=True)
            fin_sec_a_jnt = cmds.joint(n="fingerSectionA_{}_skn_{}".format(side_f,number_f_r))
            fin_sec_b_jnt = cmds.joint(n="fingerSectionB_{}_skn_{}".format(side_f,number_f_r))
            fin_sec_c_jnt = cmds.joint(n="fingerSectionC_{}_skn_{}".format(side_f,number_f_r))
            fin_end_jnt = cmds.joint(n="fingerEnd_{}_jnt_{}".format(side_f,number_f_r))
            
            cmds.matchTransform(fin_sec_a_jnt,fin_sec_a,pos=True,rot=True,scl=False)
            cmds.matchTransform(fin_sec_b_jnt,fin_sec_b,pos=True,rot=True,scl=False)
            cmds.matchTransform(fin_sec_c_jnt,fin_sec_c,pos=True,rot=True,scl=False)
            cmds.matchTransform(fin_end_jnt,fin_end,pos=True,rot=True,scl=False)
            if parent_fin_check is True:
                cmds.parent(fin_sec_a_jnt,"hand_{}_skn_{}".format(side_f,parent_fin_num))
            
            fin_sec_a_ctr = cmds.circle(c=(0,0,0),nr=(90,0,0),sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=0,n="fingerSectionA_{}_ctr_{}".format(side_f,number_f_r))[0]
            fin_sec_b_ctr = cmds.circle(c=(0,0,0),nr=(90,0,0),sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=0,n="fingerSectionB_{}_ctr_{}".format(side_f,number_f_r))[0] 
            fin_sec_c_ctr = cmds.circle(c=(0,0,0),nr=(90,0,0),sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=0,n="fingerSectionC_{}_ctr_{}".format(side_f,number_f_r))[0] 
            
            cmds.matchTransform(fin_sec_a_ctr,fin_sec_a_jnt,pos=True,rot=True,scl=False)
            cmds.matchTransform(fin_sec_b_ctr,fin_sec_b_jnt,pos=True,rot=True,scl=False)
            cmds.matchTransform(fin_sec_c_ctr,fin_sec_c_jnt,pos=True,rot=True,scl=False) 
            
            fin_sec_a_offset = CreateOffset(fin_sec_a_ctr,number_f_r)
            fin_sec_b_offset = CreateOffset(fin_sec_b_ctr,number_f_r)
            fin_sec_c_offset = CreateOffset(fin_sec_c_ctr,number_f_r)
            
            cmds.parent(fin_sec_c_offset,fin_sec_b_ctr)
            cmds.parent(fin_sec_b_offset,fin_sec_a_ctr)
            if parent_fin_check is True:
                finger_hand_ik_cns = cmds.parentConstraint("handFK_{}_ctr_{}".format(side_f,parent_fin_num),"handIK_{}_ctr_{}".format(side_f,parent_fin_num),fin_sec_a_offset,mo=True,n="fingerHandIkParent_{}_cns_{}".format(side_f,number_f_r))[0]
                cmds.connectAttr("armIk_{}_rev_{}.outputX".format(side_f,parent_fin_num),"{}.handFK_{}_ctr_{}W0".format(finger_hand_ik_cns,side_f,parent_fin_num))
                cmds.connectAttr("armSettings_{}_ctr_{}.armIK".format(side_f,parent_fin_num),"{}.handIK_{}_ctr_{}W1".format(finger_hand_ik_cns,side_f,parent_fin_num))
                cmds.parent(fin_sec_a_offset,hand_rig)
                cmds.connectAttr("armSettings_{}_ctr_{}.visFingers".format(side_f,parent_fin_num),"{}.visibility".format(fin_sec_a_ctr))
                cmds.connectAttr("armSettings_{}_ctr_{}.visFingers".format(side_f,parent_fin_num),"{}.visibility".format(fin_sec_b_ctr))
                cmds.connectAttr("armSettings_{}_ctr_{}.visFingers".format(side_f,parent_fin_num),"{}.visibility".format(fin_sec_c_ctr))
            
            cmds.parentConstraint(fin_sec_a_ctr,fin_sec_a_jnt,mo=False,n="fingerSectionAParent_{}_cns_{}".format(side_f,number_f_r))
            cmds.parentConstraint(fin_sec_b_ctr,fin_sec_b_jnt,mo=False,n="fingerSectionBParent_{}_cns_{}".format(side_f,number_f_r))
            cmds.parentConstraint(fin_sec_c_ctr,fin_sec_c_jnt,mo=False,n="fingerSectionCParent_{}_cns_{}".format(side_f,number_f_r))
            LockScaleTransVis(fin_sec_a)
            LockScaleTransVis(fin_sec_b)
            LockScaleTransVis(fin_sec_c)
            LockScaleTransVis(fin_end)
        
        win.fingerRightButton.clicked.connect(BuildRightFinger)

        def Finish():
            # Bloqueo y finalizacion de rig   
            win.close()
            # Borrar controles limpios
            cmds.delete("controles")
            
            # Esconder locators y points
            Hide(body_locs)
            points_check = cmds.objExists("*_point_*")
            if points_check is True:
                point_group = cmds.listRelatives(cmds.ls("*_point_*")[0],parent=True)[0]
                Hide(point_group)
            # Poner huesos no skineables en none 
            noskin_jnt_list = cmds.ls(type="joint")
            for noskin_jnt in noskin_jnt_list:
                usage = noskin_jnt.split("_")[2]
                if "jnt" in usage:
                    cmds.setAttr("{}.drawStyle".format(noskin_jnt),2)
                
            # Lockear offsets de controles
            cmds.select(cl=True)
            cmds.select("*_ctr_*")
            controls = cmds.ls(sl=1,type="transform")
            for paren in controls:
                offset = cmds.listRelatives(paren,p=True)[0]
                usage = offset.split("_")[2]
                if "zero" in usage:
                    LockAll(offset)
        win.pushButtonFinishSpine.clicked.connect(Finish)
        win.pushButtonFinishNeck.clicked.connect(Finish)
        win.pushButtonFinishClavicle.clicked.connect(Finish)
        win.pushButtonFinishArm.clicked.connect(Finish)
        win.pushButtonFinishLeg.clicked.connect(Finish)
        win.pushButtonFinishPoints.clicked.connect(Finish)
        win.pushButtonFinishFinger.clicked.connect(Finish)
        min.close() 
    min.pushButtonStart.clicked.connect(ModularAutorigBuilder)
