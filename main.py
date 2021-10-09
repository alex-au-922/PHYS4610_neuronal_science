from utils.readcsv import ReadWeightCSV
import yaml

from network.network import NeuronNetworkTimeSeries, NeuronNetwork
from network.network import NeuronNetwork, NeuronNetworkTimeSeries
import utils
import numpy as np
import numba as nb
from tqdm import tqdm
import datetime
import shutil
import os
import csv
import pathlib
from utils.plot import PlotGraph
from utils.parser import parse_arg

def main():
    # 1. Load weight matrix from file
    #    Load constant values from .yaml

    args = parse_arg()
    with open('constants.yaml') as stream:
        buff_arg = yaml.safe_load(stream)
    for key, value in buff_arg.items():
        if 'dt' in value:
            value['dt'] = args.dt
        if 'totalTime' in value:
            value['totalTime'] = args.totalTime
        if 'maxSpike' in value:
            value['maxSpike'] = args.maxSpike
    timestamp = datetime.datetime.now()
    filepath = f'{timestamp}.yaml'
    with open(filepath, 'w') as file:
        yaml.dump(buff_arg, file, default_flow_style = False)


    with open(filepath) as stream:
        network_constant = yaml.safe_load(stream)["Main"]
    w_matrix = ReadWeightCSV(network_constant['file_path']).values

    if os.path.exists('log.txt'):
        os.remove('log.txt')
    with open('log.txt','w') as file:
        pass
    
    # 2. Create Neuron Network from weight matrix, u, v
    network = NeuronNetworkTimeSeries(w_matrix)
    dt, totalTime = network_constant['dt'], network_constant['totalTime']
    # 3. Step until time t, store Spike, and time series of v, u, I
    total_time_step = int(totalTime / dt)

    for _ in tqdm(range(total_time_step)):
    # while (network.time < total_time):
    #     #network.output()
        network.step()
        # break
    
    baseFolder = pathlib.Path('./result')
    if not os.path.exists(baseFolder):
        os.mkdir(baseFolder)
    
    directory = baseFolder / f'{dt}_{totalTime}'
    os.mkdir(directory)
    shutil.move('log.txt', directory)

    shutil.copy(filepath, directory / 'constants.yaml')
    print('Writing spikes record...')
    with open(os.path.join(directory, 'log.csv'), 'w', newline = '') as file:
        writer = csv.writer(file)
        for key, value_list in tqdm(network.t_spike_record.items()):
            writer.writerow(value_list)
    
    graph = PlotGraph(directory, 'log.csv')

    # pass

def test():
    with open('constants.yaml') as stream:
        network_constant = yaml.safe_load(stream)["Main"]
    w_matrix = ReadWeightCSV(network_constant['file_path']).values
    print(w_matrix)
    network = NeuronNetworkTimeSeries(w_matrix)
    print(network.exc_node_map)
    print(network.inh_node_map)


if __name__ == "__main__":
    main()
