from pathlib import Path
import csv
import numpy as np

# --- Exempelkod för att hämta data ---

#    from data_importer import CSVTools, MatrixTools
#
#    # Hämta csv-data
#    path = "Data/Jury/2023_jury_results.csv"
#    votes = CSVTools.load(path)
#
#    # Konvertera till matris.
#    matrix, countries = MatrixTools.matrix_from_data(votes)

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
    def matrix_from_data(data, filter = None):
        # Strip data
        countries = MatrixTools.__strip_datas(data)

        # Convert to np matrix
        return MatrixTools.__dict_to_matrix(countries, filter)

    # Strips keys_to_remove from a country dict
    @staticmethod
    def __strip_data(country: dict) -> dict:
        stripped_country = dict()
        for key, value in country.items():
            # Only keep items that are not marked for deletion
            if key not in keys_to_remove:
                stripped_country[key] = value
        
        return stripped_country
    
    # Strip_datas "overload"
    @staticmethod
    def __strip_datas(countries):
        for index, country in enumerate(countries):
            countries[index] = MatrixTools.__strip_data(country)
        return countries

    # Convert dict data to a numeric np matrix
    @staticmethod
    def __dict_to_matrix(countries, filter = None):
        if filter == None:
            filter = lambda x: x
        def str_to_int(value):
            if value is None:
                return 0
            if value == '':
                return 0
            return int(value)
        
        # Order keys based on their first appearance
        ordered_keys = []
        for country in countries:
            for key in country:
                if key not in ordered_keys:
                    ordered_keys.append(key)

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

    # Convert to matrix form
    matrix, countries = MatrixTools.matrix_from_data(votes)

    print(matrix)
    print(countries)