import numpy as np
class Hi:
    def __init__(self):
        self.N = 4095
        self.t_spike = [None]*(self.N + 1)
        for i in range(len(self.t_spike)):
            self.t_spike[i]= [np.inf,1,2]
            self.t_spike[i] = np.array(self.t_spike[i])
        self.t_spike = np.array(self.t_spike)
        j_list = [1,2,3]
        self.time = 3
        print(self.t_spike)
        print(np.sum(np.expself.t_spike[j_list][:,1:])

        
if __name__ == "__main__":
    obj = Hi()