import os
from gui_utils.guiComponents import showError
from utils.logger import BaseLogger

def checkSearchPathConstantFile(basePath, parent):
    if 'result_constants.yaml' not in os.listdir(basePath):
        showError('Error!', 'There is no result_constants.yaml\nfile in the directory!', parent)
        return False
    return True

def check_node_type(w_matrix):
    '''Check whether the node type is consistent'''
    log = BaseLogger(__name__)
    for i, column in enumerate(w_matrix.T):
        inhi_condition = all(column <=0) and not any (column > 0)
        exci_condition = all(column >= 0) and not any(column < 0)
        if (not inhi_condition) and (not exci_condition):
            logger.exception(f'Error for node {i}: The node cannot be both inhibitory and excitatory!\n{w_matrix[:, i]}')
            raise AssertionError(f'Error for node {i}: The node cannot be both inhibitory and excitatory!\n') 
            