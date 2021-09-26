from numba.np.ufunc import parallel
from .node import *
import yaml
import utils.functions
import numpy as np
import numba as nb
from tqdm import tqdm
import math

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
        # self.t_spike = [None]*(self.N + 1)
        # for i in range(len(self.t_spike)):
        #     self.t_spike[i] = np.zeros(self.arg['maxSpike'])
        #     for j in range(self.arg['maxSpike']):
        #         self.t_spike[i][j] = np.inf
        # self.t_spike = np.array(self.t_spike)
        self.t_spike = [np.zeros(self.arg['maxSpike']) for _ in range(self.N + 1)]
        self.t_spike = np.array(self.t_spike)

        self.t_spike_indices = [0]*(self.N + 1)

        # self.node_map[n].neuron_type == NodeType.EXCITED

        self.node_list = []
        #self.node_map = {}
        # node_type_map[n] = 1 => node_n is Excitor
        # node_type_map[n] = -1 => node_n is Inhibitor
        self.node_type_map = {}
        # Rubbish value
        self.node_type_map[0] = 0
        self.exc_node_map = {}
        self.inh_node_map = {}

        self.exc_matrix = np.zeros_like(self.w_matrix) # all values are 1, 0
        self.inh_matrix = np.zeros_like(self.w_matrix) # all values are 1, 0

        self.exc_w_matrix = np.zeros_like(self.w_matrix)
        self.inh_w_matrix = np.zeros_like(self.w_matrix) # All positive values (absoluted)

        self.weight_map = {}
        self.initialize_from_adj_matrix()

        
            

        self.mat = np.ones(self.arg['maxSpike'])

        a_exc = self.arg["EXCITED"]["a"]
        a_inh = self.arg["INHIBIT"]["a"]
        b_exc = self.arg["EXCITED"]["b"]
        b_inh = self.arg["INHIBIT"]["b"]
        c_exc = self.arg["EXCITED"]["c"]
        c_inh = self.arg["INHIBIT"]["c"]
        d_exc = self.arg["EXCITED"]["d"]
        d_inh = self.arg["INHIBIT"]["d"]
        self.a = [a_exc if (self.node_type_map[n] == 1) else a_inh if (self.node_type_map[n] == -1) else 0 for n in range(self.N + 1) ]
        self.b = [b_exc if (self.node_type_map[n] == 1) else b_inh if (self.node_type_map[n] == -1) else 0 for n in range(self.N + 1) ]
        self.c = [c_exc if (self.node_type_map[n] == 1) else c_inh if (self.node_type_map[n] == -1) else 0 for n in range(self.N + 1) ]
        self.d = [d_exc if (self.node_type_map[n] == 1) else d_inh if (self.node_type_map[n] == -1) else 0 for n in range(self.N + 1) ]
    
    def check_node_type(self,w_matrix):
        '''Check whether the node type is consistent'''
        for column in w_matrix.T:
            assert all(column >= 0) or all(column <= 0)   

    def initialize_from_adj_matrix(self):
        print("Initializing the sparse matrix from adjacency matrix...")
        (i_max, j_max) = self.w_matrix.shape
        for i in tqdm(range(1, i_max)):
            for j in range(1, j_max):
                w_ij = self.w_matrix[i][j]
                '''
                if (w_ij > 0):
                    self.node_type_map[j] = 1
                    if i not in self.exc_node_map:
                        self.exc_node_map[i] = [j]
                    else:
                        self.exc_node_map[i].append(j)
                    continue
                if (w_ij < 0):
                    self.node_type_map[j] = -1
                    if i not in self.inh_node_map:
                        self.inh_node_map[i] = [j]
                    else:
                        self.inh_node_map[i].append(j)
                    continue
                self.node_type_map[j] = 0
                '''
                if (w_ij > 0):
                    self.node_type_map[j] = 1
                    self.exc_matrix[i][j] = 1
                    self.exc_w_matrix[i][j] = w_ij
                    continue
                if (w_ij < 0):
                    self.node_type_map[j] = -1
                    self.inh_matrix[i][j] = 1
                    self.inh_w_matrix[i][j] = abs(w_ij)
                    continue
                self.node_type_map[j] = 0

        
        for i, j_list in self.exc_node_map.items():
            self.weight_map[i] = self.w_matrix[i][j_list]
                    
