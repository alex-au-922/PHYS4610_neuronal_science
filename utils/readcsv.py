import pandas as pd
import numpy as np
import os

# Testing for commit

class ReadCSV:
    def __init__(self, path):
        self.connectionMatrix = pd.read_csv(path, sep = '\t', header = None).values
        self.startAtOne()

    def startAtOne(self) -> np.ndarray:
        height, width = self.connectionMatrix.shape
        bufferMatrix = np.zeros((width + 1, height + 1), dtype = np.float64)
        for i, row in enumerate(self.connectionMatrix):
            for j, value in enumerate(row):
                bufferMatrix[i + 1][j + 1] = value
        self.connectionMatrix = bufferMatrix

    def non_zero_count(self):
        return np.count_nonzero(self.connectionMatrix)
        
    def size(self):
        return self.connectionMatrix.size
    
    @property
    def values(self):
        return self.connectionMatrix


if __name__ == "__main__":
    data = ReadCSV()
    print(data.values)
    print(data.non_zero_count())
    print(data.size())
