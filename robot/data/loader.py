import csv
from typing import List


def read_csv(file: str, delimiter: str=';', quotechar: str='"') -> List[str]:
    """Reads a CSV file and saves in a list of dictionaries."""

    data = []
    with open(file) as f:
        reader = csv.DictReader(f, delimiter=delimiter, quotechar=quotechar)
        for r in reader:
            data.append(dict(r))

    return data