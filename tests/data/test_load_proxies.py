import mock
import settings
from robot.data import loader
from tests.data import mock_data
from multiprocessing.managers import ListProxy, DictProxy, EventProxy


@mock.patch('robot.data.loader.read_csv', return_value=mock_data.PROXIES)
def test_loads_all_data(mock_read_csv):
    data = loader.read_csv(file='some CSV file')
    proxies_manager = loader.load_proxies(proxies=data)
    assert len(data) == len(proxies_manager), 'data and manager must have same lenght.'

@mock.patch('robot.data.loader.read_csv', return_value=mock_data.PROXIES)
def test_returns_managers(mock_read_csv):
    data = loader.read_csv(file='some CSV file')
    manager = loader.load_proxies(proxies=data)
    assert isinstance(manager, ListProxy), 'Main list isn\'t a manager type.'
    for p in manager:
        assert isinstance(p, DictProxy), 'Nested dicts aren\'t manager type.'

@mock.patch('robot.data.loader.read_csv', return_value=mock_data.PROXIES)
def test_return_dict_all_keys(mock_read_csv):
    data = loader.read_csv(file='some CSV file')
    manager = loader.load_proxies(proxies=data)
    keys = ['proxy', 'available', 'change_ip', 'counter', 'info', 'refresh']
    for p in manager:
        for k in keys:
            assert k in p, '%s not in response.' % k

@mock.patch('robot.data.loader.read_csv', return_value=mock_data.PROXIES)
def test_keys_are_event_types(mock_read_csv):
    data = loader.read_csv(file='some CSV file')
    manager = loader.load_proxies(proxies=data)
    keys = ['available', 'change_ip']
    for p in manager:
        for k in keys:
            assert isinstance(p.get(k), EventProxy), '%s isn\'t a Event type' % k
            assert not p.get(k).is_set(), '%s was loaded improperly.'

@mock.patch('robot.data.loader.read_csv', return_value=mock_data.PROXIES)
def test_key_counter(mock_read_csv):
    data = loader.read_csv(file='some CSV file')
    manager = loader.load_proxies(proxies=data)
    for p in manager:
        assert isinstance(p.get('counter'), int), 'counter isn\'t a integer.'
        assert p.get('counter') == 0, 'counter need to be 0 during load.'

@mock.patch('robot.data.loader.read_csv', return_value=mock_data.PROXIES)
def test_key_refresh(mock_read_csv):
    data = loader.read_csv(file='some CSV file')
    manager = loader.load_proxies(proxies=data)
    refresh = settings.PROXY_REFRESH_TIME
    for p in manager:
        assert isinstance(p.get('refresh'), int), 'refresh isn\'t a integer.'
        assert p.get('refresh') == refresh, 'counter need to be %s during load.' % refresh