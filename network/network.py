from .node import *

class NeuronNetwork:
    def __init__(self, w_matrix):
        self.node_list = []
        self.node_map = {}
        self.initialize_from_adj_matrix(w_matrix)
    
    def check_node_type(self,w_matrix):
        '''Check whether the node type is consistent'''
        for column in w_matrix.T:
            assert all(column >= 0) or all(column <= 0)   

    def initialize_from_adj_matrix(self, w_matrix):
        (i_max, j_max) = w_matrix.shape
        for i in range(1, i_max):
            for j in range(1, j_max):
                if w_matrix[i][j] == 0:
                    continue
                if (i, j) in self.node_map:
                    continue
                self.node_map[(i, j)] = Neuron()



    