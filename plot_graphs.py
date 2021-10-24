import pathlib
from utils.plot import PlotGraph
import argparse
import os
from datetime import datetime

def define_parse():
    parser = argparse.ArgumentParser('Specify the directory and bins of the plot.')
    parser.add_argument('-d', '--dir', type=str, default = None, help = 'Path to directory where log.csv exists.')
    parser.add_argument('-fb', '--fire_bin_size', type=float, default = 0.1, help='Bins of the firing frequency plot.')
    parser.add_argument('-ib', '--isi_bin_size', type=float, default = 0.1, help='Bins of the ISI plot.')
    args = parser.parse_args()
    return args

if __name__ =="__main__":
    args = define_parse()
    if args.dir is None:    
        basePath = pathlib.Path('./result')
        filelist = os.listdir(basePath)
        fileDict = {datetime.strptime(key, "%Y-%m-%d %H:%M:%S.%f"):key for key in filelist}
        max_time = max(fileDict.keys())
        directory = basePath / fileDict[max_time]
    else:
        directory = pathlib.Path(args.dir)
    
    print(directory)

    try:
        graph = PlotGraph(directory, 'log.csv', args.fire_bin_size, args.isi_bin_size)
    except OSError as e:
        print(f'{directory} does not exist!')