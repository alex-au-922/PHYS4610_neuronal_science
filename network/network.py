from yaml import loader
from .node import *
import yaml
import sys
import utils.functions
import numpy as np

class NeuronNetwork:
    def __init__(self, w_matrix):
        self.w_matrix = w_matrix
        self.N = len(w_matrix) - 1
        self.arg = {}
        with open('constants.yaml') as stream:
            self.arg.update(yaml.load(stream, Loader=yaml.SafeLoader)['NeuronNetwork'])
        
        utils.functions.random_seed(self.arg['seed'])
        self.u_arr = utils.functions.random_vec(self.N, self.arg['initLowBound'], self.arg['initUpBound'])
        self.v_arr = utils.functions.random_vec(self.N, self.arg['initLowBound'], self.arg['initUpBound'])
        self.node_list = []
        self.node_map = {}
        # self.initialize_from_adj_matrix()
    
    def check_node_type(self,w_matrix):
        '''Check whether the node type is consistent'''
        for column in w_matrix.T:
            assert all(column >= 0) or all(column <= 0)   

    def initialize_from_adj_matrix(self):
        (i_max, j_max) = self.w_matrix.shape
        for i in range(1, i_max):
            self._create_node(i)
            for j in range(1, j_max):
                self._create_node(j)
                w_ij = self.w_matrix[i][j]
                if (w_ij != 0):
                    self.node_map[j].direct_to(self.node_map[i], w_ij)

    def _create_node(self, n):
        '''Create Node n if not exists'''
        if n not in self.node_map:
            # Check if Node n is Excitor or Inhibitor
            if any(self.w_matrix[i][n] > 0 for i in range(1, len(self.w_matrix))):
                self.node_map[n] = ExciNeuron(self.init_u_arr[n], self.v_arr[n])
            if any(self.w_matrix[i][n] < 0 for i in range(1, len(self.w_matrix))):
                self.node_map[n] = InhiNeuron(self.init_u_arr[n], self.v_arr[n])
            self.node_list.append(self.node_map[n])
                    
class NeuronNetworkTimeSeries(NeuronNetwork):


    def __init__(self, w_matrix, *args, **kwargs):
        super().__init__(w_matrix = w_matrix, *args, **kwargs)
        self.time = 0
        with open('constants.yaml') as stream:
            self.arg.update(yaml.load(stream)['NeuronNetworkTimeSeries'])
        print(self.arg)

        
    # def v_step(self) -> np.ndarray:
    #     noise_arr = np.ones_like(self.v_arr) * noise 
    #     v_vec_delta = (self.arg['c1']*self.v_arr**2 + self.arg['c2'] * self.v_arr \
    #          + self.arg['c3'] - self.arg['c4'] * self.u_vec+ self.arg['c5']*self.I_vec + )*time_step 
    #     v_vec += v_vec_delta

    # def u_step(v_vec: np.ndarray, u_vec:np.ndarray, args):

if __name__ == "__main__":
    obj = NeuronNetworkTimeSeries()


    def u_step(v_vec: np.ndarray, u_vec:np.ndarray, args):
        pass

    def step(self):
        # some functions
        self.time += self.arg["dt"]

    
    def output(self):
        pass







    