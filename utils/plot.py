from os import pathconf
import matplotlib.pyplot as plt
from typing import List
import os
import csv
import yaml
import numpy as np
import seaborn as sns
from tqdm import tqdm
import numba as nb

class PlotGraph:
    def __init__(self, pathname, filename):
        self.pathname = pathname
        print('Reading data...')
        with open(os.path.join(pathname, filename), 'r') as file:
            self.data = []
            reader = csv.reader(file)
            for key, row in enumerate(tqdm(reader)):
                buff_row = []
                for value in row:
                    buff_row.append(int(value))
                self.data.append(buff_row)
        with open('constants.yaml') as stream:
            self.arg = yaml.safe_load(stream)['Plot']
        self.plot_graphs()
    
    def plot_graphs(self):
        self.firing_frequency_probability_distribution()
        self.log_spike_interval()
        

    def write_csv(self, data: List, filepath: str):
        with open(filepath, 'w', newline = '') as file:
            writer = csv.writer(file)
            writer.writerows(data)
    
    def firing_frequency_probability_distribution(self):
        print('Calculating the firing distribution...')
        index = []
        length = []
        for i,row in enumerate(self.data):
            index.append(i)
            length.append(len(row) / self.arg['totalTime'])
        self.write_csv(zip(index, length), os.path.join(self.pathname, 'firing_rate.csv'))

        fig,ax = plt.subplots()
        sns.kdeplot(x = length, ax = ax)
        ax.set(xlabel = "Firing Rate (Hz)", ylabel = "Probability Density")
        fig.savefig(os.path.join(self.pathname, 'firing_rate.jpg'))
    
    def calculate_interval(self):
        interval = []
        index = []
        count = 0
        for row in tqdm(self.data):
            if len(row) == 0:
                continue
            elif len(row) == 1:
                interval.append(int(self.arg['totalTime'] / self.arg['dt']) - row[0])
            else:
                buff_row = [0] * (len(row) - 1)
                for j in range(len(buff_row)):
                    buff_row[j] = row[j + 1] - row[j]
                    index.append(count)
                    count += 1
                interval.extend(buff_row)
        return index, interval
    
    def log_spike_interval(self):
        print('Calculating the spike intervals...')

        index, interval = self.calculate_interval()
        # self.write_csv(zip(index, interval), os.path.join(self.pathname, 'log_spike_interval.csv'))

        interval = np.array(interval, dtype = np.float64)

        fig,ax = plt.subplots()
        sns.kdeplot(x = interval*self.arg['dt'] / 1000, ax = ax)
        ax.set(xlabel = "ISI (s)", ylabel = "Probability Density")
        ax.set_xscale('log')
        fig.savefig(os.path.join(self.pathname, 'log_spike_interval.jpg'))

        


            
