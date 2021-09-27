from utils.plot import PlotGraph
import pathlib

def main():
    directory = pathlib.Path('./result/2021-09-27 22:52:01.068981/')
    graph = PlotGraph(directory, 'log.csv')
if __name__ == "__main__":
    main()
