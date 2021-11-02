import maya.cmds as cmds
import maya.mel as mel
import sys

# This function can probubly go into a class to allow for ease amount control

def create_Loc():

	# a = print input('set number of locators')
	amount = 6
	for i in range(amount):

		count = i+1

		loc = cmds.spaceLocator (n = 'locator_{}_PRX'.format (count), p = [0,i*2.5,0])
		cmds.makeIdentity (loc, a = 1, t = 1)

		mel.eval ('CenterPivot;')
	cmds.select ('*_PRX')

	lyr = cmds.createDisplayLayer (n = 'locators', num = 1)
	cmds.setAttr ('locators.color', 22)


def create_JNT():

 # Make joints

	# names  = ['C_Pelvis_jnt','l_leg_jnt','l_knee_jnt','l_ankle_jnt','l_toe_jnt','l_foot_ball_jnt'] # Name of joints
	names  = ['C_l_wrist_jnt', 'C_l_elbow_jnt', 'C_l_shoulder_jnt', 'C_l_clav_jnt'] # ['C_l_clav_jnt', 'C_l_shoulder_jnt', 'C_l_elbow_jnt', 'C_l_wrist_jnt']


	sc = 0
	for name in names:

		cmds.select (cl = 1)
		jnt = cmds.joint (n = name , sc = sc )



# Constrain joints to Locators
	Loc = cmds.ls ('*_PRX')

	if Loc:
		con1 = cmds.parentConstraint(Loc[0],names[5])
		con2 = cmds.parentConstraint(Loc[1],names[4])
		con3 = cmds.parentConstraint(Loc[2],names[3])
		con4 = cmds.parentConstraint(Loc[3],names[2])
		con5 = cmds.parentConstraint(Loc[4],names[1])
		con6 = cmds.parentConstraint(Loc[5],names[0])

		cmds.delete(con1,con2,con3,con4,con5,con6) #delete Constraints

	for i, n in enumerate(names):
	    if i ==len(names)-1:
	        continue
	    cmds.parent (names[i+1], n)

	jnt = cmds.select('C_Pelvis_jnt', hi = 1)
	if jnt:
		cmds.makeIdentity (jnt, a = 1, t =1, r = 1, s = 1)

	cmds.mirrorJoint ('l_leg_jnt', mb = True, myz = True, sr = ('l_', 'r_') )

	cmds.select(cl = 1)




# what do i want to code to do 

# I want to create a set of locators for the user to possition 
# I want the user to then be able to create a set of joints based on the locators position 

# what data do we know we know the names of the joints and we know the number of locators we need len()
# class examples = https://github.com/CoreyMSchafer/code_snippets/tree/master/Object-Oriented


