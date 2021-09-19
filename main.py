import yaml
from network.network import NeuronNetwork, NeuronNetworkTimeSeries
import utils
import numpy as np

def main():
    # 1. Load weight matrix from file
    #    Load constant values from .yaml
    w_matrix = None
    with open('constants.yaml') as stream:
        network_constant = yaml.safe_load(stream)["NeuronNetwork"]
    
    # 2. Create Neuron Network from weight matrix, u, v
    network = NeuronNetworkTimeSeries(w_matrix)
    
    # 3. Step until time t, store Spike, and time series of v, u, I
    total_time = network_constant["totalTime"]
    while (network.time < total_time):
        network.output()
        network.step()
    pass


if __name__ == "__main__":
    main()
