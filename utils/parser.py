import argparse

def parse_arg():
    parser = argparse.ArgumentParser('Specify the dt, totalTime and maxSpike')
    parser.add_argument('-d', '--dt', default = 0.125, type = float, help = 'Time separations')
    parser.add_argument('-t','--totalTime', default = 7500, type = int, help = 'Total time of experiment')
    parser.add_argument('-m','--maxSpike', default = 1000, type = int, help = 'Maximum spike stored before truncation')
    parser.add_argument('-f', '--file-path', type = str, help = 'Source File')
    args = parser.parse_args()
    return args
