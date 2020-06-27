import mock
import settings
from robot.data import loader
from datetime import datetime as dt
from tests.proxymonitor import mock_data
from robot.proxymonitor import proxydata
from multiprocessing.managers import ListProxy, DictProxy, EventProxy


@mock.patch('robot.data.loader.read_csv', return_value=mock_data.PROXIES)
def test_loads_all_data(mock_read_csv):
    data = loader.read_csv(file='some CSV file')
    proxies = proxydata.load_proxies(proxies=data)
    assert len(data) == len(proxies), 'Not all proxies were loaded.'

@mock.patch('robot.data.loader.read_csv', return_value=mock_data.PROXIES)
def test_returns_list_manager(mock_read_csv):
    data = loader.read_csv(file='some CSV file')
    proxies = proxydata.load_proxies(proxies=data)
    assert isinstance(proxies, ListProxy), 'It isn\'t a list manager type.'

@mock.patch('robot.data.loader.read_csv', return_value=mock_data.PROXIES)
def test_returns_dict_inside_list_manager(mock_read_csv):
    data = loader.read_csv(file='some CSV file')
    proxies = proxydata.load_proxies(proxies=data)
    for p in proxies:
        assert isinstance(p, dict), 'It ins\'t a dict type.'

@mock.patch('robot.data.loader.read_csv', return_value=mock_data.PROXIES)
def test_returns_server_key_in_dict(mock_read_csv):
    data = loader.read_csv(file='some CSV file')
    proxies = proxydata.load_proxies(proxies=data)
    key = 'server'
    for p in proxies:
        assert key in p, '%s not in response.' % key
        assert isinstance(p[key], str), '%s ins\'t a string.' % key

@mock.patch('robot.data.loader.read_csv', return_value=mock_data.PROXIES)
def test_returns_server_key_in_dict(mock_read_csv):
    data = loader.read_csv(file='some CSV file')
    proxies = proxydata.load_proxies(proxies=data)
    key = 'server'
    for p in proxies:
        assert key in p, '%s not in response.' % key
        assert isinstance(p[key], str), '%s ins\'t a string.' % key

@mock.patch('robot.data.loader.read_csv', return_value=mock_data.PROXIES)
def test_returns_connection_key_in_dict(mock_read_csv):
    data = loader.read_csv(file='some CSV file')
    proxies = proxydata.load_proxies(proxies=data)
    key = 'connection'
    for p in proxies:
        assert key in p, '%s not in response.' % key
        assert isinstance(p[key], DictProxy), '%s ins\'t a dict manager.' % key

@mock.patch('robot.data.loader.read_csv', return_value=mock_data.PROXIES)
def test_returns_event_keys_in_dict(mock_read_csv):
    data = loader.read_csv(file='some CSV file')
    proxies = proxydata.load_proxies(proxies=data)
    keys = ['available', 'change_ip', 'busy']
    for p in proxies:
        for k in keys:
            assert k in p, '%s not in response.' % k
            assert isinstance(p[k], EventProxy), '%s ins\'t a event.' % k

@mock.patch('robot.data.loader.read_csv', return_value=mock_data.PROXIES)
def test_returns_releases_key_in_dict(mock_read_csv):
    data = loader.read_csv(file='some CSV file')
    proxies = proxydata.load_proxies(proxies=data)
    key = 'releases'
    for p in proxies:
        assert key in p, '%s not in response.' % key
        assert isinstance(p[key], int), '%s ins\'t a integer.' % key
        assert p[key] == 0, '%s is not loaded as ZERO.' % key

@mock.patch('robot.data.loader.read_csv', return_value=mock_data.PROXIES)
def test_returns_last_change_key_in_dict(mock_read_csv):
    data = loader.read_csv(file='some CSV file')
    proxies = proxydata.load_proxies(proxies=data)
    key = 'last_change'
    for p in proxies:
        assert isinstance(p[key], dt), '%s isn\'t an datetime.' % key

@mock.patch('robot.data.loader.read_csv', return_value=mock_data.PROXIES)
def test_returns_refresh_time_key_in_dict(mock_read_csv):
    data = loader.read_csv(file='some CSV file')
    proxies = proxydata.load_proxies(proxies=data)
    key = 'refresh_time'
    for p in proxies:
        assert isinstance(p[key], int), '%s isn\'t an integer.' % key
        assert p[key] == settings.PROXY_REFRESH_TIME, '%s is not loaded following settings.' % key
