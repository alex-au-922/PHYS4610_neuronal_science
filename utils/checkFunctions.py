import os
from gui_utils.guiComponents import showError

def removeFiles(filename):
    if os.path.exists(filename):
        os.remove(filename)

def checkSearchPathConstantFile(basePath, parent):
    if 'result_constants.yaml' not in os.listdir(basePath):
        showError('Error!', 'There is no result_constants.yaml\nfile in the directory!', parent)
        return False
    return True