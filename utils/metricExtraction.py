from utils.readcsv import ReadWeightCSV
import numpy as np

def metricExtract(data_path):
    weight_csv = ReadWeightCSV(path)
    # w_matrix
    w_matrix = weight_csv.connectionMatrix
    # w_matrix_plus
    w_matrix_plus = np.copy(w_matrix)
    w_matrix_plus[w_matrix_plus <= 0] = 0
    # w_matrix_minus
    w_matrix_minus = np.copy(w_matrix)
    w_matrix_minus[w_matrix_minus >= 0] = 0

    k_in = np.sum(w_matrix != 0, axis = 1)
    k_out = np.sum(w_matrix != 0, axis = 0)
    k_in_plus = np.sum(w_matrix > 0, axis = 1)
    k_in_minus = np.sum(w_matrix < 0, axis = 1)
    k_out_plus = np.sum(w_matrix > 0, axis = 0)
    k_out_minus = np.sum(w_matrix < 0, axis = 0)

    s_in = np.sum(w_matrix, axis = 1) / k_in
    s_in_plus = np.sum(w_matrix_plus, axis = 1) / k_in_plus
    s_in_minus = np.sum(w_matrix_minus, axis = 1) / k_in_minus
    s_out = np.sum(w_matrix, axis = 0) / k_out
    s_out_plus = np.sum(w_matrix_plus, axis = 0) / k_out_plus
    s_out_minus = np.sum(w_matrix_minus, axis = 0) / k_out_minus

    


    
    
