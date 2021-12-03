
# Construir el rig y aplicar este script [BIPEDO NORMAL]
controles =[u'base_c_ctr_0', u'center_c_ctr_0', u'pelvis_c_ctr_0', u'root_c_ctr_0', u'spineFK1_c_ctr_0', u'spineFK2_c_ctr_0', u'spineFK3_c_ctr_0', u'middleSpineIK_c_ctr_0', u'chest_c_ctr_0', u'spineFK1Inv_c_ctr_0', u'spineFK2Inv_c_ctr_0', u'spineFK3Inv_c_ctr_0', u'neck_c_ctr_0', u'head_c_ctr_0', u'middleNeck_c_ctr_0', u'clavicle_l_ctr_0', u'clavicle_r_ctr_0', u'armPole_l_ctr_0', u'handFK_l_ctr_0', u'elbowFK_l_ctr_0', u'shoulderFK_l_ctr_0', u'handIK_l_ctr_0', u'forearmBend_l_ctr_0', u'elbowBend_l_ctr_0', u'uparmBend_l_ctr_0', u'armSettings_l_ctr_0', u'handFK_r_ctr_0', u'armSettings_r_ctr_0', u'lowlegBend_l_ctr_0', u'kneeBend_l_ctr_0', u'uplegBend_l_ctr_0', u'footFK_l_ctr_0', u'kneeFK_l_ctr_0', u'legSettings_l_ctr_0', u'hipFK_l_ctr_0', u'legPole_l_ctr_0', u'footIK_l_ctr_0', u'toe_l_ctr_0', u'hip_l_ctr_0', u'uplegBend_r_ctr_0', u'kneeBend_r_ctr_0', u'lowlegBend_r_ctr_0', u'legPole_r_ctr_0', u'legSettings_r_ctr_0', u'footIK_r_ctr_0', u'kneeFK_r_ctr_0', u'hipFK_r_ctr_0', u'toe_r_ctr_0', u'footFK_r_ctr_0', u'hip_r_ctr_0', u'handIK_r_ctr_0', u'armPole_r_ctr_0', u'forearmBend_r_ctr_0', u'elbowBend_r_ctr_0', u'uparmBend_r_ctr_0', u'elbowFK_r_ctr_0', u'shoulderFK_r_ctr_0']

for x in controles:
    controles_sucios = x.replace("_0","_1")
    controles_sucios_pos = cmds.xform(controles_sucios,q=True,matrix=True,ws=True)
    cmds.xform(x,matrix=controles_sucios_pos,ws=True)
    