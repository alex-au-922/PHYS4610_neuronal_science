import pandas as pd
import numpy as np
import os

PATH = os.path.abspath('DIV66_BMI0_g.txt')

class ReadCSV:
    def __init__(self):
        self.connectionMatrix = pd.read_csv(PATH, sep = '\t', header = None).values
        self.startAtOne()

    def startAtOne(self) -> np.ndarray:
        height, width = self.connectionMatrix.shape
        bufferMatrix = np.zeros((width + 1, height + 1), dtype = np.float64)
        for i, row in enumerate(self.connectionMatrix):
            for j, value in enumerate(row):
                bufferMatrix[i + 1][j + 1] = value
        self.connectionMatrix = bufferMatrix
    
    @property
    def values(self):
        return self.connectionMatrix


if __name__ == "__main__":
    data = ReadCSV()
    print(data.values)
