from os import pathconf
import matplotlib.pyplot as plt
from typing import List
import os
import pandas as pd
import numpy as np

class PlotGraph:
    def __init__(self, pathname, filename):
        print('Reading data...')
        self.data = pd.read_csv(os.path.join(pathname, filename), header = None).values
        print(self.data)

    def firing_frequency_probability_distribution(data: List[List[int]], pathname: str):
        pass

