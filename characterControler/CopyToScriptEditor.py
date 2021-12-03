import sys
import os  
sistemaop = sys.platform

windows = ["win32", "win64"]
mac = "darwin"
homedir = os.path.expanduser("~")

for win in windows:
	if sistemaop == win:
		homedir_win = "{}/maya/scripts/characterControler".format(homedir)
		sys.path.append(homedir_win)
		import switch_fk_ik as stch

		
if sistemaop == mac:
	homedir_mac = "{}/Documents/maya/characterControler".format(homedir)
	sys.path.append(homedir_mac)
	import switch_fk_ik as stch
ref = ""
stch.SwitchFunction()
