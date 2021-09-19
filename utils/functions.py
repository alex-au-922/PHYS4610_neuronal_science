import numpy as np
from numpy.core.fromnumeric import searchsorted
from network.node import NodeType

class NeuronNetworkTimeSeries:
    def __init__(self, seed, numberOfNodes):
        self.numberOfNodes = 4095
        self.seed = seed
        self.v_vec = np.zeros(self.numberOfNodes + 1)
        self.u_vec = np.zeros(self.numberOfNodes + 1)
        
    def random_seed(self, seed: int) -> None:
        np.random.seed(seed)

    def random_vec(numberOfNodes: int, lowbound: float, upbound: float) -> np.ndarray:
        self.v_vec = np.random.random(numberOfNodes)*(upbound - lowbound) + lowbound

    def v_step(v_vec: np.ndarray, u_vec: np.ndarray, I_vec: np.ndarray, time_step: float, args) -> np.ndarray:
        assert v_vec.shape[0] == I_vec.shape[0] 
        assert v_vec.shape[0] == u_vec.shape[0]
        v_vec_delta = (args.c1 * v_vec**2 + args.c2 * v_vec + args.c3 - args.c4 * u_vec + I_vec)*time_step 
        v_vec += v_vec_delta

    def u_step(v_vec: np.ndarray, u_vec:np.ndarray, args):
