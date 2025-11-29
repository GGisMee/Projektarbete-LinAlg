import data_tools_1 as import_tools
import process_to_node_matrix_2 as to_binary
import find_indices_cliques_3 as find_cliques
import partition_cliques_4
import rank_cliques_by_size_5
import show_cliques_6
# import compare_data_7


if __name__ == "__main__":
    number_of_countries = 10
    show_cliques: bool = True


    files = ("Data/Jury/2016_jury_results.csv", "Data/Jury/2017_jury_results.csv")
    csv_tools = import_tools.CSVTools()
    votes = csv_tools.load(relative_path=files[0])
    matrix_tools = import_tools.MatrixTools()
    matrix, countries = matrix_tools.matrix_from_data(votes, number_of_countries)

    binary_matrix = to_binary.get_binary_matrix(matrix, threshold=6)
    clique_indicies, clique_names =  find_cliques.find_cliques(binary_matrix, countries)

    cliques_display = show_cliques_6.CliquesDislay(matrix, countries, CHOSEN_NODES=clique_indicies.tolist())
    cliques_display.setup_pygame_vars(1500, 1000)
    cliques_display.setup_node_vars(14, LINE_WIDTH=2)
    cliques_display.run()
