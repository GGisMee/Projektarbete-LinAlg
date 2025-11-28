import numpy as np
from data_tools_1 import CSVTools, MatrixTools
from process_to_node_matrix_2 import get_binary_matrix

def find_cliques(matrix: np.ndarray, countries: list):
    """Hittar vilka länder som är med i åtmisntone 1 klick."""
    
    symmetrical_matrix = matrix * matrix.T  # Skapar en symmetrisk matris med alla connections som är åt båda hållen
    
    # Tar bort connections med sig själv
    n = symmetrical_matrix.shape[0]
    for i in range(n):
        symmetrical_matrix[i, i] = 0
    
    A3 = np.linalg.matrix_power(symmetrical_matrix, 3) #Beräkna matrisen upphöjt med 3

    # Kolla diagonalerna av A3 för att finna alla länder i klickar
    clique_member_indices = []
    for i in range(n):
        if A3[i, i] != 0:
            clique_member_indices.append(i)
    
    #Finner namnen på alla länder i klickar
    clique_member_names = []
    for index in clique_member_indices:
        name = countries[index]
        clique_member_names.append(name)
        
    return np.array(clique_member_indices), clique_member_names

# Kort exempel för denna fil
if __name__ == "__main__":
    
    path = "Data/Jury/2023_jury_results.csv"
    gransvarde = 6
    
    votes = CSVTools.load(path)
    matrix_raw, country_names = MatrixTools.matrix_from_data(votes, max_size=0)
    
    binary_matrix = get_binary_matrix(matrix_raw, threshold=gransvarde)
    
    indices, names = find_cliques(binary_matrix, country_names)
    
    print(indices, names)