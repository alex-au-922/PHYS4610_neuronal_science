from numba.np.ufunc import parallel
from .node import *
import yaml
import utils.functions
import numpy as np
import numba as nb
from tqdm import tqdm

np.seterr(all='raise')

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
        self.exc_t_spike = np.array(self.t_spike)
        self.inh_t_spike = np.array(self.t_spike)
        self.t_spike_indices = [0]*(self.N + 1)
        self.t_spike_record = [[]]*(self.N + 1)
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
        self.initialize_from_adj_matrix()

        self.mat = np.ones(self.arg['maxSpike'])

        self.a = self.create_constant_list(self.arg["EXCITED"]["a"], self.arg["INHIBIT"]["a"])
        self.b = self.create_constant_list(self.arg["EXCITED"]["b"], self.arg["INHIBIT"]["b"])
        self.c = self.create_constant_list(self.arg["EXCITED"]["c"], self.arg["INHIBIT"]["c"])
        self.d = self.create_constant_list(self.arg["EXCITED"]["d"], self.arg["INHIBIT"]["d"])
    
    def create_constant_list(self, exc, inh):
        return np.array([exc if (self.node_type_map[n] == 1) else inh if (self.node_type_map[n] == -1) else 0 for n in range(self.N + 1) ])

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
                    
class NeuronNetworkTimeSeries(NeuronNetwork):
    def __init__(self, w_matrix):
        super().__init__(w_matrix = w_matrix)
        self.time = 0
        with open('constants.yaml') as stream:
            self.arg.update(yaml.load(stream)['NeuronNetworkTimeSeries'])
        self.exc_decay_factor = np.exp(-1*self.arg['dt'] / self.arg['tauExc'])
        self.inh_decay_factor = np.exp(-1*self.arg['dt'] / self.arg['tauInh'])
    
    def v_step(self):
        noise_arr = np.ones_like(self.v_arr) * \
            utils.functions.random_gaussian(self.arg['sigma'], len(self.v_arr))*np.sqrt(self.arg['dt'])
        try:
            self.buff_v_arr = self.v_arr +(self.arg['c1']*self.v_arr**2 + self.arg['c2'] * self.v_arr \
             + self.arg['c3'] - self.arg['c4'] * self.u_arr+ self.arg['c5']*self.I_arr+ noise_arr)*self.arg['dt'] 
        except Exception as e:
            with open("log.txt", 'a') as file:
                file.write(f'{e}\n')
                file.write(f'{self.buff_v_arr = }\n')

            # @nb.njit()
            def check_overflow():
                for i in nb.prange(len(self.v_arr)):
                    try:
                        self.buff_v_arr[i] = self.v_arr[i] + (self.arg['c1']*self.v_arr[i]**2 + self.arg['c2'] * self.v_arr[i] \
                            + self.arg['c3'] - self.arg['c4'] * self.u_arr + self.arg['c5'] * self.I_arr[i] + noise_arr) * self.arg['dt']
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
                for i in nb.prange(len(self.u_arr)):
                    try:
                        self.buff_u_arr[i] =  self.u_arr[i] + (self.a[i] * (self.b[i] * self.v_arr[i] - self.u_arr[i]))*self.arg['dt']
                    except Exception:
                        self.reset_index.append(i)
            
            check_overflow()

    def I_step(self):
        try:
            self.buff_I_arr = self.G_exc_arr*(self.arg['ve'] - self.v_arr) - (self.G_inh_arr*(self.v_arr - self.arg['vI']))
        except Exception as e:
            with open("log.txt", 'a') as file:
                file.write(f'{e}\n')
                file.write(f'{self.buff_I_arr = }\n')
            self.buff_I_arr = self.G_exc_arr*(self.arg['ve'] - self.v_arr) - (self.G_inh_arr*(self.v_arr - self.arg['vI']))


    def G_exc_step(self):
        # Loop for all keys
        buff_G_exc = np.zeros_like(self.G_exc_arr)
        for i, j_list in self.exc_node_map.items():
            # new_matrix = np.exp(-1*np.abs(self.time - self.t_spike[j_list])/self.arg['tauExc'])
            gamma_j = np.matmul(self.exc_t_spike[j_list], self.mat)
            weight = self.w_matrix[:, i][j_list]
            try:
                buff_G_exc[i] = self.arg['beta']*np.matmul(weight, gamma_j)
            except Exception as e:
                with open("log.txt", 'a') as file:
                    file.write(f'{e}\n')
                    file.write(f'{buff_G_exc = }\n')

        return buff_G_exc

    def G_inh_step(self):
        buff_G_inh = np.zeros_like(self.G_inh_arr)
        for i, j_list in self.inh_node_map.items():
            # new_matrix = np.exp(-1*np.abs(self.time - self.t_spike[j_list])/self.arg['tauInh'])
            gamma_j = np.matmul(self.inh_t_spike[j_list], self.mat)
            weight = np.abs(self.w_matrix[:, i][j_list])
            try:
                buff_G_inh[i] = self.arg['beta']*np.matmul(weight, gamma_j)
            except Exception as e:
                with open("log.txt", 'a') as file:
                    file.write(f'{e}\n')
                    file.write(f'{buff_G_inh = }\n')

        return buff_G_inh

    def step(self):
        exceeded_indies = np.where(self.v_arr >= self.arg["max_v"])[0]
        for index in exceeded_indies:
            # Modify spike time for both excitory and inhibitory
            self.exc_t_spike[index][self.t_spike_indices[index] % self.arg['maxSpike']] = 1
            self.inh_t_spike[index][self.t_spike_indices[index] % self.arg['maxSpike']] = 1
            self.t_spike_record[index].append(self.time // self.arg['dt'])
            self.t_spike_indices[index] += 1
            # Reset u, v
            self.v_arr[index] = self.c[index]
            self.u_arr[index] += self.d[index]
        
        # Exponential decay for every time step 
        self.exc_t_spike *= self.exc_decay_factor
        self.inh_t_spike *= self.inh_decay_factor

        # Calcutaion
        self.v_step()
        self.u_step()

        if self.reset_index != []:
            self.buff_v_arr[self.reset_index] = self.c[self.reset_index]
            self.buff_u_arr[self.reset_index] = self.c[self.reset_index]
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

        # print(self.v_arr)



if __name__ == "__main__":
    obj = NeuronNetworkTimeSeries()









    