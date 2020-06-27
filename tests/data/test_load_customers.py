import mock
from robot.data import loader
from tests.data import mock_data
from multiprocessing.managers import DictProxy, ListProxy


@mock.patch('robot.data.loader.read_csv', return_value=mock_data.CUSTOMERS)
def test_loads_all_data(mock_read_csv):
    data = loader.read_csv(file='some CSV file')
    manager = loader.load_customers(customers=data)
    assert len(data) == len(manager), 'data and manager must have same lenght.'

@mock.patch('robot.data.loader.read_csv', return_value=mock_data.CUSTOMERS)
def test_returns_managers(mock_read_csv):
    data = loader.read_csv(file='some CSV file')
    manager = loader.load_customers(customers=data)
    assert isinstance(manager, ListProxy), 'Main list isn\'t a manager type.'
    for p in manager:
        assert isinstance(p, DictProxy), 'Nested dicts aren\'t manager type.'

@mock.patch('robot.data.loader.read_csv')
def test_selects_option(mock_read_csv):
    # De-select a customer
    mock_data.CUSTOMERS[0]['select'] = ''
    mock_read_csv.return_value = mock_data.CUSTOMERS
    data = loader.read_csv(file='some CSV file')
    manager = loader.load_customers(customers=data)
    assert len(data) != len(manager), 'data and manager couldn\'t have same lenght.'
