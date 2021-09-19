import numpy as np

def random_seed(seed: int) -> None:
    np.random.seed(seed)

def random_vec(numberOfNodes: int, lowbound: float, upbound: float) -> np.ndarray:
    return np.random.random(numberOfNodes)*(upbound - lowbound) + lowbound

def v_step(v_vec: np.ndarray, I_vec: np.ndarray, time_step: float) -> np.ndarray:
    assert v_vec.shape[0] == I_vec.shape[0]