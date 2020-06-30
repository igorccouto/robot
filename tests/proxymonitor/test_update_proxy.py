import mock
import time
import settings
from robot.data import loader
from tests.proxymonitor import mock_data
from robot.proxymonitor import proxydata
from robot.proxymonitor import proxytools


def create_sample_proxy():
    with mock.patch('robot.data.loader.read_csv') as mock_read_csv:
        mock_read_csv.return_value = mock_data.PROXIES
        data = loader.read_csv('ANY CSV')
    proxy = proxydata.load_proxies(proxies=data)[0]

    return proxy

def test_deals_with_non_USA_connections():
    proxy = create_sample_proxy()
    with mock.patch('robot.proxymonitor.proxytools.get_connection_info') as mock_get_connection_info:
        mock_get_connection_info.return_value = mock_data.NON_USA_CONN
        proxytools.update_proxy(proxy)
        assert not proxy.get('available').is_set(), 'Non USA connections sets proxy as available.'

def test_updates_connection_properly():
    proxy = create_sample_proxy()
    with mock.patch('robot.proxymonitor.proxytools.get_connection_info') as mock_get_connection_info:
        mock_get_connection_info.return_value = mock_data.WILLIS_TEXAS_CONN
        proxytools.update_proxy(proxy)
        assert proxy.get('connection') == mock_data.WILLIS_TEXAS_CONN, 'connection not updated with new connection.'
        mock_get_connection_info.return_value = mock_data.WINTER_SPRINGS_FL_CONN
        proxytools.update_proxy(proxy)
        assert proxy.get('connection') == mock_data.WINTER_SPRINGS_FL_CONN, 'connection not updated with new connection.'
        mock_get_connection_info.return_value = mock_data.NON_USA_CONN
        proxytools.update_proxy(proxy)
        assert proxy.get('connection') == mock_data.NON_USA_CONN, 'connection not updated with new non-USA connection.'
        mock_get_connection_info.return_value = mock_data.WINTER_SPRINGS_FL_CONN
        proxytools.update_proxy(proxy)
        assert proxy.get('connection') == mock_data.WINTER_SPRINGS_FL_CONN, 'connection not updated with new connection.'
        mock_get_connection_info.return_value = mock_data.FAILED_CONN
        proxytools.update_proxy(proxy)
        assert proxy.get('connection') == mock_data.FAILED_CONN, 'connection not updated with failed connection.'
        mock_get_connection_info.return_value = mock_data.WILLIS_TEXAS_CONN
        proxytools.update_proxy(proxy)
        assert proxy.get('connection') == mock_data.WILLIS_TEXAS_CONN, 'connection not updated with new connection.'

def test_sets_available_properly():
    proxy = create_sample_proxy()
    with mock.patch('robot.proxymonitor.proxytools.get_connection_info') as mock_get_connection_info:
        mock_get_connection_info.return_value = mock_data.WILLIS_TEXAS_CONN
        proxytools.update_proxy(proxy)
        assert proxy.get('available').is_set(), 'status success but available is not set.'
        proxytools.update_proxy(proxy)
        assert proxy.get('available').is_set(), 'status success continues but available is not set.'
        mock_get_connection_info.return_value = mock_data.WINTER_SPRINGS_FL_CONN
        proxytools.update_proxy(proxy)
        assert proxy.get('available').is_set(), 'new USA connection but available is not set.'
        mock_get_connection_info.return_value = mock_data.NON_USA_CONN
        proxytools.update_proxy(proxy)
        assert not proxy.get('available').is_set(), 'non-USA connection but available is set.'
        mock_get_connection_info.return_value = mock_data.WILLIS_TEXAS_CONN
        proxytools.update_proxy(proxy)
        assert proxy.get('available').is_set(), 'new USA connection but available is not set.'
        mock_get_connection_info.return_value = mock_data.FAILED_CONN
        proxytools.update_proxy(proxy)
        assert not proxy.get('available').is_set(), 'not success status but available is set.'

def test_increases_releases_properly():
    proxy = create_sample_proxy()
    with mock.patch('robot.proxymonitor.proxytools.get_connection_info') as mock_get_connection_info:
        mock_get_connection_info.return_value = mock_data.WILLIS_TEXAS_CONN
        proxytools.update_proxy(proxy)
        assert proxy.get('releases') == 1, 'connection have changed but releases didn\'t increase.'
        proxytools.update_proxy(proxy)
        assert proxy.get('releases') == 1, 'connection haven\'t  changed but releases increased.'
        mock_get_connection_info.return_value = mock_data.WINTER_SPRINGS_FL_CONN
        proxytools.update_proxy(proxy)
        assert proxy.get('releases') == 2, 'connection have changed but releases didn\'t increase.'
        mock_get_connection_info.return_value = mock_data.FAILED_CONN
        proxytools.update_proxy(proxy)
        assert proxy.get('releases') == 2, 'connection status isn\'t success but releases have increased.'
        mock_get_connection_info.return_value = mock_data.WILLIS_TEXAS_CONN
        proxytools.update_proxy(proxy)
        assert proxy.get('releases') == 3, 'connection have changed but releases didn\'t increase.'
        mock_get_connection_info.return_value = mock_data.NON_USA_CONN
        proxytools.update_proxy(proxy)
        assert proxy.get('releases') == 3, 'non-USA connection increased releases.'

