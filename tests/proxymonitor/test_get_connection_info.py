import mock
from json import JSONDecodeError
from robot.proxymonitor import proxytools
from requests.exceptions import ConnectTimeout, ConnectionError


def test_response_keys_NOT_MOCKED():
    excepted_keys = ['status', 'country', 'countryCode', 'region', 'regionName',
                     'city', 'zip', 'lat', 'lon', 'timezone', 'isp', 'org', 'as',
                     'query']
    response = proxytools.get_connection_info()
    for k in excepted_keys:
        assert k in response.keys(), '%s key not in get_connection_info response.' % k

def test_over_proxy_NOT_MOCKED():
    response = proxytools.get_connection_info(proxy_server='163.172.111.11:1231')
    assert 'success' == response.get('status')

def test_unauthorized_NOT_MOCKED():
    response = proxytools.get_connection_info(proxy_server='163.172.111.11:1230')
    assert 'success' != response.get('status')

def test_status_code_not_200():
    status = b'Not 200 status code'
    r = mock.Mock(status_code=0, content=status)
    with mock.patch('robot.proxymonitor.proxytools.requests.get') as mock_get:
        mock_get.return_value = r
        response = proxytools.get_connection_info()

    assert response.get('status') == status.decode()

def test_deals_with_ConnectTimeout():
    error_msg = 'ANY ERROR MESSAGE'
    with mock.patch('robot.proxymonitor.proxytools.requests.get') as mock_get:
        mock_get.side_effect = ConnectTimeout(error_msg)
        response = proxytools.get_connection_info()
    assert error_msg == response.get('status')

def test_deals_with_ConnectionError():
    error_msg = 'ANY ERROR MESSAGE'
    with mock.patch('robot.proxymonitor.proxytools.requests.get') as mock_get:
        mock_get.side_effect = ConnectionError(error_msg)
        response = proxytools.get_connection_info()
    assert error_msg == response.get('status')

def test_deals_with_JSONDecodeError():
    error_msg = 'ANY ERROR MESSAGE'
    m = mock.Mock(status_code=200)
    m.json.side_effect = JSONDecodeError(msg=error_msg, doc='', pos=0)
    with mock.patch('robot.proxymonitor.proxytools.requests.get') as mock_get:
        mock_get.return_value = m
        response = proxytools.get_connection_info()
    assert error_msg in response.get('status')