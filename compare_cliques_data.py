import data_tools_1 as import_tools
import process_to_node_matrix_2 as to_binary
import find_indices_cliques_3 as find_cliques
import partition_cliques_4 
import rank_cliques_by_size_5
import compare_data_7

import numpy as np

def get_paths(years: list[int], data_type: str):
    paths = [f'Data/{data_type}/{year}_{data_type}_results.csv' for year in years]
    return paths


def get_all_data(paths: list[str], number_of_countries: int) -> tuple[list[np.ndarray], list[list[str]]]:
    '''Gets relevant data from files
    Returns: matrices, countries.
    matrices: list of matrices of votes
    countries: list of country names corresponding to indices in matrices'''
    csv_tools = import_tools.CSVTools()
    matrix_tools = import_tools.MatrixTools()
    matrices = []
    countries_y = []
    for path in paths:
        votes = csv_tools.load(relative_path=path)
        matrix, countries = matrix_tools.matrix_from_data(votes, number_of_countries)
        
        matrices.append(matrix)
        countries_y.append(countries)
    return matrices, countries_y

def get_cliques(matrices: list[np.ndarray], countries_y:list[list[str]], years: list[int]) -> tuple[list[list], list[list]]:
    '''Returns a list of the cliques'''
    list_clique_indices = []
    list_clique_names = []
    for i,matrix in enumerate(matrices):
        print(f'År {years[i]}')
        # Turn matrix to binary matrix (directed matrix)
        binary_matrix = to_binary.get_binary_matrix(matrix, threshold=4)

        # Gets the indicies which are in cliques (greater with more countries then 2) and their names
        symmetrical_matrix = find_cliques.get_symmetric_matrix(binary_matrix)

        cliques_list = partition_cliques_4.seperate_into_cliques(np.array(list(range(len(symmetrical_matrix)))), symmetrical_matrix)
        cliques_list = partition_cliques_4.filter_out_cliques_with_2_or_less(cliques_list)
        clique_names = partition_cliques_4.separated_cliques_to_name(cliques=cliques_list, names=countries_y[i])
        list_clique_indices.append(cliques_list)
        list_clique_names.append(clique_names)
        rank_cliques_by_size_5.rank(clique_names.copy())
    return list_clique_indices, list_clique_names

def pair_get_data(jury_tele: tuple[bool,bool], years: list[int], number_of_countries: int = 0):
    order_countries = ['Austria', 'Portugal', 'Switzerland', 'Poland', 'Serbia', 'France', 'Cyprus', 'Spain', 'Sweden', 'Albania', 'Italy', 'Estonia', 'Finland', 'Czech Republic', 'Australia', 'Belgium', 'Armenia', 'Moldova', 'Ukraine', 'Norway', 'Germany', 'Lithuania', 'Israel', 'Slovenia', 'Croatia', 'United Kingdom']
    if jury_tele[0]:
        paths = get_paths(years, 'jury')
        matrices, countries_y = get_all_data(paths, number_of_countries)
        print("jury")
        list_clique_index_jury, list_clique_names_jury= get_cliques(matrices, countries_y, years)
    if jury_tele[1]:
        print("televote")
        paths = get_paths(years, 'televote')
        matrices, countries_y = get_all_data(paths, number_of_countries)
        list_clique_index_tele, list_clique_names_tele = get_cliques(matrices, countries_y, years)

    compare_data_7.run(list_clique_names_jury, list_clique_names_tele, countries = order_countries)

if __name__ == "__main__":
    years: list[int] = [2023, 2022, 2021,2019, 2018, 2017,2016]
    data_type = 'jury'
    jury_tele = (True, True)
    number_of_countries = 0
    show_cliques: bool = True
    
    pair_get_data(jury_tele, years, number_of_countries)

    exit()
    paths = get_paths(years, data_type)
    matrices, countries = get_all_data(paths, number_of_countries)
    _, list_clique_names = get_cliques(matrices, countries)

    rank_cliques_by_size_5.rank(list_clique_names)
    
    exit()

    files = ("Data/Jury/2016_jury_results.csv", "Data/Jury/2017_jury_results.csv")
    csv_tools = import_tools.CSVTools()
    votes = csv_tools.load(relative_path=files[0])
    matrix_tools = import_tools.MatrixTools()
    matrix, countries = matrix_tools.matrix_from_data(votes, number_of_countries)

    # Turn matrix to binary matrix (directed matrix)
    binary_matrix = to_binary.get_binary_matrix(matrix, threshold=4)

    # Gets the indicies which are in cliques (greater with more countries then 2) and their names
    symmetrical_matrix = find_cliques.get_symmetric_matrix(binary_matrix)

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

