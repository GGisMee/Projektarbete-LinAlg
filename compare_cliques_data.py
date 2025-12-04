import data_tools_1 as import_tools
import process_to_node_matrix_2 as to_binary
import find_indices_cliques_3 as find_cliques
import partition_cliques_4 
import rank_cliques_by_size_5
import show_cliques_6
import compare_data_7

import numpy as np

def iterate_clique_data():
    pass

if __name__ == "__main__":
    years: list[int] = [2023, 2022]
    jury: bool = True
    Tele: bool = True
    number_of_countries = 25
    show_cliques: bool = True


    files = ("Data/Jury/2016_jury_results.csv", "Data/Jury/2017_jury_results.csv")
    csv_tools = import_tools.CSVTools()
    votes = csv_tools.load(relative_path=files[0])
    matrix_tools = import_tools.MatrixTools()
    matrix, countries = matrix_tools.matrix_from_data(votes, number_of_countries)

    # Turn matrix to binary matrix (directed matrix)
    binary_matrix = to_binary.get_binary_matrix(matrix, threshold=4)

    # Gets the indicies which are in cliques (greater with more countries then 2) and their names
    symmetrical_matrix = find_cliques.get_symmetric_matrix(binary_matrix)
    clique_indicies, clique_names =  find_cliques.find_cliques(symmetrical_matrix, countries)

    # seperate into clique groups
    cliques_list = partition_cliques_4.seperate_into_cliques(np.array(list(range(len(symmetrical_matrix)))), symmetrical_matrix)
    cliques_list = partition_cliques_4.filter_out_cliques_with_2_or_less(cliques_list)
    str_cliques_list = partition_cliques_4.separated_cliques_to_name(cliques=cliques_list, names=countries)
    rank_cliques_by_size_5.rank(str_cliques_list)

    # display cliques
    # cliques_display = show_cliques_6.CliquesDislay(VERTEX_MATRIX=symmetrical_matrix, NODE_NAMES=countries, CHOSEN_NODES=clique_indicies.tolist())
    # cliques_display.setup_pygame_vars(1500, 1000)
    # cliques_display.setup_node_vars(20, LINE_WIDTH=2)
    # cliques_display.setup_movement_vars(node_distance=400, unconnected_multiplier=80, center_speed=0.05)
    # cliques_display.run()

    # compare_data_7.run()   

