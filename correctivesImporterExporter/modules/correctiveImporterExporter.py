#Importador de correctivos 
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
		window_path ="{}/maya/scripts/correctivesImporterExporter/window/correctiveExporterImporterWindow.ui".format(homedir)
		sys.path.append(homedir_win)
		import correctiveImporter as ci
		import correctiveExporter as ce
		import pyside_utils as py
				
if sistemaop == mac:
	homedir_mac = "{}/Documents/maya/correctivesImporterExporter/modules".format(homedir)
	window_path ="{}/Documents/maya/correctivesImporterExporter/window/correctiveExporterImporterWindow.ui".format(homedir)
	sys.path.append(homedir_mac)
	import correctiveImporter as ci
	import correctiveExporter as ce
	import pyside_utils as py

win = py.loadUi(window_path)
win.exportButtom.clicked.connect(ce.CorrectiveExporter)
win.importButtom.clicked.connect(ci.CorrectiveImporter)