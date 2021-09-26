import numpy as np

def random_seed(seed: int) -> None:
    np.random.seed(seed)

def random_vec(numberOfNodes: int, lowBound:float, upBound: float) -> np.ndarray:
    return np.random.random(numberOfNodes)*(upBound - lowBound) + lowBound

def random_gaussian(sigma, size):
    return np.random.normal(scale = sigma, size = size)

if __name__ == "__main__":
    print(random_gaussian(1))