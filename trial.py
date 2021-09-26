from utils.plot import PlotGraph
import pathlib

def main():
    directory = pathlib.Path('./result/2021-09-26 15:57:13.940277/')
    graph = PlotGraph(directory, 'log.csv')
if __name__ == "__main__":
    main()
