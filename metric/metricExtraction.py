import numpy as np
import argparse
import os
import utils
#from  import ReadWeightCSV

def metricExtract(data_path):
    weight_csv = utils.readcsv.ReadWeightCSV(data_path)
    # w_matrix
    w_matrix = weight_csv.connectionMatrix
    # w_matrix_plus
    w_matrix_plus = np.copy(w_matrix)
    w_matrix_plus[w_matrix_plus <= 0] = 0
    # w_matrix_minus
    w_matrix_minus = np.copy(w_matrix)
    w_matrix_minus[w_matrix_minus >= 0] = 0

    k_in = np.sum(w_matrix != 0, axis = 1)
    k_in_plus = np.sum(w_matrix > 0, axis = 1)
    k_in_minus = np.sum(w_matrix < 0, axis = 1)
    k_out = np.sum(w_matrix != 0, axis = 0)
    k_out_plus = np.sum(w_matrix > 0, axis = 0)
    k_out_minus = np.sum(w_matrix < 0, axis = 0)

    s_in = np.sum(w_matrix, axis = 1) / k_in
    s_in_plus = np.sum(w_matrix_plus, axis = 1) / k_in_plus
    s_in_minus = np.sum(w_matrix_minus, axis = 1) / k_in_minus
    s_out = np.sum(w_matrix, axis = 0) / k_out
    s_out_plus = np.sum(w_matrix_plus, axis = 0) / k_out_plus
    s_out_minus = np.sum(w_matrix_minus, axis = 0) / k_out_minus

    big_matrix = np.vstack((k_in, k_in_plus, k_in_minus, k_out, k_out_plus, k_out_minus, s_in, s_in_plus, s_in_minus, s_out, s_out_plus, s_out_minus)).T
    _, fileName = os.path.split(data_path)
    currentPath = os.getcwd()
    newFileName = 'metric_'+fileName.replace('.txt', '.csv')
    np.savetxt(os.path.join(currentPath, newFileName),big_matrix, delimiter='\t')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Directory for extracting network metrics')
    parser.add_argument('-d', '--dir', type = str, required= True, help = 'Directory of the source file.')
    args = parser.parse_args()
    metricExtract(args.dir)