from numba.np.ufunc import parallel
from .node import *
import yaml
import utils.functions
import numpy as np
import numba as nb
from tqdm import tqdm
import csv
import math

np.seterr(all='raise')

class NeuronNetwork:
    def __init__(self, w_matrix, filePath):
        self.w_matrix = w_matrix
        self.N = len(w_matrix) - 1
        self.arg = {}
        with open(filePath) as stream:
            self.arg.update(yaml.load(stream, Loader=yaml.SafeLoader)['NeuronNetwork'])
        
        utils.functions.random_seed(self.arg['seed'])
        self.I_arr = np.zeros(self.N + 1)
        self.u_arr = utils.functions.random_vec(self.N + 1, self.arg['VinitLowBound'], self.arg['VinitUpBound'])
        self.v_arr = utils.functions.random_vec(self.N + 1, self.arg['UinitLowBound'], self.arg['UinitUpBound'])
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
        self.t_spike_record = {key:[] for key in range(self.N + 1)}
        self.reset_index = []

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

        
            

        self.one_vec = np.ones(self.arg['maxSpike'])

        self.a = self.create_constant_list(self.arg["EXCITED"]["a"], self.arg["INHIBIT"]["a"])
        self.b = self.create_constant_list(self.arg["EXCITED"]["b"], self.arg["INHIBIT"]["b"])
        self.c = self.create_constant_list(self.arg["EXCITED"]["c"], self.arg["INHIBIT"]["c"])
        self.d = self.create_constant_list(self.arg["EXCITED"]["d"], self.arg["INHIBIT"]["d"])
    
    def create_constant_list(self, exc, inh):
        return np.array([inh if (self.node_type_map[n] == -1) else exc for n in range(self.N + 1) ])

    def check_node_type(self,w_matrix):
        '''Check whether the node type is consistent'''
        for column in w_matrix.T:
            assert all(column >= 0) or all(column <= 0)   

    def initialize_from_adj_matrix(self):
        print("Initializing the sparse matrix from adjacency matrix...")
        (i_max, j_max) = self.w_matrix.shape
        for i in range(1, i_max):
            self.node_type_map[i] = 0
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
                # self.node_type_map[j] = 0

        
        for i, j_list in self.exc_node_map.items():
            self.weight_map[i] = self.w_matrix[i][j_list]
                    