def GRP_Higher():

	names1 = ['l_leg_grp','l_sd_ft_roll_r_SDK_grp','l_sd_ft_roll_l_SDK_grp','l_ball_twist_grp','l_pirouette_SDK_grp']
	names2 = ['l_pirouette_grp','l_foot_tap_SDK_grp','l_foot_tap_grp']
	names3 = ['l_heel_lift_SDK_grp','l_heel_lift_grp']
	names4 = ['l_toe_tap_SDK_grp','l_toe_tap_grp']



	names5 = names1 + names2 + names3 + names4


	for name in names5:
		cmds.select (cl = 1)
		GRP = cmds.group (n = name, em = 1, w = 1)

	for i, n in enumerate(names5):
		    if i ==len(names5)-1:
		        continue
		    cmds.parent (names5[i+1], n)

		    if cmds.listRelatives ('l_heel_lift_SDK_grp'):
		    	break

	cmds.parent (names4[1],names4[0])
	cmds.parent (names4[0],names5[7])



	PJnt = cmds.xform ('l_toe_jnt', q = 1, ws = 1, piv = 1) # find jnt position

	# create locators based on joint position for group piv possition

	amount = 3
	for i in range(amount):

		count = i+1

		loc = cmds.spaceLocator (n = 'locator_{}_PIV'.format (count), p = (PJnt[0],PJnt[1],PJnt[2]))
		cmds.makeIdentity (loc, a = 1, t = 1)

		mel.eval ('CenterPivot;')


	# move created locators to possition

	cmds.move (0,0,-3.2, 'locator_1_PIV', a = 1 )
	cmds.move (-1.6,0,0, 'locator_2_PIV', a = 1 )
	cmds.move (1.6,0,0, 'locator_3_PIV', a = 1 )

	# possitioning group pivit

	JPos1 = cmds.xform ('l_toe_jnt', q = 1, ws = 1, piv = 1 )

	cmds.xform (names5[3], names5[8], names5[9], names5[10], names5[11], ws = 1, piv = (JPos1[0], JPos1[1], JPos1[2]))

	JPos2 = cmds.xform ('l_foot_ball_jnt', q = 1, ws = 1, piv = 1 )

	cmds.xform (names5[4], names5[5], ws = 1, piv = (JPos2[0], JPos2[1], JPos2[2]))

	JPos3 = cmds.xform ('l_ankle_jnt', q = 1, ws = 1, piv = 1)

	cmds.xform (names5[0], ws = 1, piv = (JPos3[0], JPos3[1], JPos3[2]))


	loc1 = cmds.xform ('locator_1_PIV', q = 1, ws = 1, piv = 1 )
	cmds.xform ('l_foot_tap_SDK_grp','l_foot_tap_grp', ws = 1, piv = (loc1[0], loc1[1], loc1[2]))

	loc2 = cmds.xform ('locator_2_PIV', q = 1, ws = 1, piv = 1 )
	cmds.xform ('l_sd_ft_roll_r_SDK_grp', ws = 1, piv = (loc2[0], loc2[1], loc2[2]))

	loc3 = cmds.xform ('locator_3_PIV', q = 1, ws = 1, piv = 1 )
	cmds.xform ('l_sd_ft_roll_l_SDK_grp', ws = 1, piv = (loc2[0], loc2[1], loc2[2]))

	cmds.delete ('*_PIV')


	cmds.duplicate ('l_leg_grp', n = 'l_leg_grp'.replace ('l_','r_') )
	cmds.group (n = 'C_CTRL_Grp', em = 1, w = 1)
	cmds.parent ('r_leg_grp', 'C_CTRL_Grp')
	cmds.setAttr ('C_CTRL_Grp.scaleX', -1 )
	cmds.makeIdentity ('C_CTRL_Grp', a = 1, t = 1, s = 1 )
	cmds.parent ('l_leg_grp', 'C_CTRL_Grp')


def Ctrl_Names():

	sel = cmds.ls(sl = 1)
	cmds.rename(sel, '_leg_CTRL')
	cmds.addAttr (ln = 'Heel_Lift', at = 'double',  min = 0, max = 60, dv = 0, k = 1)
	cmds.addAttr (ln = 'Toe_Tap', at = 'double',  min = 0, max = 50, dv = 0, k = 1)
	cmds.addAttr (ln = 'Foot_Tap', at = 'double',  min = 0, max = 40, dv = 0, k = 1)
	cmds.addAttr (ln = 'Ball_Twist', at = 'double',  min = -70, max = 70, dv = 0, k = 1)
	cmds.addAttr (ln = 'Pirouette_U_D', at = 'double',  min = 0, max = 60, dv = 0, k = 1)
	cmds.addAttr (ln = 'Pirouette_L_R', at = 'double',  min = -70, max = 70, dv = 0, k = 1)
	cmds.addAttr (ln = 'Side_Roll', at = 'double',  min = -30, max = 30, dv = 0, k = 1)
	cmds.addAttr (ln = 'PW_Foot_Roll', at = 'double',  min = -30, max = 60, dv = 0, k = 1)
	cmds.addAttr (ln = 'Twist', at = 'double',  min = -30, max = 30, dv = 0, k = 1)













# GitHun guide
# https://guides.github.com/activities/hello-world/



