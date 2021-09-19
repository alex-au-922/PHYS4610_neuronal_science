from network.network import NeuronNetworkTimeSeries, NeuronNetwork
import utils
import numpy as np

def main():
    # 1. Load weight matrix from file
    w_matrix = None
    # 2. Create Neuron Network from weight matrix, u, v
    network = NeuronNetwork(w_matrix)
    # 3. Step until time t, store 
    dt = 0.125
    time = 0    
    pass


if __name__ == "__main__":
    main()
