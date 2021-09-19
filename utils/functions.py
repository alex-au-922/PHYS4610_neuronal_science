import numpy as np
import enum

class Constants:
    '''Class of constants useful in the project'''
    synapticMatrixPath = 'utils/DIV66_BMI0_g.txt'
    numberOfNodes = 4095

class Node(enum.Enum):
    '''Nodes of EXCITED, INHIBIT and UNCLEAR type in categorical data types.'''
    EXCITED = 1
    INHIBIT = -1
    UNCLEAR = 0

class Functions:
    '''Storing all the functions and'''
    def __init__(self):
        self.v = np.zeros(Constants.numberOfNodes + 1, dtype = np.float64)
        self.u = np.zeros(Constants.numberOfNodes + 1, dtype = np.float64)
        self.nodeType = np.zeros(Constants.numberOfNodes + 1, dtype = np.int8)
        self.durationOfSpike = None
        self. 

    def randomGaussian(self):
        return np.random.standard_normal(1)

if __name__ == "__main__":
    obj = Functions()
    print(obj.randomGaussian())