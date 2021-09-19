import numpy as np
class Hi:
    def __init__(self):
        self.N = 4095
        self.maxK = 2000
        self.t_spike = [None]*(self.N + 1)
        for i in range(self.N + 1):
            self.t_spike[i] = np.zeros(self.maxK)
            for j in range(self.maxK):
                self.t_spike[i][j] = np.inf
        self.t_spike = np.array(self.t_spike)
        self.t_spike_indices = [0]*(self.N + 1)

        j_list = [2, 352, 1029, 3912]
        
        new_matrix = self.t_spike[j_list][:, :max(self.t_spike_indices)]
        self.time = 10
        print(np.sum(np.exp(-1*np.abs(self.time - new_matrix)), axis = 1))



if __name__ == "__main__":
    obj = Hi()