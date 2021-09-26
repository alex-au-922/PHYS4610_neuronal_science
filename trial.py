from utils.plot import PlotGraph
import pathlib

def main():
    directory = pathlib('./result/')
    graph = PlotGraph(directory, 'log.csv')
    