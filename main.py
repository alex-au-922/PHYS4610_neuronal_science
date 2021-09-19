<<<<<<< HEAD
from network.network import NeuronNetworkTimeSeries, NeuronNetwork
=======
from network.network import NeuronNetwork, NeuronNetworkTimeSeries
>>>>>>> e60568a150a953a2ea37deb3552d5165d2f5089e
import utils
import numpy as np

def main():
    # 1. Load weight matrix from file
    w_matrix = None
    # 2. Create Neuron Network from weight matrix, u, v
    network = NeuronNetworkTimeSeries(w_matrix)
    # 3. Step until time t, store Spike, and time series of v, u, I
    dt = 0.125
<<<<<<< HEAD
    time = 0    
=======
    time = 0
    target_time = 7500
    while (time < target_time):
        network.output()
        network.step()
        time += dt
    
>>>>>>> e60568a150a953a2ea37deb3552d5165d2f5089e
    pass


if __name__ == "__main__":
    main()
