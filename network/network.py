from .node import *

class NeuronNetwork:
    def __init__(self, w_matrix):
        self.node_list = []
        self.node_map = {}
        self.initialize_from_adj_matrix(w_matrix)
        
        
        
        
    def initialize_from_adj_matrix(self, w_matrix):
        (i_max, j_max) = w_matrix.shape
        for i in range(1, i_max):
            for j in range(1, j_max):
                if w_matrix[i][j] == 0:
                    continue
                if j not in self.node_map:
                    if (w_matrix[i][j] > 0):
                        temp = ExciNeuron()
                        self.node_map[j] = temp
                        self.node_list.append(temp)
                    if (w_matrix[i][j] < 0):
                        temp = InhiNeuron()
                        self.node_map[j] = temp
                        self.node_list.append(temp)
                    continue
                if j in self.node_map:
                    pass


                





    