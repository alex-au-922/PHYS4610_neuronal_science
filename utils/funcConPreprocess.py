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

    def writeCSVFile(self):
        df  = pd.DataFrame(self.Sparse.toarray())
        basePath, fileName = os.path.split(self.path)
        df.to_csv(os.path.join(basePath,'converted_'+fileName), index = None, header = None, sep = '\t')


if __name__ == '__main__':
    obj = FuncToEffConvert('data/DIV66_fncch.txt')

