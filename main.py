from utils.readcsv import ReadCSV
import yaml

from network.network import NeuronNetworkTimeSeries, NeuronNetwork
from network.network import NeuronNetwork, NeuronNetworkTimeSeries
import utils
import numpy as np
#import numba as nb
from tqdm import tqdm

def main():
    # 1. Load weight matrix from file
    #    Load constant values from .yaml
    with open('constants.yaml') as stream:
        network_constant = yaml.safe_load(stream)["Main"]
    w_matrix = ReadCSV(network_constant['file_path']).values
    
    # 2. Create Neuron Network from weight matrix, u, v
    network = NeuronNetworkTimeSeries(w_matrix)
    
    # 3. Step until time t, store Spike, and time series of v, u, I
    total_time_step = int(network_constant["totalTime"] / network_constant['dt'])
    for i in tqdm(range(total_time_step)):
    # while (network.time < total_time):
    #     #network.output()
        network.step()
    # pass

def test():
    with open('constants.yaml') as stream:
        network_constant = yaml.safe_load(stream)["Main"]
    w_matrix = ReadCSV(network_constant['file_path']).values
    print(w_matrix)
    network = NeuronNetworkTimeSeries(w_matrix)
    print(network.exc_node_map)
    print(network.inh_node_map)


if __name__ == "__main__":
    main()
