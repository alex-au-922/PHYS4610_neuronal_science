import numpy as np
import os

def random_seed(seed: int) -> None:
    np.random.seed(seed)

def random_vec(numberOfNodes: int, lowBound:float, upBound: float) -> np.ndarray:
    return np.random.random(numberOfNodes)*(upBound - lowBound) + lowBound

def random_gaussian(sigma, size = 1):
    return np.random.normal(scale = sigma, size = size)

def removeFiles(filename):
    if os.path.exists(filename):
        os.remove(filename)

if __name__ == "__main__":
    print(random_gaussian(1))