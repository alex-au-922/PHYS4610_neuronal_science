import numpy as np
t_spike = np.array([0,0,0])
subset_list = [1]
subset_t_spike = t_spike[subset_list]
subset_t_spike += 1
print(t_spike)
print(subset_t_spike)
