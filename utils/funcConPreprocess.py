import pandas as pd
import numpy as np
from scipy.sparse import lil_matrix
import os

class FuncToEffConvert(object):
    def __init__(self, path):
        self.readFuncCSV(path)
        self.N = 4095
        self.path = path
        self.convertSparseMatrix()
        self.check_node_type_valid()
        self.writeCSVFile()
    
    def readFuncCSV(self, path):
        matrix = pd.read_csv(path, header = None, delimiter = ' ').values
        self.list_i = np.array(matrix[:, 0], dtype = np.int16)
        self.list_j = np.array(matrix[:, 1], dtype = np.int16)
        self.weight_ji = np.array(matrix[:, 2], dtype = np.float64)
    
    def convertSparseMatrix(self):
        self.Sparse = lil_matrix((self.N, self.N))
        for i,j, weight_ji in zip(self.list_i, self.list_j, self.weight_ji):
            self.Sparse[j, i] = weight_ji
    
    def check_node_type_valid(self):
        '''Check whether the node type is consistent'''
        for i, column in enumerate(self.Sparse.toarray().T):
            inhi_condition = all(column <=0) and not any (column > 0)
            exci_condition = all(column >= 0) and not any(column < 0)
            if (not inhi_condition) and (not exci_condition):
                if os.environ.get('FUNC'):
                    # If inhibitory has more nodes
                    if np.sum(column < 0) > np.sum(column > 0):
                        indices = np.where(self.list_i == i)[0]
                        for _, j, weight_ji in zip(self.list_i[indices], self.list_j[indices], self.weight_ji[indices]):
                            self.Sparse[j, _] = -1*np.abs(weight_ji)
                    else:
                        indices = np.where(self.list_i == i)[0]
                        for _, j, weight_ji in zip(self.list_i[indices], self.list_j[indices], self.weight_ji[indices]):
                            self.Sparse[j, _] = np.abs(weight_ji)                        
                else:
                    raise AssertionError(f'Error for node {i}: The node cannot be both inhibitory and excitatory!\n{self.Sparse.toarray()[:, i]}') 

    def writeCSVFile(self):
        df  = pd.DataFrame(self.Sparse.toarray())
        basePath, fileName = os.path.split(self.path)
        df.to_csv(os.path.join(basePath,'converted_'+fileName), index = None, header = None, sep = '\t')


if __name__ == '__main__':
    obj = FuncToEffConvert('data/DIV66_fncch.txt')

