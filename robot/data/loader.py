import csv
from typing import List
from multiprocessing import Manager


def read_csv(file: str, delimiter: str=';', quotechar: str='"') -> List[str]:
    """Reads a CSV file and saves in a list of dictionaries."""

    data = []
    with open(file) as f:
        reader = csv.DictReader(f, delimiter=delimiter, quotechar=quotechar)
        for r in reader:
            data.append(dict(r))

    return data

def load_customers(customers: List[dict]) -> Manager:
    "Loads selected customers from a list of dicts to a multiprocessing.Manager"
    m = Manager()
    m_list = m.list()

    for c in customers:
        # If selected appends to manager
        if c.get('select'):
            m_list.append(m.dict(c))

    return m_list

def load_proxies(proxies: List[dict]) -> Manager:
    "Loads proxies to a multiprocessing.Manager"
    m = Manager()
    m_list = m.list()

    for p in proxies:
        p.update({'available': m.Event()})
        p.update({'change_ip': m.Event()})
        p.update({'counter': 0})
        p.update({'info': {}})
        p.update({'refresh': 15})
        m_list.append(m.dict(p))

    return m_list