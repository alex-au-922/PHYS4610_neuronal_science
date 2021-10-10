from utils.readcsv import ReadWeightCSV
import yaml

from network.network import NeuronNetworkTimeSeries, NeuronNetwork
from network.network import NeuronNetwork, NeuronNetworkTimeSeries
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from utils.parser import parse_arg
import numpy as np
from tqdm import tqdm
import datetime
import shutil
import os
import csv
import pathlib
from utils.plot import PlotGraph
from utils.checkFunctions import removeFiles
import time

class WorkerSignal(QObject):
    progress = pyqtSignal(int, str, float)
    plotting = pyqtSignal()
    finished = pyqtSignal()

class MainExecution(QThread):
    def __init__(self, args):
        super(MainExecution,self).__init__()
        self.signal = WorkerSignal()
        self.args = args
        self.network_constant = args['Main']
        self.dt, self.totalTime = self.network_constant['dt'], self.network_constant['totalTime']
        self.total_time_step = int(self.totalTime / self.dt)
        timestamp = datetime.datetime.now()
        self.filepath = f'{timestamp}.yaml'
    
    def initialization(self):
        self.writeTempFile()
        self.initConstants()
    
    def writeTempFile(self):
        removeFiles('log.txt')
        with open('log.txt','w') as file:
            pass
        with open(self.filepath, 'w') as file:
            yaml.dump(self.args, file, default_flow_style = False)

    def initConstants(self):
        w_matrix = ReadWeightCSV(self.network_constant['file_path']).values
        self.network = NeuronNetworkTimeSeries(w_matrix, self.filepath)
        
    
    def run(self):
        start = time.time()
        finish = 0
        for counter in range(self.total_time_step):
            self.network.step()
            finish = time.time()
            _eta = int((self.total_time_step / (counter + 1) - 1)* (finish - start))
            eta = str(datetime.timedelta(seconds=_eta))
            iterRate = (counter + 1)/(finish - start)
            self.signal.progress.emit(counter, eta, iterRate)
        self.signal.plotting.emit()
        baseFolder = pathlib.Path('./result')
        if not os.path.exists(baseFolder):
            os.mkdir(baseFolder)
        
        directory = baseFolder / f'{self.dt}_{self.totalTime}'
        if not os.path.exists(directory):
            os.mkdir(directory)
        removeFiles(os.path.join(directory,'log.txt'))
        shutil.move('log.txt', directory)

        removeFiles(os.path.join(directory, 'result_constants.yaml'))
        shutil.copy(self.filepath, directory / 'result_constants.yaml')

        removeFiles(os.path.join(directory, 'log.csv'))
        with open(os.path.join(directory, 'log.csv'), 'w', newline = '') as file:
            writer = csv.writer(file)
            for key, value_list in tqdm(self.network.t_spike_record.items()):
                writer.writerow(value_list)
        
        graph = PlotGraph(directory, 'log.csv')
        self.signal.finished.emit()


def main():
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
    network = NeuronNetworkTimeSeries(w_matrix, filepath)
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

    shutil.copy(filepath, directory / 'result_constants.yaml')
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