class NeuronNetworkTimeSeries(NeuronNetwork):
    def __init__(self, w_matrix):
        super().__init__(w_matrix = w_matrix)
        self.time = 0
        self.current_step = 0
        with open('constants.yaml') as stream:
            self.arg.update(yaml.load(stream)['NeuronNetworkTimeSeries'])
        self.exc_decay_factor = np.exp(-1*self.arg['dt'] / self.arg['tauExc'])
        self.inh_decay_factor = np.exp(-1*self.arg['dt'] / self.arg['tauInh'])

        self.exc_exponentials = [math.exp( -(n * self.arg['dt'])/(self.arg['tauExc']) ) for n in range(self.arg['maxSpike'])]
        self.inh_exponentials = [math.exp( -(n * self.arg['dt'])/(self.arg['tauInh']) ) for n in range(self.arg['maxSpike'])]
    
    def v_step(self):
        noise_arr = np.ones_like(self.v_arr) * \
            utils.functions.random_gaussian(self.arg['sigma'])*np.sqrt(self.arg['dt'])
        try:
            buff_v_arr = self.v_arr +(self.arg['c1']*self.v_arr**2 + self.arg['c2'] * self.v_arr \
             + self.arg['c3'] - self.arg['c4'] * self.u_arr+ self.arg['c5']*self.I_arr+ noise_arr)*self.arg['dt'] 
            return buff_v_arr
        except OverflowError as e:
            with open("log.txt", 'a') as file:
                file.write(f'{e}\n')
                file.write(f'{buff_v_arr}\n')
            return buff_v_arr

    def u_step(self):
        try:
            buff_u_arr =  self.a * (self.b * self.v_arr - self.u_arr)
            return  buff_u_arr
        except OverflowError as e:
            with open("log.txt", 'a') as file:
                file.write(f'{e}\n')
                file.write(f'{buff_u_arr}\n')
            return buff_u_arr

    def I_step(self):
        try:
            buff_I_arr = self.G_exc_arr*(self.arg['ve'] - self.v_arr) - (self.G_inh_arr*(self.v_arr - self.arg['vI']))
            return buff_I_arr
        except OverflowError as e:
            with open("log.txt", 'a') as file:
                file.write(f'{e}\new_matrixn')
                file.write(f'{buff_I_arr}\n')
            return buff_I_arr

    #@profile
    def G_exc_step(self):
        # sum_of_exp: (N+1) x 1 vector, sum_of_exp[j] => Summation part of Neuron j
        sum_of_exp = np.matmul(  (self.t_spike * self.exc_exponentials), np.ones(self.arg['maxSpike']) )
        return self.arg['beta'] * np.matmul( self.exc_w_matrix, sum_of_exp )

    #@profile
    def G_inh_step(self):
        #sum_of_exp: (N+1) x 1 vector, sum_of_exp[j] => Summation part of Neuron j
        sum_of_exp = np.matmul(  (self.t_spike * self.inh_exponentials), np.ones(self.arg['maxSpike']) )
        return self.arg['beta'] * np.matmul( self.inh_w_matrix, sum_of_exp )

    @profile
    def step(self):
        exceeded_indies = np.where(self.v_arr >= self.arg["max_v"])[0]
        print(f"u = {self.u_arr[0]}, v = {self.v_arr[0]}")

        # Shift one right for all sliding windows
        np.roll(self.t_spike, 1, axis=1)
        self.t_spike[:,0] = 0


        for index in exceeded_indies:
            length = self.arg['maxSpike']
            # Modify spike time for both excitory and inhibitory
            self.t_spike_indices[index] += 1
            self.t_spike[index][0] = 1

            # Reset u, v
            self.v_arr[index] = self.c[index]
            self.u_arr[index] += self.d[index]


        # Calcutaion
        new_v = self.v_step()
        new_u = self.u_step()
        
        new_G_exc = self.G_exc_step()
        new_G_inh = self.G_inh_step()
        new_I = self.I_step()
        # Replace
        self.v_arr = new_v
        self.u_arr = new_u
        self.I_arr = new_I
        self.G_exc_arr = new_G_exc
        self.G_inh_arr = new_G_inh

        self.time += self.arg["dt"]
        self.current_step += 1

        # print(self.v_arr)



if __name__ == "__main__":
    obj = NeuronNetworkTimeSeries()









    