import csv 
import yaml
import pathlib
def convert_to_Johns_plotting_function(baseFilePath):
    baseFilePath = pathlib.Path(baseFilePath)
    constantFilePath = baseFilePath / 'result_constants.yaml'
    outSpikeFilePath = baseFilePath / 'log.csv'
    outputSPIKETxt = 'OUT_SPIK.txt'
    configTxt = 'INI_CNFG'
    with open(constantFilePath, 'r') as stream:
        args = yaml.safe_load(stream)['Plot']
    with open(outSpikeFilePath, 'r') as f:
        with open(outputSPIKETxt, 'w') as write_file:
            reader = csv.reader(f, delimiter = ',')
            write_file = csv.writer(write_file, delimiter = '\t')
            count = 0
            for row in reader:
                if count == 0: 
                    count += 1
                    continue
                length = len(row)
                row = map(lambda x: float(x)*args['dt'], row)
                write_file.writerow([count, length, *row])
                count += 1
    with open(configTxt, 'w') as f:
        write_file = csv.writer(f, delimiter = '\t')
        write_file.writerow([count - 1, args['dt'], float(args['totalTime'])])

            
if __name__ == '__main__':
    convert_to_Johns_plotting_function('result/0.125_7500_20211025_115626')