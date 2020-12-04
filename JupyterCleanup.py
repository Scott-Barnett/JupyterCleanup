#!/usr/bin/env python3

import json
import copy
import sys

class CleanNotebook:
    """
    Takes a Jupyter Notebook (.ipynb) file and strips out all the environment specific info (python version, output etc)

    @param nb_path: Path to the .ipynb fileS
    """
    def __init__(self, nb_path: str):
        self.nb_path = nb_path
        self.data = self.open_nb()
        if self.data is None:
            print("Notebook does not exist")
            return
        
        new_nb = self.cleanup_code()
        self.write_nb(new_nb)

    def cleanup_code(self) -> dict:
        """
        Takes the .ipynb data (in the json form) and cleans the notebook metadata, and removes any output
        """
        new_data = copy.deepcopy(self.data)
        new_data["metadata"]["language_info"]["version"] = 3
        if "kernelspec" in new_data["metadata"]:
            new_data["metadata"].pop('kernelspec')
        for index, cell in enumerate(self.data["cells"]):
            if cell["cell_type"] == "code":
                new_data["cells"][index]["metadata"] = {}
                new_data["cells"][index]["outputs"] = []
                new_data["cells"][index]["execution_count"] = None
        return new_data

    def open_nb(self) -> dict:
        try:
            with open(self.nb_path, 'r') as nb:
                data = json.load(nb)
            return data
        except FileNotFoundError:
            return None

    def write_nb(self, data: dict) -> bool:
        try:
            with open(self.nb_path, 'w') as nb:
                json.dump(data, nb, indent=1)
            return True
        except FileNotFoundError:
            return False

def main():
    if len(sys.argv) != 2:
        print('Please use the format "JupyterCleanup <path_to_ipynb>"')
        return
    CleanNotebook(sys.argv[1])

if __name__ == "__main__":
    main()
