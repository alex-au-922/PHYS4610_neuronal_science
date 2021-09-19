from .node import *
import utils.functions

class NeuronNetwork:
    def __init__(self, w_matrix, init_u_arr, init_v_arr):
        self.w_matrix = w_matrix
        self.init_u_arr = init_u_arr
        self.init_v_arr = init_v_arr
        self.node_list = []
        self.node_map = {}
        self.initialize_from_adj_matrix(w_matrix)
    
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
                self.node_map[n] = ExciNeuron(self.init_u_arr[n], self.init_v_arr[n])
            if any(self.w_matrix[i][n] < 0 for i in range(1, len(self.w_matrix))):
                self.node_map[n] = InhiNeuron(self.init_u_arr[n], self.init_v_arr[n])
            self.node_list.append(self.node_map[n])
                    
class NeuronNetworkTimeSeries:
    def __init__(self):
        self.initLowBound = -10
        self.initUpBound = 10
        self.numberOfNodes = 4095
        self.init_u_arr = utils.functions.random_vec(self.numberOfNodes + 1, self.initLowBound, self.initUpBound)
        self.init_v_arr = utils.functions.random_vec(self.numberOfNodes + 1, self.initLowBound, self.initUpBound)

       





    