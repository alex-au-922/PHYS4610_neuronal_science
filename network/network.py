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
        self.I_arr = np.zeros(self.N + 1)
        self.u_arr = utils.functions.random_vec(self.N + 1, self.arg['initLowBound'], self.arg['initUpBound'])
        self.v_arr = utils.functions.random_vec(self.N + 1, self.arg['initLowBound'], self.arg['initUpBound'])
        self.G_exc_arr = np.zeros(self.N + 1)
        self.G_inh_arr = np.zeros(self.N + 1)

        self.t_spike = [None]*(self.N + 1)
        for i in range(len(self.t_spike)):
            self.t_spike[i] = np.zeros(self.arg['maxSpike'])
            for j in range(self.arg['maxSpike']):
                self.t_spike[i][j] = np.inf
        self.t_spike = np.array(self.t_spike)

        self.t_spike_indices = [0]*(self.N + 1)

        # self.node_map[n].neuron_type == NodeType.EXCITED

        self.node_list = []
        #self.node_map = {}
        # node_type_map[n] = 1 => node_n is Excitor
        # node_type_map[n] = -1 => node_n is Inhibitor
        self.node_type_map = {}
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
                    self.node_type_map[j] = 1
                    if i not in self.exc_node_map:
                        self.exc_node_map[i] = [j]
                    else:
                        self.exc_node_map[i].append(j)
                if (w_ij < 0):
                    self.node_type_map[j] = -1
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
        a_Exc = self.arg["EXCITED"]["a"]
        a_Inh = self.arg["INHIBIT"]["a"]
        b_Exc = self.arg["EXCITED"]["b"]
        b_Inh = self.arg["INHIBIT"]["b"]
        a = [a_Exc if (self.node_type_map[n] == 1) else a_Inh if (self.node_type_map[n] == -1) else 0 for n in range(self.N + 1) ]
        b = [b_Exc if (self.node_type_map[n] == 1) else b_Inh if (self.node_type_map[n] == -1) else 0 for n in range(self.N + 1) ]
        return a * (b * self.v_arr - self.u_arr)

    def I_step(self):
        return self.G_exc_arr*(self.arg['ve'] - self.v_arr) - (self.G_inh_arr*(self.v_arr - self.arg['vI']))

    def G_Exc_step(self):
        # Loop for all keys
        for i, j_list in self.exc_node_map.items():
            new_matrix = self.t_spike[j_list][:, :max(self.t_spike_indices)]
            gamma_j = np.sum(np.exp(-1*np.abs(self.time - new_matrix)/self.arg['tauExc']), axis = 1)
            weight = self.w_matrix[:, i][j_list]
            self.G_exc_arr[i] = self.arg['beta']*np.matmul(weight, gamma_j)


    def G_Inh_step(self):
        for i, j_list in self.inh_node_map.items():
            new_matrix = self.t_spike[j_list][:, :max(self.t_spike_indices)]
            gamma_j = np.sum(np.exp(-1*np.abs(self.time - new_matrix)/self.arg['tauInh']), axis = 1)
            weight = np.abs(self.w_matrix[:, i][j_list])
            self.G_inh_arr[i] = self.arg['beta']*np.matmul(weight, gamma_j)

    def step(self):
        
        # Calcutaion
        new_v = self.v_step
        new_u = self.u_step
        new_I = self.I_step
        new_G_Exc = self.G_Exc_step
        new_G_Inh = self.G_Inh_step
        # Replace

        pass



if __name__ == "__main__":
    obj = NeuronNetworkTimeSeries()









    