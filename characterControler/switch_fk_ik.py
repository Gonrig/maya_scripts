#Match IK/FK, Gonzalo Berrocal
#IK to FK:
    #char_ac_lf_shoulderFK == char_sk_lf_shoulder
    #char_ac_lf_elbowFK == char_sk_lf_elbow
    #char_ac_lf_handFK == char_sk_lf_hand
ref = ""
def SwitchFunction():    
    import maya.cmds as cmds
    from maya.api import OpenMaya
    import pyside_utils
    import os 
    import sys  
    sistemaop = sys.platform
    windows = ["win32", "win64"]
    mac = "darwin"
    homedir = os.path.expanduser("~")
    
    for win in windows:
    	if sistemaop == win:
    		homedir_win = "{}/maya/scripts/characterControler".format(homedir)
    		homedir_window = "{}/windows".format(homedir_win)
    		
    if sistemaop == mac:
    	homedir_mac = "{}/Documents/maya/characterControler".format(homedir)
    	homedir_window = "{}/windows".format(homedir_mac)
    
    	
    
    win = pyside_utils.loadUi("{}/ventanaik.ui".format(homedir_window))
    
    def setNameSpace():
        character_name = win.name_combobox.currentText()
        try:
            cmds.select("*{}".format(character_name))
        except ValueError:
            cmds.select("*:{}".format(character_name))
        x = len(character_name)
        character_ref = cmds.pickWalk(d="up")[0]
        n = len(character_ref) - x
        global ref
        ref = character_ref[:n]
        return ref
    try:    
        setNameSpace()
    except ValueError:
        global ref
        ref = ""
    win.set_namespace_buttom.clicked.connect(setNameSpace)
    def match_tranform(match_list):
        for matches in match_list:
            source = matches[1]
            dest = matches[0]
            pos = cmds.xform(source, q=1, ws=1, t=1)
            rot = cmds.xform(source, q=1, ws=1, ro=1)
            cmds.xform(dest, ws=1, t=pos)
            cmds.xform(dest, ws=1, ro= rot)
     
    def transfer_stretch(tran_dict):
        for elm in tran_dict:
            dest = elm
            source = tran_dict[elm]
            curr_val = cmds.getAttr(source)
            cmds.setAttr(dest,curr_val) 
    
    def setAttrbutes(attr_list):
        attr_name = attr_list[0]
        value = attr_list[1]
        cmds.setAttr(attr_name,value)
    
    
    def matchFK(side):
        match_list = [["{}shoulderFK_{}_ctr_1".format(ref,side), "{}shoulderFK_{}_snap_1".format(ref,side)],["{}elbowFK_{}_ctr_1".format(ref,side),"{}elbowFK_{}_snap_1".format(ref,side)],["{}handFK_{}_ctr_1".format(ref,side),"{}handFK_{}_snap_1".format(ref,side)]]
        tran_dict = {"{}shoulderFK_{}_ctr_1.stretch".format(ref,side):"{}shoulder_{}_jnt_1.scaleX".format(ref,side),"{}elbowFK_{}_ctr_1.stretch".format(ref,side):"{}elbow_{}_jnt_1.scaleX".format(ref,side)}
        attr_list = ["{}armSettings_{}_ctr_1.armIK".format(ref,side), 0]
        
        match_tranform(match_list)
        transfer_stretch(tran_dict)
        setAttrbutes(attr_list)
    #FK to IK
    #char_ac_lf_handIK == char_sk_lf_hand
    def poleVector(start_trf, midle_trf, end_trf, pole_vector_ctrl, offset = 5):
        start_pos = cmds.xform(start_trf ,q= 1 ,ws = 1,t =1 )
        mid_pos = cmds.xform(midle_trf ,q= 1 ,ws = 1,t =1 )
        end_pos = cmds.xform(end_trf ,q= 1 ,ws = 1,t =1 )
        start_vec = OpenMaya.MVector(start_pos)
        mid_vec = OpenMaya.MVector(mid_pos)
        end_vec = OpenMaya.MVector(end_pos)
        
        startEnd = end_vec - start_vec
        startMid = mid_vec - start_vec
    
        proj = startMid * startEnd.normal()
    
        projV = startEnd.normal() * proj
    
        arrowV = startMid - projV
        
        finalV = (arrowV.normal()*offset) + mid_vec
        cmds.xform(pole_vector_ctrl, ws=1, t=list(finalV))

    def matchIK(side):
        poleVector_dict = {"start":"{}shoulder_{}_jnt_1".format(ref,side), "end":"{}hand_{}_skn_1".format(ref,side), "mid":"{}elbow_{}_jnt_1".format(ref,side), "pole":"{}armPole_{}_ctr_1".format(ref,side)}    
        matchik_list = [["{}handIK_{}_ctr_1".format(ref,side), "{}handIK_{}_snap_1".format(ref,side)]]
        attr_list_ik = ["{}armSettings_{}_ctr_1.armIK".format(ref,side), 1]
        match_tranform(matchik_list)
        poleVector(poleVector_dict["start"], poleVector_dict["mid"], poleVector_dict["end"],  poleVector_dict["pole"])
        setAttrbutes(attr_list_ik)
    def switchIKFK(side):
        attr_switch = cmds.getAttr("{}armSettings_{}_ctr_1.armIK".format(ref,side))
        if attr_switch == 1:
            matchFK(side)
        else:
            matchIK(side)
    def switchIKFKrt():
        switchIKFK("r")
    def switchIKFKlf():
        switchIKFK("l") 
    
    win.arm_rt_button_one.clicked.connect(switchIKFKrt)
    win.arm_lf_button_one.clicked.connect(switchIKFKlf)
    
    
    def matchFK_leg(side):
        match_list = [["{}hipFK_{}_ctr_1".format(ref,side), "{}hipFK_{}_snap_1".format(ref,side)],["{}kneeFK_{}_ctr_1".format(ref,side),"{}kneeFK_{}_snap_1".format(ref,side)],["{}footFK_{}_ctr_1".format(ref,side),"{}footFK_{}_snap_1".format(ref,side)]]
        tran_dict = {"{}hipFK_{}_ctr_1.stretch".format(ref,side):"{}hip_{}_jnt_1.scaleX".format(ref,side),"{}kneeFK_{}_ctr_1.stretch".format(ref,side):"{}knee_{}_jnt_1.scaleX".format(ref,side)}
        attr_list = ["{}legSettings_{}_ctr_1.legIK".format(ref,side), 0]
        
        match_tranform(match_list)
        transfer_stretch(tran_dict)
        setAttrbutes(attr_list)
    
    def matchIK_leg(side):
        poleVector_dict = {"start":"{}hip_{}_jnt_1".format(ref,side), "end":"{}foot_{}_skn_1".format(ref,side), "mid":"{}knee_{}_jnt_1".format(ref,side), "pole":"{}legPole_{}_ctr_1".format(ref,side)}    
        matchik_list = [["{}footIK_{}_ctr_1".format(ref,side), "{}footIK_{}_snap_1".format(ref,side)]]
        attr_list_ik = ["{}legSettings_{}_ctr_1.legIK".format(ref,side), 1]
        match_tranform(matchik_list)
        poleVector(poleVector_dict["start"], poleVector_dict["mid"], poleVector_dict["end"],  poleVector_dict["pole"])
        setAttrbutes(attr_list_ik)
        
    def switchIKFK_leg(side):
        attr_switch = cmds.getAttr("{}legSettings_{}_ctr_1.legIK".format(ref,side))
        if attr_switch == 1:
            matchFK_leg(side)
        else:
            matchIK_leg(side)      
    def switchIKFKrt_leg():
        switchIKFK_leg("r")
    def switchIKFKlf_leg():
        switchIKFK_leg("l") 
       
    win.leg_rt_button.clicked.connect(switchIKFKrt_leg)
    win.leg_lf_button.clicked.connect(switchIKFKlf_leg)
    
    def selectAllControls():
        ctrs_list =[u'armPole_l_ctr_1', u'armPole_r_ctr_1', u'armSettings_l_ctr_1', u'armSettings_r_ctr_1', u'base_c_ctr_1', u'center_c_ctr_1', u'chest_c_ctr_1', u'clavicle_l_ctr_1', u'clavicle_r_ctr_1', u'dwFinger01_l_ctr_1', u'dwFinger01_r_ctr_1', u'dwFinger02_l_ctr_1', u'dwFinger02_r_ctr_1', u'dwFinger03_l_ctr_1', u'dwFinger03_r_ctr_1', u'dwThumb_l_ctr_1', u'dwThumb_r_ctr_1', u'elbowBend_l_ctr_1', u'elbowBend_r_ctr_1', u'elbowFK_l_ctr_1', u'elbowFK_r_ctr_1', u'footFK_l_ctr_1', u'footFK_r_ctr_1', u'footIK_l_ctr_1', u'footIK_r_ctr_1', u'forearmBend_l_ctr_1', u'forearmBend_r_ctr_1', u'handFK_l_ctr_1', u'handFK_r_ctr_1', u'handIK_l_ctr_1', u'handIK_r_ctr_1', u'head_c_ctr_1', u'hipFK_l_ctr_1', u'hipFK_r_ctr_1', u'hip_l_ctr_1', u'hip_r_ctr_1', u'kneeBend_l_ctr_1', u'kneeBend_r_ctr_1', u'kneeFK_l_ctr_1', u'kneeFK_r_ctr_1', u'legPole_l_ctr_1', u'legPole_r_ctr_1', u'legSettings_l_ctr_1', u'legSettings_r_ctr_1', u'lowlegBend_l_ctr_1', u'lowlegBend_r_ctr_1', u'middleFinger01_l_ctr_1', u'middleFinger01_r_ctr_1', u'middleFinger02_l_ctr_1', u'middleFinger02_r_ctr_1', u'middleFinger03_l_ctr_1', u'middleFinger03_r_ctr_1', u'middleNeck_c_ctr_1', u'middleSpineIK_c_ctr_1', u'middleThumb_l_ctr_1', u'middleThumb_r_ctr_1', u'neck_c_ctr_1', u'pelvis_c_ctr_1', u'root_c_ctr_1', u'shoulderFK_l_ctr_1', u'shoulderFK_r_ctr_1', u'spineFK1Inv_c_ctr_1', u'spineFK1_c_ctr_1', u'spineFK2Inv_c_ctr_1', u'spineFK2_c_ctr_1', u'spineFK3Inv_c_ctr_1', u'spineFK3_c_ctr_1', u'toe_l_ctr_1', u'toe_r_ctr_1', u'upFinger01_l_ctr_1', u'upFinger01_r_ctr_1', u'upFinger02_l_ctr_1', u'upFinger02_r_ctr_1', u'upFinger03_l_ctr_1', u'upFinger03_r_ctr_1', u'upThumb_l_ctr_1', u'upThumb_r_ctr_1', u'uparmBend_l_ctr_1', u'uparmBend_r_ctr_1', u'uplegBend_l_ctr_1', u'uplegBend_r_ctr_1'] 
        print "*********************************** OBJECTS SELECTED ***********************************"
        print "****************************************************************************************"
        print "****************************************************************************************"
        select_control_list = []
        for ctr in ctrs_list:
            ctr_name = "{}{}".format(ref,ctr)
            select_control_list.append(ctr_name)
            print ctr_name
        cmds.select(select_control_list)
    win.select_all_controls_button.clicked.connect(selectAllControls)
    def restPose():
        all = win.restpose_all.isChecked()
        ctr_nonArm = ['{}base_c_ctr_1'.format(ref),
                      '{}center_c_ctr_1'.format(ref),
                      '{}chest_c_ctr_1'.format(ref),
                      '{}clavicle_l_ctr_1'.format(ref),
                      '{}clavicle_r_ctr_1'.format(ref),
                      '{}dwFinger01_l_ctr_1'.format(ref),
                      '{}dwFinger01_r_ctr_1'.format(ref),
                      '{}dwFinger02_l_ctr_1'.format(ref),
                      '{}dwFinger02_r_ctr_1'.format(ref),
                      '{}dwFinger03_l_ctr_1'.format(ref),
                      '{}dwFinger03_r_ctr_1'.format(ref),
                      '{}dwThumb_l_ctr_1'.format(ref),
                      '{}dwThumb_r_ctr_1'.format(ref),
                      '{}elbowBend_l_ctr_1'.format(ref),
                      '{}elbowBend_r_ctr_1'.format(ref),
                      '{}elbowFK_l_ctr_1'.format(ref),
                      '{}elbowFK_r_ctr_1'.format(ref),
                      '{}footFK_l_ctr_1'.format(ref),
                      '{}footFK_r_ctr_1'.format(ref),
                      '{}footIK_l_ctr_1'.format(ref),
                      '{}footIK_r_ctr_1'.format(ref),
                      '{}forearmBend_l_ctr_1'.format(ref),
                      '{}forearmBend_r_ctr_1'.format(ref),
                      '{}handFK_l_ctr_1'.format(ref),
                      '{}handFK_r_ctr_1'.format(ref),
                      '{}head_c_ctr_1'.format(ref),
                      '{}hipFK_l_ctr_1'.format(ref),
                      '{}hipFK_r_ctr_1'.format(ref),
                      '{}hip_l_ctr_1'.format(ref),
                      '{}hip_r_ctr_1'.format(ref),
                      '{}kneeBend_l_ctr_1'.format(ref),
                      '{}kneeBend_r_ctr_1'.format(ref),
                      '{}kneeFK_l_ctr_1'.format(ref),
                      '{}kneeFK_r_ctr_1'.format(ref),
                      '{}legPole_l_ctr_1'.format(ref),
                      '{}legPole_r_ctr_1'.format(ref),
                      '{}lowlegBend_l_ctr_1'.format(ref),
                      '{}lowlegBend_r_ctr_1'.format(ref),
                      '{}middleFinger01_l_ctr_1'.format(ref),
                      '{}middleFinger01_r_ctr_1'.format(ref),
                      '{}middleFinger02_l_ctr_1'.format(ref),
                      '{}middleFinger02_r_ctr_1'.format(ref),
                      '{}middleFinger03_l_ctr_1'.format(ref),
                      '{}middleFinger03_r_ctr_1'.format(ref),
                      '{}middleNeck_c_ctr_1'.format(ref),
                      '{}middleSpineIK_c_ctr_1'.format(ref),
                      '{}middleThumb_l_ctr_1'.format(ref),
                      '{}middleThumb_r_ctr_1'.format(ref),
                      '{}neck_c_ctr_1'.format(ref),
                      '{}pelvis_c_ctr_1'.format(ref),
                      '{}root_c_ctr_1'.format(ref),
                      '{}spineFK1Inv_c_ctr_1'.format(ref),
                      '{}spineFK1_c_ctr_1'.format(ref),
                      '{}spineFK2Inv_c_ctr_1'.format(ref),
                      '{}spineFK2_c_ctr_1'.format(ref),
                      '{}spineFK3Inv_c_ctr_1'.format(ref),
                      '{}spineFK3_c_ctr_1'.format(ref),
                      '{}toe_l_ctr_1'.format(ref),
                      '{}toe_r_ctr_1'.format(ref),
                      '{}upFinger01_l_ctr_1'.format(ref),
                      '{}upFinger01_r_ctr_1'.format(ref),
                      '{}upFinger02_l_ctr_1'.format(ref),
                      '{}upFinger02_r_ctr_1'.format(ref),
                      '{}upFinger03_l_ctr_1'.format(ref),
                      '{}upFinger03_r_ctr_1'.format(ref),
                      '{}upThumb_l_ctr_1'.format(ref),
                      '{}upThumb_r_ctr_1'.format(ref),
                      '{}uparmBend_l_ctr_1'.format(ref),
                      '{}uparmBend_r_ctr_1'.format(ref),
                      '{}uplegBend_l_ctr_1'.format(ref),
                      '{}uplegBend_r_ctr_1'.format(ref)]
            
        shoulder_l = "{}shoulderFK_l_ctr_1".format(ref)
        shoulder_r = "{}shoulderFK_r_ctr_1" .format(ref)
        
        handik_l = "{}handIK_l_ctr_1".format(ref)
        handik_r = "{}handIK_r_ctr_1".format(ref)
        
        armpole_l = "{}armPole_l_ctr_1".format(ref)
        armpole_r = "{}armPole_r_ctr_1".format(ref)
        if all == True:
            for ctrs in ctr_nonArm:
                ctrs_attr = cmds.listAttr(ctrs,k=True)
                for x in ctrs_attr:
                    if "translate" in x:
                        cmds.setAttr("{}.{}".format(ctrs,x),0)
                    if "rotate" in x:
                        cmds.setAttr("{}.{}".format(ctrs,x),0)
            
            cmds.setAttr("{}.rx".format(shoulder_l),0)
            cmds.setAttr("{}.rx".format(shoulder_r),0)
            cmds.setAttr("{}.ry".format(shoulder_l),0)
            cmds.setAttr("{}.ry".format(shoulder_r),0)
            cmds.setAttr("{}.rz".format(shoulder_l),0)
            cmds.setAttr("{}.rz".format(shoulder_r),0)
            
            cmds.setAttr("{}.tx".format(handik_l),0)
            cmds.setAttr("{}.ty".format(handik_l),0)
            cmds.setAttr("{}.tz".format(handik_l),0)
            cmds.setAttr("{}.rx".format(handik_l),0)
            cmds.setAttr("{}.ry".format(handik_l),0)
            cmds.setAttr("{}.rz".format(handik_l),0)
            
            cmds.setAttr("{}.tx".format(handik_r),0)
            cmds.setAttr("{}.ty".format(handik_r),0)
            cmds.setAttr("{}.tz".format(handik_r),0)
            cmds.setAttr("{}.rx".format(handik_r),0)
            cmds.setAttr("{}.ry".format(handik_r),0)
            cmds.setAttr("{}.rz".format(handik_r),0)
            
            cmds.setAttr("{}.tx".format(armpole_l),0)
            cmds.setAttr("{}.ty".format(armpole_l),0)
            cmds.setAttr("{}.tz".format(armpole_l),0)
            
            cmds.setAttr("{}.tx".format(armpole_r),0)
            cmds.setAttr("{}.ty".format(armpole_r),0)
            cmds.setAttr("{}.tz".format(armpole_r),0)
            roll_atributes = ["footRoll","footTilt","toeRoll","toeSlide","heelRoll","ballRoll"]
            for side in "lr":
                for r_attr in roll_atributes:
                    cmds.setAttr("{}footIK_{}_ctr_1.{}".format(ref,side,r_attr),0)
        
        else:
            selection_list = cmds.ls(sl=1)
            for selection in selection_list:
                if selection in ctr_nonArm:
                    sel_attr = cmds.listAttr(selection,k=True)
                    for a in sel_attr:
                        if "translate" in a:
                            cmds.setAttr("{}.{}".format(selection,a),0)
                        if "rotate" in a:
                            cmds.setAttr("{}.{}".format(selection,a),0)
                    print selection
                
                elif selection == handik_l:
                    cmds.setAttr("{}.tx".format(handik_l),0)
                    cmds.setAttr("{}.ty".format(handik_l),0)
                    cmds.setAttr("{}.tz".format(handik_l),0)
                    cmds.setAttr("{}.rx".format(handik_l),0)
                    cmds.setAttr("{}.ry".format(handik_l),0)
                    cmds.setAttr("{}.rz".format(handik_l),0)
                    cmds.setAttr("{}.tx".format(armpole_l),0)
                    cmds.setAttr("{}.ty".format(armpole_l),0)
                    cmds.setAttr("{}.tz".format(armpole_l),0)
                    print selection
                
                elif selection == handik_r:
                    cmds.setAttr("{}.tx".format(handik_r),0)
                    cmds.setAttr("{}.ty".format(handik_r),0)
                    cmds.setAttr("{}.tz".format(handik_r),0)
                    cmds.setAttr("{}.rx".format(handik_r),0)
                    cmds.setAttr("{}.ry".format(handik_r),0)
                    cmds.setAttr("{}.rz".format(handik_r),0)
                    cmds.setAttr("{}.tx".format(armpole_r),0)
                    cmds.setAttr("{}.ty".format(armpole_r),0)
                    cmds.setAttr("{}.tz".format(armpole_r),0)
                
                elif selection == shoulder_l:
                    cmds.setAttr("{}.rx".format(shoulder_l),0)
                    cmds.setAttr("{}.ry".format(shoulder_l),0)
                    cmds.setAttr("{}.rz".format(shoulder_l),0)
                
                elif selection == shoulder_r:
                    cmds.setAttr("{}.rx".format(shoulder_r),0)
                    cmds.setAttr("{}.ry".format(shoulder_r),0)
                    cmds.setAttr("{}.rz".format(shoulder_r),0)
                for side in "lr":
                    if selection == "{}footIK_{}_ctr_1".format(ref,side):
                        roll_atributes = ["footRoll","footTilt","toeRoll","toeSlide","heelRoll","ballRoll"]
                        for r_attr in roll_atributes:
                            cmds.setAttr("{}footIK_{}_ctr_1.{}".format(ref,side,r_attr),0)
    def flipPose():
        flip_all_check = win.flippose_all.isChecked()
        if flip_all_check is True:
            center_ctrls = ['{}base_c_ctr_1'.format(ref),
                            '{}center_c_ctr_1'.format(ref),
                            '{}chest_c_ctr_1'.format(ref),
                            '{}head_c_ctr_1'.format(ref),
                            '{}middleNeck_c_ctr_1'.format(ref),
                            '{}middleSpineIK_c_ctr_1'.format(ref),
                            '{}neck_c_ctr_1'.format(ref),
                            '{}pelvis_c_ctr_1'.format(ref),
                            '{}root_c_ctr_1'.format(ref),
                            '{}spineFK1Inv_c_ctr_1'.format(ref),
                            '{}spineFK1_c_ctr_1'.format(ref),
                            '{}spineFK2Inv_c_ctr_1'.format(ref),
                            '{}spineFK2_c_ctr_1'.format(ref),
                            '{}spineFK3Inv_c_ctr_1'.format(ref),
                            '{}spineFK3_c_ctr_1'.format(ref)] 
            
            center_inv_trans = ["tx","ry","rz"]
            for c_ctr in center_ctrls:
                for cit in center_inv_trans:
                    ct_value = cmds.getAttr("{}.{}".format(c_ctr,cit))
                    cit_value = ct_value*-1
                    cmds.setAttr("{}.{}".format(c_ctr,cit),cit_value)
            
            
            #hand FK
            
            hand_fk = "{}handFK_l_ctr_1".format(ref)
            inv_hand_fk = "{}handFK_r_ctr_1".format(ref)
            
            handfk_rx_value = cmds.getAttr("{}.rx".format(hand_fk))
            handfk_ry_value = cmds.getAttr("{}.ry".format(hand_fk))
            handfk_rz_value = cmds.getAttr("{}.rz".format(hand_fk))
            
            invhandfk_rx_value = cmds.getAttr("{}.rx".format(inv_hand_fk))
            invhandfk_ry_value = cmds.getAttr("{}.ry".format(inv_hand_fk))
            invhandfk_rz_value = cmds.getAttr("{}.rz".format(inv_hand_fk))
            
            cmds.setAttr("{}.rx".format(hand_fk),invhandfk_rx_value*-1)
            cmds.setAttr("{}.ry".format(hand_fk),invhandfk_ry_value*-1)
            cmds.setAttr("{}.rz".format(hand_fk),invhandfk_rz_value)
            
            cmds.setAttr("{}.rx".format(inv_hand_fk),handfk_rx_value*-1)
            cmds.setAttr("{}.ry".format(inv_hand_fk),handfk_ry_value*-1)
            cmds.setAttr("{}.rz".format(inv_hand_fk),handfk_rz_value)
            
            #elbow FK
            
            elbow_fk = "{}elbowFK_l_ctr_1".format(ref)
            inv_elbow_fk = "{}elbowFK_r_ctr_1".format(ref)
            
            elbowfk_rx_value = cmds.getAttr("{}.rx".format(elbow_fk))
            elbowfk_ry_value = cmds.getAttr("{}.ry".format(elbow_fk))
            elbowfk_rz_value = cmds.getAttr("{}.rz".format(elbow_fk))
            
            invelbowfk_rx_value = cmds.getAttr("{}.rx".format(inv_elbow_fk))
            invelbowfk_ry_value = cmds.getAttr("{}.ry".format(inv_elbow_fk))
            invelbowfk_rz_value = cmds.getAttr("{}.rz".format(inv_elbow_fk))
            
            cmds.setAttr("{}.rx".format(elbow_fk),invelbowfk_rx_value*-1)
            cmds.setAttr("{}.ry".format(elbow_fk),invelbowfk_ry_value*-1)
            cmds.setAttr("{}.rz".format(elbow_fk),invelbowfk_rz_value)
            
            cmds.setAttr("{}.rx".format(inv_elbow_fk),elbowfk_rx_value*-1)
            cmds.setAttr("{}.ry".format(inv_elbow_fk),elbowfk_ry_value*-1)
            cmds.setAttr("{}.rz".format(inv_elbow_fk),elbowfk_rz_value)
            
            #shoulder FK
            
            shoulder_fk = "{}shoulderFK_l_ctr_1".format(ref)
            inv_shoulder_fk = "{}shoulderFK_r_ctr_1".format(ref)
            
            shoulderfk_rx_value = cmds.getAttr("{}.rx".format(shoulder_fk))
            shoulderfk_ry_value = cmds.getAttr("{}.ry".format(shoulder_fk))
            shoulderfk_rz_value = cmds.getAttr("{}.rz".format(shoulder_fk))
            
            invshoulderfk_rx_value = cmds.getAttr("{}.rx".format(inv_shoulder_fk))
            invshoulderfk_ry_value = cmds.getAttr("{}.ry".format(inv_shoulder_fk))
            invshoulderfk_rz_value = cmds.getAttr("{}.rz".format(inv_shoulder_fk))
            
            cmds.setAttr("{}.rx".format(shoulder_fk),invshoulderfk_rx_value*-1)
            cmds.setAttr("{}.ry".format(shoulder_fk),invshoulderfk_ry_value*-1)
            cmds.setAttr("{}.rz".format(shoulder_fk),invshoulderfk_rz_value)
            
            cmds.setAttr("{}.rx".format(inv_shoulder_fk),shoulderfk_rx_value*-1)
            cmds.setAttr("{}.ry".format(inv_shoulder_fk),shoulderfk_ry_value*-1)
            cmds.setAttr("{}.rz".format(inv_shoulder_fk),shoulderfk_rz_value)
            
            shoulderfk_chest_value = cmds.getAttr("{}.chestSpace".format(shoulder_fk))
            invshoulderfk_chest_value = cmds.getAttr("{}.chestSpace".format(inv_shoulder_fk))
            cmds.setAttr("{}.chestSpace".format(shoulder_fk),invshoulderfk_chest_value)
            cmds.setAttr("{}.chestSpace".format(inv_shoulder_fk),shoulderfk_chest_value)
            
            #clavicle
            clavicle = "{}clavicle_l_ctr_1".format(ref)
            inv_clavicle = "{}clavicle_r_ctr_1".format(ref)
            
            for trans in "rt":
                for axis in "xyz":
                    clavicle_value = cmds.getAttr("{}.{}{}".format(clavicle,trans,axis))
                    invclavicle_value = cmds.getAttr("{}.{}{}".format(inv_clavicle,trans,axis))
                    cmds.setAttr("{}.{}{}".format(clavicle,trans,axis),invclavicle_value)
                    cmds.setAttr("{}.{}{}".format(inv_clavicle,trans,axis),clavicle_value)
                    
            #footik        
            
            foot_ik = "{}footIK_l_ctr_1".format(ref)
            inv_foot_ik = "{}footIK_r_ctr_1".format(ref)
            
            footik_rx_value = cmds.getAttr("{}.rx".format(foot_ik))
            footik_ry_value = cmds.getAttr("{}.ry".format(foot_ik))
            footik_rz_value = cmds.getAttr("{}.rz".format(foot_ik))
            footik_tx_value = cmds.getAttr("{}.tx".format(foot_ik))
            footik_ty_value = cmds.getAttr("{}.ty".format(foot_ik))
            footik_tz_value = cmds.getAttr("{}.tz".format(foot_ik))
            
            invfootik_rx_value = cmds.getAttr("{}.rx".format(inv_foot_ik))
            invfootik_ry_value = cmds.getAttr("{}.ry".format(inv_foot_ik))
            invfootik_rz_value = cmds.getAttr("{}.rz".format(inv_foot_ik))
            invfootik_tx_value = cmds.getAttr("{}.tx".format(inv_foot_ik))
            invfootik_ty_value = cmds.getAttr("{}.ty".format(inv_foot_ik))
            invfootik_tz_value = cmds.getAttr("{}.tz".format(inv_foot_ik))
            
            
            cmds.setAttr("{}.rx".format(foot_ik),invfootik_rx_value)
            cmds.setAttr("{}.ry".format(foot_ik),invfootik_ry_value*-1)
            cmds.setAttr("{}.rz".format(foot_ik),invfootik_rz_value*-1)
            cmds.setAttr("{}.tx".format(foot_ik),invfootik_tx_value*-1)
            cmds.setAttr("{}.ty".format(foot_ik),invfootik_ty_value)
            cmds.setAttr("{}.tz".format(foot_ik),invfootik_tz_value)
            
            cmds.setAttr("{}.rx".format(inv_foot_ik),footik_rx_value)
            cmds.setAttr("{}.ry".format(inv_foot_ik),footik_ry_value*-1)
            cmds.setAttr("{}.rz".format(inv_foot_ik),footik_rz_value*-1)
            cmds.setAttr("{}.tx".format(inv_foot_ik),footik_tx_value*-1)
            cmds.setAttr("{}.ty".format(inv_foot_ik),footik_ty_value)
            cmds.setAttr("{}.tz".format(inv_foot_ik),footik_tz_value)
            
            
            roll_attr = ["knee","autoStretch","footRoll","toeBreak","releaseAngle","footTilt","toeRoll","toeSlide","heelRoll","ballRoll"]
            
            for r_attr in roll_attr:
                footik_roll_value = cmds.getAttr("{}.{}".format(foot_ik,r_attr))
                invfootik_roll_value = cmds.getAttr("{}.{}".format(inv_foot_ik,r_attr))
                cmds.setAttr("{}.{}".format(foot_ik,r_attr),invfootik_roll_value)
                cmds.setAttr("{}.{}".format(inv_foot_ik,r_attr),footik_roll_value)
            
            
            #toe
            
            toe = "{}toe_l_ctr_1".format(ref)
            inv_toe = "{}toe_r_ctr_1".format(ref)
            
            toe_rx_value = cmds.getAttr("{}.rx".format(toe))
            toe_ry_value = cmds.getAttr("{}.ry".format(toe))
            toe_rz_value = cmds.getAttr("{}.rz".format(toe))
            
            invtoe_rx_value = cmds.getAttr("{}.rx".format(inv_toe))
            invtoe_ry_value = cmds.getAttr("{}.ry".format(inv_toe))
            invtoe_rz_value = cmds.getAttr("{}.rz".format(inv_toe))
            
            cmds.setAttr("{}.rx".format(toe),invtoe_rx_value)
            cmds.setAttr("{}.ry".format(toe),invtoe_ry_value*-1)
            cmds.setAttr("{}.rz".format(toe),invtoe_rz_value*-1)
            
            cmds.setAttr("{}.rx".format(inv_toe),toe_rx_value)
            cmds.setAttr("{}.ry".format(inv_toe),toe_ry_value*-1)
            cmds.setAttr("{}.rz".format(inv_toe),toe_rz_value*-1)
            
            
            #legPole
            
            leg_pole = "{}legPole_l_ctr_1".format(ref)
            inv_leg_pole = "{}legPole_r_ctr_1".format(ref)
            
            legpole_tx_value = cmds.getAttr("{}.tx".format(leg_pole))
            legpole_ty_value = cmds.getAttr("{}.ty".format(leg_pole))
            legpole_tz_value = cmds.getAttr("{}.tz".format(leg_pole))
            
            invlegpole_tx_value = cmds.getAttr("{}.tx".format(inv_leg_pole))
            invlegpole_ty_value = cmds.getAttr("{}.ty".format(inv_leg_pole))
            invlegpole_tz_value = cmds.getAttr("{}.tz".format(inv_leg_pole))
            
            cmds.setAttr("{}.tx".format(leg_pole),invlegpole_tx_value*-1)
            cmds.setAttr("{}.ty".format(leg_pole),invlegpole_ty_value)
            cmds.setAttr("{}.tz".format(leg_pole),invlegpole_tz_value)
            
            cmds.setAttr("{}.tx".format(inv_leg_pole),legpole_tx_value*-1)
            cmds.setAttr("{}.ty".format(inv_leg_pole),legpole_ty_value)
            cmds.setAttr("{}.tz".format(inv_leg_pole),legpole_tz_value)
            
            #handIK
            
            hand_ik = "{}handIK_l_ctr_1".format(ref)
            inv_hand_ik = "{}handIK_r_ctr_1".format(ref)
            
            handik_rx_value = cmds.getAttr("{}.rx".format(hand_ik))
            handik_ry_value = cmds.getAttr("{}.ry".format(hand_ik))
            handik_rz_value = cmds.getAttr("{}.rz".format(hand_ik))
            handik_tx_value = cmds.getAttr("{}.tx".format(hand_ik))
            handik_ty_value = cmds.getAttr("{}.ty".format(hand_ik))
            handik_tz_value = cmds.getAttr("{}.tz".format(hand_ik))
            
            invhandik_rx_value = cmds.getAttr("{}.rx".format(inv_hand_ik))
            invhandik_ry_value = cmds.getAttr("{}.ry".format(inv_hand_ik))
            invhandik_rz_value = cmds.getAttr("{}.rz".format(inv_hand_ik))
            invhandik_tx_value = cmds.getAttr("{}.tx".format(inv_hand_ik))
            invhandik_ty_value = cmds.getAttr("{}.ty".format(inv_hand_ik))
            invhandik_tz_value = cmds.getAttr("{}.tz".format(inv_hand_ik))
            
            
            
            cmds.setAttr("{}.rx".format(hand_ik),invhandik_rx_value*-1)
            cmds.setAttr("{}.ry".format(hand_ik),invhandik_ry_value*-1)
            cmds.setAttr("{}.rz".format(hand_ik),invhandik_rz_value)
            cmds.setAttr("{}.tx".format(hand_ik),invhandik_tx_value)
            cmds.setAttr("{}.ty".format(hand_ik),invhandik_ty_value)
            cmds.setAttr("{}.tz".format(hand_ik),invhandik_tz_value*-1)
            
            
            cmds.setAttr("{}.rx".format(inv_hand_ik),handik_rx_value*-1)
            cmds.setAttr("{}.ry".format(inv_hand_ik),handik_ry_value*-1)
            cmds.setAttr("{}.rz".format(inv_hand_ik),handik_rz_value)
            cmds.setAttr("{}.tx".format(inv_hand_ik),handik_tx_value)
            cmds.setAttr("{}.ty".format(inv_hand_ik),handik_ty_value)
            cmds.setAttr("{}.tz".format(inv_hand_ik),handik_tz_value*-1)
            
            
            #armPole
            
            arm_pole = "{}armPole_l_ctr_1".format(ref)
            inv_arm_pole = "{}armPole_r_ctr_1".format(ref)
            
            
            armpole_tx_value = cmds.getAttr("{}.tx".format(arm_pole))
            armpole_ty_value = cmds.getAttr("{}.ty".format(arm_pole))
            armpole_tz_value = cmds.getAttr("{}.tz".format(arm_pole))
            
            invarmpole_tx_value = cmds.getAttr("{}.tx".format(inv_arm_pole))
            invarmpole_ty_value = cmds.getAttr("{}.ty".format(inv_arm_pole))
            invarmpole_tz_value = cmds.getAttr("{}.tz".format(inv_arm_pole))
            
            cmds.setAttr("{}.tx".format(arm_pole),invarmpole_tx_value*-1)
            cmds.setAttr("{}.ty".format(arm_pole),invarmpole_ty_value)
            cmds.setAttr("{}.tz".format(arm_pole),invarmpole_tz_value)
            
            cmds.setAttr("{}.tx".format(inv_arm_pole),armpole_tx_value*-1)
            cmds.setAttr("{}.ty".format(inv_arm_pole),armpole_ty_value)
            cmds.setAttr("{}.tz".format(inv_arm_pole),armpole_tz_value)
            
            
            #hip
            
            hip = "{}hipFK_l_ctr_1".format(ref)
            inv_hip = "{}hipFK_r_ctr_1".format(ref)
            
            for axis in "xyz":
                hip_value = cmds.getAttr("{}.r{}".format(hip,axis))
                invhip_value = cmds.getAttr("{}.r{}".format(inv_hip,axis))
                cmds.setAttr("{}.r{}".format(hip,axis),invhip_value)
                cmds.setAttr("{}.r{}".format(inv_hip,axis),hip_value)
            
            #knee
            
            knee = "{}kneeFK_l_ctr_1".format(ref)
            inv_knee = "{}kneeFK_r_ctr_1".format(ref)
            
            for axis in "xyz":
                knee_value = cmds.getAttr("{}.r{}".format(knee,axis))
                invknee_value = cmds.getAttr("{}.r{}".format(inv_knee,axis))
                cmds.setAttr("{}.r{}".format(knee,axis),invknee_value)
                cmds.setAttr("{}.r{}".format(inv_knee,axis),knee_value)
            
            #footFK
            
            foot_fk = "{}footFK_l_ctr_1".format(ref)
            inv_foot_fk = "{}footFK_r_ctr_1".format(ref)
            
            for axis in "xyz":
                footfk_value = cmds.getAttr("{}.r{}".format(foot_fk,axis))
                invfootfk_value = cmds.getAttr("{}.r{}".format(inv_foot_fk,axis))
                cmds.setAttr("{}.r{}".format(foot_fk,axis),invfootfk_value)
                cmds.setAttr("{}.r{}".format(inv_foot_fk,axis),footfk_value)
            
            
            #leg
            
            leg = "{}hip_l_ctr_1".format(ref)
            inv_leg = "{}hip_r_ctr_1".format(ref)
            
            leg_tx_value = cmds.getAttr("{}.tx".format(leg))
            leg_ty_value = cmds.getAttr("{}.ty".format(leg))
            leg_tz_value = cmds.getAttr("{}.tz".format(leg))
            
            invleg_tx_value = cmds.getAttr("{}.tx".format(inv_leg))
            invleg_ty_value = cmds.getAttr("{}.ty".format(inv_leg))
            invleg_tz_value = cmds.getAttr("{}.tz".format(inv_leg))
            
            cmds.setAttr("{}.tx".format(leg),invleg_tx_value)
            cmds.setAttr("{}.ty".format(leg),invleg_ty_value)
            cmds.setAttr("{}.tz".format(leg),invleg_tz_value)
            
            cmds.setAttr("{}.tx".format(inv_leg),leg_tx_value)
            cmds.setAttr("{}.ty".format(inv_leg),leg_ty_value)
            cmds.setAttr("{}.tz".format(inv_leg),leg_tz_value)
        
        else:
            selection_list = cmds.ls(sl=1)
            for sel in selection_list:
                center_ctrls = ['{}base_c_ctr_1'.format(ref),
                            '{}center_c_ctr_1'.format(ref),
                            '{}chest_c_ctr_1'.format(ref),
                            '{}head_c_ctr_1'.format(ref),
                            '{}middleNeck_c_ctr_1'.format(ref),
                            '{}middleSpineIK_c_ctr_1'.format(ref),
                            '{}neck_c_ctr_1'.format(ref),
                            '{}pelvis_c_ctr_1'.format(ref),
                            '{}root_c_ctr_1'.format(ref),
                            '{}spineFK1Inv_c_ctr_1'.format(ref),
                            '{}spineFK1_c_ctr_1'.format(ref),
                            '{}spineFK2Inv_c_ctr_1'.format(ref),
                            '{}spineFK2_c_ctr_1'.format(ref),
                            '{}spineFK3Inv_c_ctr_1'.format(ref),
                            '{}spineFK3_c_ctr_1'.format(ref)] 
            
                center_inv_trans = ["tx","ry","rz"]
                if sel in center_ctrls:
                    for cit in center_inv_trans:
                        ct_value = cmds.getAttr("{}.{}".format(sel,cit))
                        cit_value = ct_value*-1
                        cmds.setAttr("{}.{}".format(sel,cit),cit_value)
        
                #hand FK
                
                hand_fk_list = ["{}handFK_l_ctr_1".format(ref),"{}handFK_r_ctr_1".format(ref)]
                
                if sel in hand_fk_list:
                    hand_fk = "{}handFK_l_ctr_1".format(ref)
                    inv_hand_fk = "{}handFK_r_ctr_1".format(ref)
                    handfk_rx_value = cmds.getAttr("{}.rx".format(hand_fk))
                    handfk_ry_value = cmds.getAttr("{}.ry".format(hand_fk))
                    handfk_rz_value = cmds.getAttr("{}.rz".format(hand_fk))
                    
                    invhandfk_rx_value = cmds.getAttr("{}.rx".format(inv_hand_fk))
                    invhandfk_ry_value = cmds.getAttr("{}.ry".format(inv_hand_fk))
                    invhandfk_rz_value = cmds.getAttr("{}.rz".format(inv_hand_fk))
                    
                    cmds.setAttr("{}.rx".format(hand_fk),invhandfk_rx_value)
                    cmds.setAttr("{}.ry".format(hand_fk),invhandfk_ry_value*-1)
                    cmds.setAttr("{}.rz".format(hand_fk),invhandfk_rz_value*-1)
                    
                    cmds.setAttr("{}.rx".format(inv_hand_fk),handfk_rx_value)
                    cmds.setAttr("{}.ry".format(inv_hand_fk),handfk_ry_value*-1)
                    cmds.setAttr("{}.rz".format(inv_hand_fk),handfk_rz_value*-1)
                
                #elbow FK
                
                elbow_fk_list =[ "{}elbowFK_l_ctr_1".format(ref), "{}elbowFK_r_ctr_1".format(ref)]
                
                if sel in elbow_fk_list:
                    elbow_fk = "{}elbowFK_l_ctr_1".format(ref)
                    inv_elbow_fk = "{}elbowFK_r_ctr_1".format(ref)
                    
                    elbowfk_rx_value = cmds.getAttr("{}.rx".format(elbow_fk))
                    elbowfk_ry_value = cmds.getAttr("{}.ry".format(elbow_fk))
                    elbowfk_rz_value = cmds.getAttr("{}.rz".format(elbow_fk))
                    
                    invelbowfk_rx_value = cmds.getAttr("{}.rx".format(inv_elbow_fk))
                    invelbowfk_ry_value = cmds.getAttr("{}.ry".format(inv_elbow_fk))
                    invelbowfk_rz_value = cmds.getAttr("{}.rz".format(inv_elbow_fk))
                    
                    cmds.setAttr("{}.rx".format(elbow_fk),invelbowfk_rx_value*-1)
                    cmds.setAttr("{}.ry".format(elbow_fk),invelbowfk_ry_value*-1)
                    cmds.setAttr("{}.rz".format(elbow_fk),invelbowfk_rz_value)
                    
                    cmds.setAttr("{}.rx".format(inv_elbow_fk),elbowfk_rx_value*-1)
                    cmds.setAttr("{}.ry".format(inv_elbow_fk),elbowfk_ry_value*-1)
                    cmds.setAttr("{}.rz".format(inv_elbow_fk),elbowfk_rz_value)
                
                #shoulder FK
                
                shoulder_fk_list = ["{}shoulderFK_l_ctr_1".format(ref),"{}shoulderFK_r_ctr_1".format(ref)]
                
                if sel in shoulder_fk_list:
                    shoulder_fk = "{}shoulderFK_l_ctr_1".format(ref)
                    inv_shoulder_fk = "{}shoulderFK_r_ctr_1".format(ref)
                    
                    shoulderfk_rx_value = cmds.getAttr("{}.rx".format(shoulder_fk))
                    shoulderfk_ry_value = cmds.getAttr("{}.ry".format(shoulder_fk))
                    shoulderfk_rz_value = cmds.getAttr("{}.rz".format(shoulder_fk))
                    
                    invshoulderfk_rx_value = cmds.getAttr("{}.rx".format(inv_shoulder_fk))
                    invshoulderfk_ry_value = cmds.getAttr("{}.ry".format(inv_shoulder_fk))
                    invshoulderfk_rz_value = cmds.getAttr("{}.rz".format(inv_shoulder_fk))
                    
                    cmds.setAttr("{}.rx".format(shoulder_fk),invshoulderfk_rx_value*-1)
                    cmds.setAttr("{}.ry".format(shoulder_fk),invshoulderfk_ry_value*-1)
                    cmds.setAttr("{}.rz".format(shoulder_fk),invshoulderfk_rz_value)
                    
                    cmds.setAttr("{}.rx".format(inv_shoulder_fk),shoulderfk_rx_value*-1)
                    cmds.setAttr("{}.ry".format(inv_shoulder_fk),shoulderfk_ry_value*-1)
                    cmds.setAttr("{}.rz".format(inv_shoulder_fk),shoulderfk_rz_value)
                    
                    shoulderfk_chest_value = cmds.getAttr("{}.chestSpace".format(shoulder_fk))
                    invshoulderfk_chest_value = cmds.getAttr("{}.chestSpace".format(inv_shoulder_fk))
                    cmds.setAttr("{}.chestSpace".format(shoulder_fk),invshoulderfk_chest_value)
                    cmds.setAttr("{}.chestSpace".format(inv_shoulder_fk),shoulderfk_chest_value)
                    
                #clavicle
                
                clavicle_list = ["{}clavicle_l_ctr_1".format(ref),"{}clavicle_r_ctr_1".format(ref)]
                if sel in clavicle_list:
                    clavicle = "{}clavicle_l_ctr_1".format(ref)
                    inv_clavicle = "{}clavicle_r_ctr_1".format(ref)
                    
                    for trans in "rt":
                        for axis in "xyz":
                            clavicle_value = cmds.getAttr("{}.{}{}".format(clavicle,trans,axis))
                            invclavicle_value = cmds.getAttr("{}.{}{}".format(inv_clavicle,trans,axis))
                            cmds.setAttr("{}.{}{}".format(clavicle,trans,axis),invclavicle_value)
                            cmds.setAttr("{}.{}{}".format(inv_clavicle,trans,axis),clavicle_value)        
                    
                    
                #footik        
                foot_ik_list = ["{}footIK_l_ctr_1".format(ref),"{}footIK_r_ctr_1".format(ref)]
                if sel in foot_ik_list:
                    foot_ik = "{}footIK_l_ctr_1".format(ref)
                    inv_foot_ik = "{}footIK_r_ctr_1".format(ref)
                    
                    footik_rx_value = cmds.getAttr("{}.rx".format(foot_ik))
                    footik_ry_value = cmds.getAttr("{}.ry".format(foot_ik))
                    footik_rz_value = cmds.getAttr("{}.rz".format(foot_ik))
                    footik_tx_value = cmds.getAttr("{}.tx".format(foot_ik))
                    footik_ty_value = cmds.getAttr("{}.ty".format(foot_ik))
                    footik_tz_value = cmds.getAttr("{}.tz".format(foot_ik))
                    
                    invfootik_rx_value = cmds.getAttr("{}.rx".format(inv_foot_ik))
                    invfootik_ry_value = cmds.getAttr("{}.ry".format(inv_foot_ik))
                    invfootik_rz_value = cmds.getAttr("{}.rz".format(inv_foot_ik))
                    invfootik_tx_value = cmds.getAttr("{}.tx".format(inv_foot_ik))
                    invfootik_ty_value = cmds.getAttr("{}.ty".format(inv_foot_ik))
                    invfootik_tz_value = cmds.getAttr("{}.tz".format(inv_foot_ik))
                    
                    
                    cmds.setAttr("{}.rx".format(foot_ik),invfootik_rx_value)
                    cmds.setAttr("{}.ry".format(foot_ik),invfootik_ry_value*-1)
                    cmds.setAttr("{}.rz".format(foot_ik),invfootik_rz_value*-1)
                    cmds.setAttr("{}.tx".format(foot_ik),invfootik_tx_value*-1)
                    cmds.setAttr("{}.ty".format(foot_ik),invfootik_ty_value)
                    cmds.setAttr("{}.tz".format(foot_ik),invfootik_tz_value)
                    
                    cmds.setAttr("{}.rx".format(inv_foot_ik),footik_rx_value)
                    cmds.setAttr("{}.ry".format(inv_foot_ik),footik_ry_value*-1)
                    cmds.setAttr("{}.rz".format(inv_foot_ik),footik_rz_value*-1)
                    cmds.setAttr("{}.tx".format(inv_foot_ik),footik_tx_value*-1)
                    cmds.setAttr("{}.ty".format(inv_foot_ik),footik_ty_value)
                    cmds.setAttr("{}.tz".format(inv_foot_ik),footik_tz_value)
                    
                    
                    roll_attr = ["knee","autoStretch","footRoll","toeBreak","releaseAngle","footTilt","toeRoll","toeSlide","heelRoll","ballRoll"]
                    
                    for r_attr in roll_attr:
                        footik_roll_value = cmds.getAttr("{}.{}".format(foot_ik,r_attr))
                        invfootik_roll_value = cmds.getAttr("{}.{}".format(inv_foot_ik,r_attr))
                        cmds.setAttr("{}.{}".format(foot_ik,r_attr),invfootik_roll_value)
                        cmds.setAttr("{}.{}".format(inv_foot_ik,r_attr),footik_roll_value)
                        
                    
                #toe
                toe_list = ["{}toe_l_ctr_1".format(ref),"{}toe_r_ctr_1".format(ref)]
                if sel in toe_list:
                    toe = "{}toe_l_ctr_1".format(ref)
                    inv_toe = "{}toe_r_ctr_1".format(ref)
                    
                    toe_rx_value = cmds.getAttr("{}.rx".format(toe))
                    toe_ry_value = cmds.getAttr("{}.ry".format(toe))
                    toe_rz_value = cmds.getAttr("{}.rz".format(toe))
                    
                    invtoe_rx_value = cmds.getAttr("{}.rx".format(inv_toe))
                    invtoe_ry_value = cmds.getAttr("{}.ry".format(inv_toe))
                    invtoe_rz_value = cmds.getAttr("{}.rz".format(inv_toe))
                    
                    cmds.setAttr("{}.rx".format(toe),invtoe_rx_value)
                    cmds.setAttr("{}.ry".format(toe),invtoe_ry_value*-1)
                    cmds.setAttr("{}.rz".format(toe),invtoe_rz_value*-1)
                    
                    cmds.setAttr("{}.rx".format(inv_toe),toe_rx_value)
                    cmds.setAttr("{}.ry".format(inv_toe),toe_ry_value*-1)
                    cmds.setAttr("{}.rz".format(inv_toe),toe_rz_value*-1)            
                        
                            
                #legPole
                
                leg_pole_list = ["{}legPole_l_ctr_1".format(ref),"{}legPole_r_ctr_1".format(ref)]
                if sel in leg_pole_list:   
                    leg_pole = "{}legPole_l_ctr_1".format(ref)
                    inv_leg_pole = "{}legPole_r_ctr_1".format(ref)
                    
                    legpole_tx_value = cmds.getAttr("{}.tx".format(leg_pole))
                    legpole_ty_value = cmds.getAttr("{}.ty".format(leg_pole))
                    legpole_tz_value = cmds.getAttr("{}.tz".format(leg_pole))
                    
                    invlegpole_tx_value = cmds.getAttr("{}.tx".format(inv_leg_pole))
                    invlegpole_ty_value = cmds.getAttr("{}.ty".format(inv_leg_pole))
                    invlegpole_tz_value = cmds.getAttr("{}.tz".format(inv_leg_pole))
                    
                    cmds.setAttr("{}.tx".format(leg_pole),invlegpole_tx_value*-1)
                    cmds.setAttr("{}.ty".format(leg_pole),invlegpole_ty_value)
                    cmds.setAttr("{}.tz".format(leg_pole),invlegpole_tz_value)
                    
                    cmds.setAttr("{}.tx".format(inv_leg_pole),legpole_tx_value*-1)
                    cmds.setAttr("{}.ty".format(inv_leg_pole),legpole_ty_value)
                    cmds.setAttr("{}.tz".format(inv_leg_pole),legpole_tz_value)            
                            
                        
                #handIK
                
                hand_ik_list = ["{}handIK_l_ctr_1".format(ref),"{}handIK_r_ctr_1".format(ref)]
                if sel in hand_ik_list:
                    hand_ik = "{}handIK_l_ctr_1".format(ref)
                    inv_hand_ik = "{}handIK_r_ctr_1".format(ref)
                    
                    handik_rx_value = cmds.getAttr("{}.rx".format(hand_ik))
                    handik_ry_value = cmds.getAttr("{}.ry".format(hand_ik))
                    handik_rz_value = cmds.getAttr("{}.rz".format(hand_ik))
                    handik_tx_value = cmds.getAttr("{}.tx".format(hand_ik))
                    handik_ty_value = cmds.getAttr("{}.ty".format(hand_ik))
                    handik_tz_value = cmds.getAttr("{}.tz".format(hand_ik))
                    
                    invhandik_rx_value = cmds.getAttr("{}.rx".format(inv_hand_ik))
                    invhandik_ry_value = cmds.getAttr("{}.ry".format(inv_hand_ik))
                    invhandik_rz_value = cmds.getAttr("{}.rz".format(inv_hand_ik))
                    invhandik_tx_value = cmds.getAttr("{}.tx".format(inv_hand_ik))
                    invhandik_ty_value = cmds.getAttr("{}.ty".format(inv_hand_ik))
                    invhandik_tz_value = cmds.getAttr("{}.tz".format(inv_hand_ik))
                    
                    
                    
                    cmds.setAttr("{}.rx".format(hand_ik),invhandik_rx_value)
                    cmds.setAttr("{}.ry".format(hand_ik),invhandik_ry_value*-1)
                    cmds.setAttr("{}.rz".format(hand_ik),invhandik_rz_value*-1)
                    cmds.setAttr("{}.tx".format(hand_ik),invhandik_tx_value*-1)
                    cmds.setAttr("{}.ty".format(hand_ik),invhandik_ty_value)
                    cmds.setAttr("{}.tz".format(hand_ik),invhandik_tz_value)
                    
                    
                    cmds.setAttr("{}.rx".format(inv_hand_ik),handik_rx_value)
                    cmds.setAttr("{}.ry".format(inv_hand_ik),handik_ry_value*-1)
                    cmds.setAttr("{}.rz".format(inv_hand_ik),handik_rz_value*-1)
                    cmds.setAttr("{}.tx".format(inv_hand_ik),handik_tx_value*-1)
                    cmds.setAttr("{}.ty".format(inv_hand_ik),handik_ty_value)
                    cmds.setAttr("{}.tz".format(inv_hand_ik),handik_tz_value)                
                    
                    
                #armPole
                
                arm_pole_list = ["{}armPole_l_ctr_1".format(ref),"{}armPole_r_ctr_1".format(ref)]
                if sel in arm_pole_list:
                    arm_pole = "{}armPole_l_ctr_1".format(ref)
                    inv_arm_pole = "{}armPole_r_ctr_1".format(ref)
                    
                    armpole_tx_value = cmds.getAttr("{}.tx".format(arm_pole))
                    armpole_ty_value = cmds.getAttr("{}.ty".format(arm_pole))
                    armpole_tz_value = cmds.getAttr("{}.tz".format(arm_pole))
                    
                    invarmpole_tx_value = cmds.getAttr("{}.tx".format(inv_arm_pole))
                    invarmpole_ty_value = cmds.getAttr("{}.ty".format(inv_arm_pole))
                    invarmpole_tz_value = cmds.getAttr("{}.tz".format(inv_arm_pole))
                    
                    cmds.setAttr("{}.tx".format(arm_pole),invarmpole_tx_value*-1)
                    cmds.setAttr("{}.ty".format(arm_pole),invarmpole_ty_value)
                    cmds.setAttr("{}.tz".format(arm_pole),invarmpole_tz_value)
                    
                    cmds.setAttr("{}.tx".format(inv_arm_pole),armpole_tx_value*-1)
                    cmds.setAttr("{}.ty".format(inv_arm_pole),armpole_ty_value)
                    cmds.setAttr("{}.tz".format(inv_arm_pole),armpole_tz_value)            
                            
                #hip
                
                hip_list = ["{}hipFK_l_ctr_1".format(ref),"{}hipFK_r_ctr_1".format(ref)]
                if sel in hip_list:
                    hip = "{}hipFK_l_ctr_1".format(ref)
                    inv_hip = "{}hipFK_r_ctr_1".format(ref)
                    
                    for axis in "xyz":
                        hip_value = cmds.getAttr("{}.r{}".format(hip,axis))
                        invhip_value = cmds.getAttr("{}.r{}".format(inv_hip,axis))
                        cmds.setAttr("{}.r{}".format(hip,axis),invhip_value)
                        cmds.setAttr("{}.r{}".format(inv_hip,axis),hip_value)       
                    
                #knee
                
                knee_list = ["{}kneeFK_l_ctr_1".format(ref),"{}kneeFK_r_ctr_1".format(ref)]
                if sel in knee_list:
                    knee = "{}kneeFK_l_ctr_1".format(ref)
                    inv_knee = "{}kneeFK_r_ctr_1".format(ref)
                    
                    for axis in "xyz":
                        knee_value = cmds.getAttr("{}.r{}".format(knee,axis))
                        invknee_value = cmds.getAttr("{}.r{}".format(inv_knee,axis))
                        cmds.setAttr("{}.r{}".format(knee,axis),invknee_value)
                        cmds.setAttr("{}.r{}".format(inv_knee,axis),knee_value)            
                   
                #footFK
                
                foot_fk_list =["{}footFK_l_ctr_1".format(ref),"{}footFK_r_ctr_1".format(ref)]
                if sel in foot_fk_list:
                    foot_fk = "{}footFK_l_ctr_1".format(ref)
                    inv_foot_fk = "{}footFK_r_ctr_1".format(ref)
                    
                    for axis in "xyz":
                        footfk_value = cmds.getAttr("{}.r{}".format(foot_fk,axis))
                        invfootfk_value = cmds.getAttr("{}.r{}".format(inv_foot_fk,axis))
                        cmds.setAttr("{}.r{}".format(foot_fk,axis),invfootfk_value)
                        cmds.setAttr("{}.r{}".format(inv_foot_fk,axis),footfk_value)    
                    
                    
                #leg
                
                leg_list = ["{}hip_l_ctr_1".format(ref),"{}hip_r_ctr_1".format(ref)]
                if sel in leg_list:
                    leg = "{}hip_l_ctr_1".format(ref)
                    inv_leg = "{}hip_r_ctr_1".format(ref)
                    
                    leg_tx_value = cmds.getAttr("{}.tx".format(leg))
                    leg_ty_value = cmds.getAttr("{}.ty".format(leg))
                    leg_tz_value = cmds.getAttr("{}.tz".format(leg))
                    
                    invleg_tx_value = cmds.getAttr("{}.tx".format(inv_leg))
                    invleg_ty_value = cmds.getAttr("{}.ty".format(inv_leg))
                    invleg_tz_value = cmds.getAttr("{}.tz".format(inv_leg))
                    
                    cmds.setAttr("{}.tx".format(leg),invleg_tx_value)
                    cmds.setAttr("{}.ty".format(leg),invleg_ty_value)
                    cmds.setAttr("{}.tz".format(leg),invleg_tz_value)
                    
                    cmds.setAttr("{}.tx".format(inv_leg),leg_tx_value)
                    cmds.setAttr("{}.ty".format(inv_leg),leg_ty_value)
                    cmds.setAttr("{}.tz".format(inv_leg),leg_tz_value)        
            
    win.flippose_buton.clicked.connect(flipPose)
    win.restpose_buton.clicked.connect(restPose)
    cmds.select(cl=1)
