import csv


def read_csv(file, delimiter=';', quotechar='"'):
    """Reads an CSV file and saves in a list of dictionaries. Avoid to use outside
    this module.

    Arguments:
        file {str} -- The CSV file path to read

    Keyword Arguments:
        delimiter {str} -- The delimiter of the CSV file (default: {';'})
        quotechar {str} -- The quote character of the CSV file (default: {'"'})

    Returns:
        list -- The list of dictionaries
    """
    data = []

    with open(file) as f:
        reader = csv.DictReader(f, delimiter=delimiter, quotechar=quotechar)
        for r in reader:
            data.append(dict(r))

    return data