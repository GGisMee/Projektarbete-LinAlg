import numpy as np
from data_tools_1 import CSVTools, MatrixTools

def get_binary_matrix(matrix: np.ndarray, threshold:int=8) -> np.ndarray:
    
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

    return binary_matrix

# Kort exempel för denna fil
if __name__ == "__main__":
    path = "Data/Jury/2023_jury_results.csv"
    votes = CSVTools.load(path)
    
    matrix, countries = MatrixTools.matrix_from_data(votes, 10)
    binary_matrix = get_binary_matrix(matrix, 6)
    print(binary_matrix)