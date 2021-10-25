from .node import *
import yaml
import utils.functions
from utils.checkFunctions import check_node_type
import numpy as np
from tqdm import tqdm
import math
import os
from utils.logger import BaseLogger

np.seterr(all='raise')

class NeuronNetwork:
    def __init__(self, w_matrix, filePath
    ):
        self.w_matrix = w_matrix
        self.N = len(w_matrix) - 1
        log = BaseLogger(self.__class__.__name__)
        self.logger = log.logger
        self.arg = {}
        with open(filePath) as stream:
            self.arg.update(yaml.load(stream, Loader=yaml.SafeLoader)['NeuronNetwork'])
        
        for key, value in self.arg.items():
            self.logger.info(f'{key} = {value}')
        
        utils.functions.random_seed(self.arg['seed'])
        self.I_arr = np.zeros(self.N + 1)
        if os.environ.get('DEBUG'):
            self.u_arr = utils.functions.random_u_vec(filePath = 'data/u_init.txt')
            self.v_arr = utils.functions.random_v_vec(filePath = 'data/v_init.txt')
        else:
            self.u_arr = utils.functions.random_v_vec(numberOfNodes = self.N + 1, lowBound = self.arg['UinitLowBound'], upBound = self.arg['UinitUpBound'])
            self.v_arr = utils.functions.random_u_vec(numberOfNodes = self.N + 1, lowBound = self.arg['VinitLowBound'], upBound = self.arg['VinitUpBound'])
        self.buff_u_arr = np.zeros_like(self.u_arr) 
        self.buff_v_arr = np.zeros_like(self.v_arr)
        self.buff_I_arr = np.zeros_like(self.I_arr)
        self.G_exc_arr = np.zeros(self.N + 1)
        self.G_inh_arr = np.zeros(self.N + 1)
        self.t_spike = [np.zeros(self.arg['maxSpike']) for _ in range(self.N + 1)]
        self.t_spike = np.array(self.t_spike)

        self.t_spike_record = {key:[] for key in range(self.N + 1)}
        self.reset_index = []
        self.node_type_map = {}
        self.node_type_map[0] = 0

        self.exc_w_matrix = np.zeros_like(self.w_matrix)
        self.inh_w_matrix = np.zeros_like(self.w_matrix) # All positive values (absoluted)

        self.initialize_from_adj_matrix()

        self.one_vec = np.ones(self.arg['maxSpike'])

        self.a = self.create_constant_list(self.arg["EXCITED"]["a"], self.arg["INHIBIT"]["a"])
        self.b = self.create_constant_list(self.arg["EXCITED"]["b"], self.arg["INHIBIT"]["b"])
        self.c = self.create_constant_list(self.arg["EXCITED"]["c"], self.arg["INHIBIT"]["c"])
        self.d = self.create_constant_list(self.arg["EXCITED"]["d"], self.arg["INHIBIT"]["d"])
    
    def create_constant_list(self, exc, inh):
        return np.array([inh if (self.node_type_map[n] == -1) else exc for n in range(self.N + 1) ])  

    def initialize_from_adj_matrix(self):
        print("Initializing the sparse matrix from adjacency matrix...")
        check_node_type(self.w_matrix)
        (i_max, j_max) = self.w_matrix.shape
        for i in range(1, i_max):
            self.node_type_map[i] = 0
        for i in tqdm(range(1, i_max)):
            for j in range(1, j_max):
                w_ij = self.w_matrix[i][j]
                if (w_ij > 0):
                    assert self.node_type_map[j] >=0 
                    self.node_type_map[j] = 1
                    self.exc_w_matrix[i][j] = w_ij
                if (w_ij < 0):
                    assert self.node_type_map[j] <=0 
                    self.node_type_map[j] = -1
                    self.inh_w_matrix[i][j] = abs(w_ij)
                    
