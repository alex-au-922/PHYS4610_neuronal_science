from network.network import NeuronNetwork, NeuronNetworkTimeSeries
import utils
import numpy as np

def main():
    # 1. Load weight matrix from file
    w_matrix = None
    # 2. Create Neuron Network from weight matrix, u, v
    network = NeuronNetworkTimeSeries(w_matrix)
    # 3. Step until time t, store Spike, and time series of v, u, I
    dt = 0.125
    time = 0
    target_time = 7500
    while (time < target_time):
        network.output()
        network.step()
        time += dt
    
    pass


if __name__ == "__main__":
    main()
