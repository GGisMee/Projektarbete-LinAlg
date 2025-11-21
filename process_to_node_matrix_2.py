import numpy as np
from data_tools_1 import CSVTools, MatrixTools

def get_binary_matrix(threshold=8, max_size=0):
    
    path = "Data/Jury/2023_jury_results.csv"
    votes = CSVTools.load(path)
    
    matrix, countries = MatrixTools.matrix_from_data(votes, max_size)

    binary_list = []

    for row in matrix:
        new_row = []
        for score in row:
            if score >= threshold:
                new_row.append(1)  
            else:
                new_row.append(0) 
        
        binary_list.append(new_row)

    binary_matrix = np.array(binary_list)

    return binary_matrix, countries