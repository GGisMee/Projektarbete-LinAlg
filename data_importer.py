from pathlib import Path
import csv
import numpy as np

class CSVDataImporter:
    def __init__(self, root_dir=None):
        project_root = Path(__file__).resolve().parent
        self.root_dir = Path(root_dir) if root_dir else project_root

    def load(self, relative_path):
        path = self.root_dir / Path(relative_path)
        with path.open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))

# strips keys_to_remove from a country dict
keys_to_remove = ['Contestant', 'Total score', 'Jury score', 'Televoting score']
def strip_data(country: dict) -> dict:
    stripped_country = dict()
    for key, value in country.items():
        # Only keep items that are not marked for deletion
        if key not in keys_to_remove:
            stripped_country[key] = value
            
    return stripped_country

# strip_datas "overload"
def strip_datas(countries):
    for index, country in enumerate(countries):
        countries[index] = strip_data(country)
    return countries

# Convert dict data to an np matrix
def dict_to_matrix(countries):
    return np.matrix((1,1))

if __name__ == "__main__":
    # Get data
    importer = CSVDataImporter()
    countries = importer.load("Data/Jury/2023_jury_results.csv")

    # strip data
    countries = strip_datas(countries)

    # convert to np matrix
    countries_matrix = dict_to_matrix(countries)

    print(countries_matrix)