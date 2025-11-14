from pathlib import Path
import numpy as np
import sys
import csv

# --- Exempelkod för att hämta data (kan kopieras in i annan .py-fil i samma folder som data_tools) ---

#    from data_tools import CSVTools, MatrixTools
#
#    # Hämta csv-data
#    path = "Data/Jury/2023_jury_results.csv"
#    votes = CSVTools.load(path)
#
#    # Konvertera till matris (storlek 5x5)
#    matrix, countries = MatrixTools.matrix_from_data(votes, 5)
#
#    # Printa (frivilligt)
#    print(matrix)
#    print(countries)

class CSVTools:
    @staticmethod
    def load(relative_path, root_dir=None):
        # Get path to root
        project_root = Path(__file__).resolve().parent
        root_dir = Path(root_dir) if root_dir else project_root
        
        # Fetch data from relative path
        path = root_dir / Path(relative_path)
        with path.open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))
        
keys_to_remove = ['Contestant', 'Total score', 'Jury score', 'Televoting score']

class MatrixTools:    
    @staticmethod
    # Creates a matrix from the given csv data.
    # Set max_size = 0 for a matrix with data for every country.
    def matrix_from_data(data, max_size: int = 0, filter = None):
        max_size = sys.maxsize if max_size == 0 else max_size
        
        # Get ordered country keys
        ordered_keys = MatrixTools.__get_country_order(data, max_size)
        
        # Strip data
        countries = MatrixTools.__strip_datas(data, max_size)
        
        # Permutate collumns
        countries = MatrixTools.__permutate_collumns_by_keys(countries, ordered_keys)
        
        # Convert to matrix
        return MatrixTools.__dict_to_matrix(countries, ordered_keys, filter)
    
    # Get the order of the countries (by row)
    @staticmethod
    def __get_country_order(countries, max_size: int):
        ordered_keys = []
        for index, country in enumerate(countries):
            if index >= max_size:
                break
            contestant = country.get('Contestant')
            if contestant is not None:
                ordered_keys.append(contestant)
        return ordered_keys
    
    # Move collumns by key to the permutation_keys' positions
    @staticmethod
    def __permutate_collumns_by_keys(countries, permutation_keys):
        permutated = []
        for country in countries:
            new_country = {}
            for key in permutation_keys:
                if key in country:
                    new_country[key] = country[key]
            permutated.append(new_country)
        return permutated

    # Strips keys_to_remove from a country
    @staticmethod
    def __strip_data(country: dict, max_size: int) -> dict:
        stripped_country = dict()
        for key, value in country.items():
            if key not in keys_to_remove:
                stripped_country[key] = value
        return stripped_country
    
    # Strip_data for multiple countries
    @staticmethod
    def __strip_datas(countries, max_size: int):
        stripped_countries = []
        for index, country in enumerate(countries):
            if index >= max_size:
                break
            stripped_countries.append(MatrixTools.__strip_data(country, max_size))
        return stripped_countries

    # Convert dict data to np matrix
    @staticmethod
    def __dict_to_matrix(countries, ordered_keys, filter = None):
        if filter == None:
            filter = lambda x: x
        def str_to_int(value):
            if value is None:
                return 0
            if value == '':
                return 0
            return int(value)

        # Populate rows
        rows = []
        for country in countries:
            row = []
            for key in ordered_keys:
                row.append(filter(str_to_int(country.get(key))))
            rows.append(row)

        return (np.asarray(rows, dtype=float), ordered_keys)
    

# Example use
if __name__ == "__main__":
    # Get voting data
    path = "Data/Jury/2023_jury_results.csv"
    votes = CSVTools.load(path)

    # Convert to matrix form (size limited to 5x5)
    matrix, countries = MatrixTools.matrix_from_data(votes, 5)

    print(matrix)
    print(countries)