from os import pathconf
import matplotlib.pyplot as plt
from typing import List
import os
import csv
import yaml
import numpy as np
import seaborn as sns
from tqdm import tqdm

class PlotGraph:
    def __init__(self, pathname, filename, firing_bin = 40, isi_bin = 40):
        self.pathname = pathname
        self.firing_bin = firing_bin
        self.isi_bin = isi_bin
        self.t_arr = []
        self.n_arr = []

        print('Reading data...')
        with open(os.path.join(pathname,'result_constants.yaml')) as stream:
            self.arg = yaml.safe_load(stream)['Plot']
        with open(os.path.join(pathname, filename), 'r') as file:
            self.data = []
            reader = csv.reader(file)
            for key, row in enumerate(tqdm(reader)):
                buff_row = []
                for value in row:
                    buff_row.append(int(value))
                    if key != 0: # Not the first node
                        self.t_arr.append(int(value) * self.arg['dt'] / 1000) # Get the absolute time
                        self.n_arr.append(key)
                self.data.append(buff_row)
            self.t_arr = np.array(self.t_arr)
            self.n_arr = np.array(self.n_arr)
        self.plot_graphs()
    
    def plot_graphs(self):
        self.firing_frequency_probability_distribution()
        self.log_spike_interval()
        self.spike_raster_plot()
        

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
            length.append(len(row) / (self.arg['totalTime'] / 1000) )
        self.write_csv(zip(index, length), os.path.join(self.pathname, 'firing_rate.csv'))

        length = np.array(length)
        # density, x_value = np.histogram(length, bins = np.linspace(0, np.max(length), self.firing_bin), density = True)
        density, x_value = np.histogram(length, bins = np.linspace(0, 12, self.firing_bin), density = True)
        x_value = x_value[:-1]

        fig,ax = plt.subplots()
        ax.plot(x_value, density)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, None)
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
                # interval.append(int(self.arg['totalTime'] / self.arg['dt']) - row[0])
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
        self.write_csv(zip(index, interval), os.path.join(self.pathname, 'log_spike_interval.csv'))

        interval = np.log10(np.array(interval, dtype = np.float64)*self.arg['dt'] / 1000)
        density, x_value = np.histogram(interval, bins = np.linspace((np.min(interval)), np.max(interval), self.isi_bin), density = True)
        x_value = np.power(10,x_value)
        x_value = (x_value[1:] + x_value[:-1])/2

        fig,ax = plt.subplots()
        ax.semilogx(x_value,density)
        ax.set_xlim(1e-4, 1e2)
        ax.set(xlabel = "ISI (s)", ylabel = "Probability Density")
        fig.savefig(os.path.join(self.pathname, 'log_spike_interval.jpg'))

    def spike_raster_plot(self):
        fig,ax = plt.subplots(figsize = (20,10))
        ax.plot(self.t_arr, self.n_arr, '.', markersize=1)
        ax.set(xlabel = 'Time (s)', ylabel = 'Neuron Index')
        ax.set_xlim(0, None)
        ax.set_ylim(0, None)
        fig.savefig(os.path.join(self.pathname, 'spike_raster_plot.jpg'))


        


            
