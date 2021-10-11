import argparse
import os
import sys
sys.path.append('./utils')
from readcsv import ReadWeightCSV
from tqdm import tqdm
import numpy as np

def metricExtract(data_path):
    weight_csv = ReadWeightCSV(data_path)
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

    (i_max, j_max) = w_matrix.shape
    node_type_map = np.zeros(j_max)
    for j in tqdm(range(j_max)):
        weight_matrix_vec = w_matrix[:, j]
        node_type_map[j] = 0 if all(weight_matrix_vec == 0) else -1 if all(weight_matrix_vec <= 0) else 1 
    
    big_matrix = np.vstack((node_type_map, k_in, k_in_plus, k_in_minus, k_out, k_out_plus, k_out_minus, s_in, s_in_plus, s_in_minus, s_out, s_out_plus, s_out_minus)).T
    _, fileName = os.path.split(data_path)
    currentPath, _ = os.path.split(__file__)
    newFileName = 'metric_'+fileName.replace('.txt', '.csv')

    np.savetxt(os.path.join(currentPath, newFileName),big_matrix, delimiter='\t')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Directory for extracting network metrics')
    parser.add_argument('-d', '--dir', type = str, required= True, help = 'Directory of the source file.')
    args = parser.parse_args()
    metricExtract(args.dir)