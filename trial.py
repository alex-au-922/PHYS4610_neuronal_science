from utils.plot import PlotGraph
import pathlib

def main():
    directory = pathlib.Path('./result/2021-09-27 17:15:42.248145/')
    graph = PlotGraph(directory, 'log.csv')
if __name__ == "__main__":
    main()
