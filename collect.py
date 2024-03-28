"""
    Collects data from each json file in the `DATA_ROOT` directory.
    Deposits into `OUTPUT_ROOT`/<team_number>.csv directory files.

    ( sorry addison i made an overcomplicated thing again )
"""

import os
import json
import csv

from pathlib import Path
from typing import Dict, List

DEFAULT_DATA_ROOT   = Path("./data/")
DEFAULT_OUTPUT_ROOT = Path("./csv/")

data: Dict[str, List[List]] = {}

def main():
    collect_to_csv(**parse_args())

def collect_to_csv(data_root, output_root, verbose) -> None:
    os.makedirs(output_root, exist_ok=True)
    if not os.path.isdir(data_root):
        print_if(verbose, f"ERROR: Data root folder '{data_root}' does not exist.")

    load_files(data_root, verbose=verbose)
    write_data(output_root, verbose=verbose)

    print_if(verbose, f"\nSuccess!\nData deposited to folder '{output_root}'.")

def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
                    prog='CSVCollector',
                    description='JSON scattered files to CSV.',
                    epilog='python collect.py [<input>] [-o <output>]')

    parser.add_argument('-i', '--input',   default=DEFAULT_DATA_ROOT,   required=False)
    parser.add_argument('-o', '--output',  default=DEFAULT_OUTPUT_ROOT, required=False)
    parser.add_argument('-v', '--verbose', default=True, required=False)

    args = parser.parse_args()

    return dict(
        data_root=Path(args.input),
        output_root=Path(args.output),
        verbose=args.verbose
    )

def print_if(condition, msg):
    if condition: print(msg)

def load_files(data_root, verbose=False) -> None:
    """
        Loads all files in `DATA_ROOT` into the data dictionary.
        Delegates work to `load_file`.
    """
    print_if(verbose, f"Loading data from {data_root}...")

    for root, _, files in os.walk(data_root):
        for file_name in files:
            team_number = root.split("/")[1]
            load_file(team_number, root + '/' + file_name, verbose=verbose)

def load_file(team_number: str, file_path: Path, verbose=False) -> None:
    """
        args:
            team_number: e.g. `"3952"`
            file_path: "./data/<team_number>/(qual | playoffs)/<n>.txt
                       e.g. `"/data/3951/playoffs/5.txt"`

        Appends the *values* of the JSON file to the `data` dict: 
        `data[team_number].append(file_data)`
    """

    print_if(verbose, f"Loading file {file_path}...")

    with open(file_path) as f:
        file_data = json.loads(f.read())
    file_data["file_path"] = file_path

    if data.get(team_number) is None:
        data[team_number] = []
    data[team_number].append(file_data)

def write_data(output_root, verbose=False) -> None:
    """
        args:
            data: A dictionary (team_number: str to data: List[List]) that stores
                  each datum as a list. Each entry in a data list would represent one
                  loaded JSON file. Each key/value pair will become an individual CSV file.

        Writes all the data into individual CSV files at paths OUTPUT_ROOT/<team_number>.csv
        Field names will be written into the first row.
    """

    print_if(verbose, "Writing data...")
    for team_number, team_datas in data.items():
        print_if(verbose, f"Writing data for team #{team_number}...")
        file_name = team_number + ".csv"
        with open(output_root / file_name, "w") as f:
            writer = csv.writer(f)
            writer.writerow(team_datas[0].keys())
            for team_data in team_datas:
                writer.writerow(team_data.values())


if __name__ == "__main__":
    main()