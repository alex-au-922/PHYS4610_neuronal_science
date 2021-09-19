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
        self.I_arr = None
        self.G_exc_arr = np.zeros(self.N + 1)
        self.G_inh_arr = np.zeros(self.N + 1)

        self.t_spike = np.zeros(self.N+1)
        for i in self.t_spike.shape[0]:
            self.t_spike[i] = np.zeros(0)

        # self.node_map[n].neuron_type == NodeType.EXCITED

        self.node_list = []
        #self.node_map = {}
        self.exc_node_map = {}
        self.inh_node_map = {}
    
        self.initialize_from_adj_matrix()
    
    def check_node_type(self,w_matrix):
        '''Check whether the node type is consistent'''
        for column in w_matrix.T:
            assert all(column >= 0) or all(column <= 0)   

    def initialize_from_adj_matrix(self):
        (i_max, j_max) = self.w_matrix.shape
        for i in range(1, i_max):
            for j in range(1, j_max):
                w_ij = self.w_matrix[i][j]
                if (w_ij > 0):
                    if i not in self.exc_node_map:
                        self.exc_node_map[i] = [j]
                    else:
                        self.exc_node_map[i].append(j)
                if (w_ij < 0):
                    if i not in self.inh_node_map:
                        self.inh_node_map[i] = [j]
                    else:
                        self.inh_node_map[i].append(j)
                    
class NeuronNetworkTimeSeries(NeuronNetwork):
    def __init__(self, w_matrix):
        super().__init__(w_matrix = w_matrix)
        with open('constants.yaml') as stream:
            self.arg.update(yaml.load(stream)['NeuronNetworkTimeSeries'])
        
    def v_step(self):
        noise_arr = np.ones_like(self.v_arr) * \
            utils.functions.random_gaussian(self.arg['sigma'])*np.sqrt(self.arg['dt'])
        
        return self.v_arr +(self.arg['c1']*self.v_arr**2 + self.arg['c2'] * self.v_arr \
             + self.arg['c3'] - self.arg['c4'] * self.u_arr+ self.arg['c5']*self.I_arr+ noise_arr)*self.arg['dt'] 

    def u_step(self):
        pass

    def I_step(self):
        pass

    def G_Exc_step(self):
        # Loop for all keys
        buff_dict = {}
        for key, key_list in self.exc_node_map.items():
            if key not in buff_dict:
                weight_matrix = self.w_matrix[key][key_list]
                inner_matrix = self.t_spike[key_list]

    def G_Inh_step(self):
        pass

    def step(self):
        # Calcutaion

        # Replace

        pass



if __name__ == "__main__":
    obj = NeuronNetworkTimeSeries()









    