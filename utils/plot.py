from os import pathconf
import matplotlib.pyplot as plt
from typing import List
import os
import csv
import numpy as np
import seaborn as sns
from tqdm import tqdm

class PlotGraph:
    def __init__(self, pathname, filename):
        self.pathname = pathname
        print('Reading data...')
        with open(os.path.join(pathname, filename), 'r') as file:
            self.data = {}
            reader = csv.reader(file)
            for key, row in enumerate(tqdm(reader)):
                buff_row = []
                for value in row:
                    buff_row.append(int(value))
                self.data[key] = buff_row
        self.plot_graphs()
    
    def plot_graphs(self):
        self.firing_frequency_probability_distribution()

    def write_csv(self, data: List, filepath: str):
        with open(filepath, 'w', newline = '') as file:
            writer = csv.write(file)
            writer.writerows(data)
    
    def firing_frequency_probability_distribution(self):
        print('Calculating the firing distribution...')
        index = []
        length = []
        for i,row in self.data.items():
            index.append(i)
            length.append(len(row) / 7500)
        self.write_csv(zip(index, length), os.path.join(self.pathname, 'firing_rate.csv'))

        fig,ax = plt.subplots()
        sns.kdeplot(x = index, y = length, ax = ax)
        ax.set(xlabel = "Firing Rate (Hz)", ylabel = "Probability Density")
        fig.savefig(os.path.join(self.pathname, 'firing_rate.jpg'))