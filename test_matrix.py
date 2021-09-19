import numpy as np

matrix = np.array([[1,2,3],[4,5,6],[7,8,9]])
i, j = matrix.shape

for row in matrix.T:
    print(row)