class NeuronNetworkTimeSeries(NeuronNetwork):
    def __init__(self, w_matrix, filePath):
        super().__init__(w_matrix = w_matrix, filePath = filePath)
        self.time = 0
        self.current_step = 0
        with open(filePath) as stream:
            self.arg.update(yaml.load(stream)['NeuronNetworkTimeSeries'])
        self.exc_decay_factor = np.exp(-1*self.arg['dt'] / self.arg['tauExc'])
        self.inh_decay_factor = np.exp(-1*self.arg['dt'] / self.arg['tauInh'])

        self.exc_exponentials = [math.exp( -(n * self.arg['dt'])/(self.arg['tauExc']) ) for n in range(self.arg['maxSpike'])]
        self.inh_exponentials = [math.exp( -(n * self.arg['dt'])/(self.arg['tauInh']) ) for n in range(self.arg['maxSpike'])]
    
    def v_step(self):
        noise_arr = np.ones_like(self.v_arr) * \
            utils.functions.random_gaussian(self.arg['sigma'], len(self.v_arr))*np.sqrt(self.arg['dt'])
        try:
            self.buff_v_arr = self.v_arr +(self.arg['c1']*self.v_arr**2 + self.arg['c2'] * self.v_arr 
             + self.arg['c3'] + self.arg['c4'] * self.u_arr+ self.arg['c5']*self.I_arr)*self.arg['dt'] + noise_arr
        except Exception as e:
            with open("log.txt", 'a') as file:
                file.write(f'{e}\n')
                file.write(f'{self.buff_v_arr = }\n')

            # @nb.njit()
            def check_overflow():
                for i in range(len(self.v_arr)):
                    try:
                        self.buff_v_arr[i] = self.v_arr[i] + (self.arg['c1']*self.v_arr[i]**2 + self.arg['c2'] * self.v_arr[i] \
                            + self.arg['c3'] + self.arg['c4'] * self.u_arr + self.arg['c5'] * self.I_arr[i]) * self.arg['dt']+ noise_arr[i]
                    except Exception:
                        self.reset_index.append(i)

            check_overflow()

    def u_step(self):
        try:
            self.buff_u_arr =  self.u_arr + (self.a * (self.b * self.v_arr - self.u_arr))*self.arg['dt']
        except Exception as e:
            with open("log.txt", 'a') as file:
                file.write(f'{e}\n')
                file.write(f'{self.buff_u_arr = }\n')
            
            # @nb.njit()
            def check_overflow():
                for i in range(len(self.u_arr)):
                    try:
                        self.buff_u_arr[i] =  self.u_arr[i] + (self.a[i] * (self.b[i] * self.v_arr[i] - self.u_arr[i]))*self.arg['dt']
                    except Exception:
                        self.reset_index.append(i)
            
            check_overflow()
        #self.buff_u_arr =  np.clip(self.u_arr + (self.a * (self.b * self.v_arr - self.u_arr))*self.arg['dt'], -1e5, 1e5, self.b*self.v_arr)

    def I_step(self):
        try:
            self.buff_I_arr = self.G_exc_arr*(self.arg['ve'] - self.v_arr) - (self.G_inh_arr*(self.v_arr - self.arg['vI']))
        except Exception as e:
            with open("log.txt", 'a') as file:
                file.write(f'{e}\n')
                file.write(f'{self.buff_I_arr = }\n')
            self.buff_I_arr = self.arg['beta']*(self.G_exc_arr*(self.arg['ve'] - self.v_arr) - (self.G_inh_arr*(self.v_arr - self.arg['vI'])))

    #@profile
    def G_exc_step(self):
        # sum_of_exp: (N+1) x 1 vector, sum_of_exp[j] => Summation part of Neuron j
        sum_of_exp = np.matmul(  (self.t_spike * self.exc_exponentials), self.one_vec )
        return self.arg['beta'] * np.matmul( self.exc_w_matrix, sum_of_exp )

    #@profile
    def G_inh_step(self):
        #sum_of_exp: (N+1) x 1 vector, sum_of_exp[j] => Summation part of Neuron j
        sum_of_exp = np.matmul(  (self.t_spike * self.inh_exponentials), self.one_vec )
        return self.arg['beta'] * np.matmul( self.inh_w_matrix, sum_of_exp )

    # @profile
    def step(self):
        exceeded_indies = np.where(self.v_arr >= self.arg["max_v"])[0]
        # print(f"u = {self.u_arr[0]}, v = {self.v_arr[0]}")

        # Shift one right for all sliding windows
        self.t_spike = np.roll(self.t_spike, 1, axis=1)
        self.t_spike[:,0] = 0


        for index in exceeded_indies:
            # length = self.arg['maxSpike']
            # Modify spike time for both excitory and inhibitory
            #self.exc_t_spike[index][self.t_spike_indices[index] % self.arg['maxSpike']] = 1
            #self.inh_t_spike[index][self.t_spike_indices[index] % self.arg['maxSpike']] = 1
            
            self.t_spike_record[index].append(self.current_step)
            self.t_spike_indices[index] += 1
            self.t_spike[index][0] = 1

            # Reset u, v
            self.v_arr[index] = self.c[index]
            self.u_arr[index] += self.d[index]


        # Calcutaion
        self.v_step()
        self.u_step()

        if self.reset_index != []:
            self.buff_v_arr[self.reset_index] = self.c[self.reset_index]
            self.buff_u_arr[self.reset_index] = (self.b*self.v_arr)[self.reset_index]
            self.reset_index = []
        
        new_G_exc = self.G_exc_step()
        new_G_inh = self.G_inh_step()


        self.I_step()
        # Replace
        self.v_arr = self.buff_v_arr
        self.u_arr = self.buff_u_arr
        self.I_arr = self.buff_I_arr
        self.G_exc_arr = new_G_exc
        self.G_inh_arr = new_G_inh
       
        self.time += self.arg["dt"]
        self.current_step += 1

        # print(self.v_arr)



if __name__ == "__main__":
    obj = NeuronNetworkTimeSeries()









    