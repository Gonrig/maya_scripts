from PySide2 import QtUiTools
from PySide2 import QtWidgets
from PySide2 import QtCore
#-------------
# obtener la ventana de maya como Widget de pyside
#-------------
from maya import OpenMayaUI
from shiboken2 import wrapInstance 
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