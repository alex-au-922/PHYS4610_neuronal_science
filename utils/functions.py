import numpy as np
import pandas as pd
import os

def random_seed(seed: int) -> None:
    np.random.seed(seed)

def random_vec(numberOfNodes: int, lowBound:float, upBound: float) -> np.ndarray:
    return np.random.random(numberOfNodes)*(upBound - lowBound) + lowBound

def read_init_txt(filePath):
    return pd.read_csv(filePath, sep='\t', header = None).iloc[0].values


def random_v_vec(numberOfNodes = None, lowBound = None, upBound = None, filePath = None) -> np.ndarray:
    if os.environ.get('DEBUG'):
        return read_init_txt(filePath)
    else:
        return random_vec(numberOfNodes, lowBound, upBound)

def random_u_vec(numberOfNodes = None, lowBound = None, upBound = None, filePath = None) -> np.ndarray:
    if os.environ.get('DEBUG'):
        return read_init_txt(filePath)
    else:
        return random_vec(numberOfNodes, lowBound, upBound)

def random_gaussian(sigma, size = 1):
    return np.random.normal(scale = sigma, size = size)

def removeFiles(filename):
    if os.path.exists(filename):
        os.remove(filename)

if __name__ == "__main__":
    print(random_gaussian(1))