def test_sets_change_ip_properly():
    proxy = create_sample_proxy()
    with mock.patch('robot.proxymonitor.proxytools.get_connection_info') as mock_get_connection_info:
        mock_get_connection_info.return_value = mock_data.WILLIS_TEXAS_CONN
        proxytools.update_proxy(proxy)
        assert proxy.get('change_ip').is_set(), 'new connection but change_ip is not set.'
        proxytools.update_proxy(proxy)
        assert not proxy.get('change_ip').is_set(), 'not new connection but change_ip is set.'
        mock_get_connection_info.return_value = mock_data.NON_USA_CONN
        proxytools.update_proxy(proxy)
        assert proxy.get('change_ip').is_set(), 'new non-USA connection but change_ip is not set.'
        proxytools.update_proxy(proxy)
        assert not proxy.get('change_ip').is_set(), 'non-USA connection remains but change_ip is set.'
        mock_get_connection_info.return_value = mock_data.WINTER_SPRINGS_FL_CONN
        proxytools.update_proxy(proxy)
        assert proxy.get('change_ip').is_set(), 'new connection but change_ip is not set.'
        mock_get_connection_info.return_value = mock_data.FAILED_CONN
        proxytools.update_proxy(proxy)
        assert proxy.get('change_ip').is_set(), 'failed connection but change_ip is not set.'
        proxytools.update_proxy(proxy)
        assert not proxy.get('change_ip').is_set(), 'failed connection remains but change_ip is set.'

def test_sets_refresh_time_properly():
    proxy = create_sample_proxy()
    with mock.patch('robot.proxymonitor.proxytools.get_connection_info') as mock_get_connection_info:
        mock_get_connection_info.return_value = mock_data.WILLIS_TEXAS_CONN
        proxytools.update_proxy(proxy)
        assert proxy.get('refresh_time') == settings.PROXY_REFRESH_TIME, 'refresh time increased in an initial successful connection.'
        proxytools.update_proxy(proxy)
        assert proxy.get('refresh_time') == settings.PROXY_REFRESH_TIME, 'refresh time increased even if the connection remains successful.'
        mock_get_connection_info.return_value = mock_data.FAILED_CONN
        proxytools.update_proxy(proxy)
        assert proxy.get('refresh_time') == settings.HIGH_PROXY_REFRESH_TIME, 'refresh time not increased even in failed connection.'
        proxytools.update_proxy(proxy)
        assert proxy.get('refresh_time') == settings.HIGH_PROXY_REFRESH_TIME, 'refresh time changed even if connection remains failed.'
        mock_get_connection_info.return_value = mock_data.WILLIS_TEXAS_CONN
        proxytools.update_proxy(proxy)
        assert proxy.get('refresh_time') == settings.PROXY_REFRESH_TIME, 'refresh time not decreases even if in successful connection.'
        mock_get_connection_info.return_value = mock_data.NON_USA_CONN
        proxytools.update_proxy(proxy)
        assert proxy.get('refresh_time') == settings.HIGH_PROXY_REFRESH_TIME, 'refresh time doesn\'t increase with non-USA connection.'
        mock_get_connection_info.return_value = mock_data.WILLIS_TEXAS_CONN
        proxytools.update_proxy(proxy)
        assert proxy.get('refresh_time') == settings.PROXY_REFRESH_TIME, 'refresh time not decreases even if in successful connection.'

def test_sets_last_change_properly():
    proxy = create_sample_proxy()
    with mock.patch('robot.proxymonitor.proxytools.get_connection_info') as mock_get_connection_info:
        last_change = proxy.get('last_change')
        time.sleep(0.1)
        mock_get_connection_info.return_value = mock_data.WILLIS_TEXAS_CONN
        proxytools.update_proxy(proxy)
        assert proxy.get('last_change') > last_change, 'last_change not updated with successful connection.'
        last_change = proxy.get('last_change')
        time.sleep(0.1)
        proxytools.update_proxy(proxy)
        assert proxy.get('last_change') == last_change, 'last_change updated even if the same connection.'
        last_change = proxy.get('last_change')
        time.sleep(0.1)
        mock_get_connection_info.return_value = mock_data.WINTER_SPRINGS_FL_CONN
        proxytools.update_proxy(proxy)
        assert proxy.get('last_change') > last_change, 'last_change not updated with a new successful connection.'
        last_change = proxy.get('last_change')
        time.sleep(0.1)
        mock_get_connection_info.return_value = mock_data.NON_USA_CONN
        proxytools.update_proxy(proxy)
        assert proxy.get('last_change') > last_change, 'last_change not updated with a non-USA connection.'
        last_change = proxy.get('last_change')
        time.sleep(0.1)
        mock_get_connection_info.return_value = mock_data.FAILED_CONN
        proxytools.update_proxy(proxy)
        assert proxy.get('last_change') > last_change, 'last_change not updated with failed connection.'
        mock_get_connection_info.return_value = mock_data.WINTER_SPRINGS_FL_CONN
        proxytools.update_proxy(proxy)