class NeuronNetworkTimeSeries(NeuronNetwork):
    def __init__(self, w_matrix, filePath):
        super().__init__(w_matrix = w_matrix, filePath = filePath)
        self.time = 0
        self.current_step = 0
        log = BaseLogger(self.__class__.__name__)
        self.logger = log.logger
        self.overflow_reset_index = []
        with open(filePath) as stream:
            self.arg.update(yaml.load(stream)['NeuronNetworkTimeSeries'])
        
        for key, value in self.arg.items():
            self.logger.info(f'{key} = {value}')

        self.exc_exponentials = [math.exp( -(n * self.arg['dt'])/(self.arg['tauExc']) ) for n in range(self.arg['maxSpike'])]
        self.logger.info(f'{self.exc_exponentials}')
        self.inh_exponentials = [math.exp( -(n * self.arg['dt'])/(self.arg['tauInh']) ) for n in range(self.arg['maxSpike'])]
        self.logger.info(f'{self.inh_exponentials}')
    
    def v_step(self):
        try:
            noise_arr = utils.functions.random_gaussian(self.arg['sigma'], len(self.v_arr))*np.sqrt(self.arg['dt'])
            # self.logger.info(f'{noise_arr}')
            self.buff_v_arr = self.v_arr +(self.arg['c1']*self.v_arr**2 + self.arg['c2'] * self.v_arr 
                + self.arg['c3'] + self.arg['c4'] * self.u_arr+ self.arg['c5']*self.I_arr)*self.arg['dt'] + noise_arr
            self.logger.info(f'{self.buff_v_arr[:10]}')
        except Exception as e:
            self.logger.info(f'{e}')
            for i in range(len(self.buff_v_arr)):
                try:
                    self.buff_v_arr[i] = self.v_arr[i] +(self.arg['c1']*self.v_arr[i]**2 + self.arg['c2'] * self.v_arr[i] 
                    + self.arg['c3'] + self.arg['c4'] * self.u_arr[i]+ self.arg['c5']*self.I_arr[i])*self.arg['dt'] + noise_arr[i]
                except Exception as e:
                    self.overflow_reset_index.append(i)
                    self.logger.exception(f'Index {i} has an overflow.\n{self.buff_v_arr[i]}')


    def u_step(self):
        try:
            self.buff_u_arr =  self.u_arr + (self.a * (self.b * self.v_arr - self.u_arr))*self.arg['dt']
        except Exception as e:
            self.logger.info(f'{e}')
            for i in range(len(self.buff_u_arr)):
                try:
                    self.buff_u_arr[i] = self.u_arr[i] + (self.a[i] * (self.b[i] * self.v_arr[i] - self.u_arr[i]))*self.arg['dt']
                except Exception as e:
                    self.overflow_reset_index.append(i)
                    self.logger.exception(f'Index {i} has an overflow.\n{self.buff_u_arr[i]}')

    def I_step(self):
        try:
            self.buff_I_arr = self.G_exc_arr*(self.arg['ve'] - self.v_arr) - (self.G_inh_arr*(self.v_arr - self.arg['vI']))
        except Exception as e:
            self.logger.info(f'{e}')
            for i in range(len(self.buff_I_arr)):
                try:
                    self.buff_I_arr[i] = self.G_exc_arr[i]*(self.arg['ve'] - self.v_arr[i]) - (self.G_inh_arr[i]*(self.v_arr[i] - self.arg['vI']))
                except Exception as e:
                    self.overflow_reset_index.append(i)
                    self.logger.exception(f'Index {i} has an overflow.\n{self.buff_I_arr[i]}')

    #@profile
    def G_exc_step(self):
        # sum_of_exp: (N+1) x 1 vector, sum_of_exp[j] => Summation part of Neuron j
        sum_of_exp = np.matmul(  (self.t_spike * self.exc_exponentials), self.one_vec )
        # self.logger.info(f'{self.t_spike = }')
        # self.logger.info(f'{self.exc_exponentials = }')
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
            
            self.t_spike_record[index].append(self.current_step)
            self.t_spike[index][0] = 1

            # Reset u, v
            self.v_arr[index] = self.c[index]
            self.u_arr[index] += self.d[index]

        # Calcutaion
        self.v_step()
        self.u_step()
        
        new_G_exc = self.G_exc_step()
        new_G_inh = self.G_inh_step()
        
        self.I_step()
        # Replace
        self.v_arr = self.buff_v_arr
        self.u_arr = self.buff_u_arr
        self.I_arr = self.buff_I_arr
        self.G_exc_arr = new_G_exc
        self.G_inh_arr = new_G_inh

        if self.overflow_reset_index != []:
            self.overflow_reset_index = list(set(self.overflow_reset_index))
            self.v_arr[self.overflow_reset_index] = self.c[self.overflow_reset_index]
            self.u_arr[self.overflow_reset_index] += self.d[self.overflow_reset_index]
            self.overflow_reset_index = []

        
       
        self.time += self.arg["dt"]
        self.current_step += 1

        # print(self.v_arr)



if __name__ == "__main__":
    obj = NeuronNetworkTimeSeries()









    