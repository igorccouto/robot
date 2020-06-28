import time
import tzlocal
import settings
import requests
from json import JSONDecodeError
from datetime import datetime as dt
from multiprocessing import Manager
from requests.exceptions import ConnectTimeout, ConnectionError


def get_connection_info(proxy_server: str='', timeout: int=None) -> dict:
    "Requests to IP-API information about connection."
    ip_api='http://ip-api.com/json'
    # Creates a dict to store response
    response = {}

    # To request over a proxy
    if proxy_server:
        http_proxy = {'http': 'http://%s' % proxy_server}
    else:
        http_proxy = None

    timeout = timeout

    try:
        # Calculates latency
        start_time = time.time()
        r = requests.get(ip_api, proxies=http_proxy, timeout=timeout)
        latency = time.time() - start_time
    except ConnectTimeout as e:
        response.update({'status': e.args[0], 'latency': None})
        return response
    except ConnectionError as e:
        response.update({'status': e.args[0], 'latency': None})
        return response

    # Updates if request have response
    if r.status_code == 200:
        try:
            response.update(r.json())
        except JSONDecodeError as e:
            response.update({'status': e.args[0], 'latency': None})
    else:
        response.update({'status': r.content.decode().replace('\n', '').strip()})

    # Adds latency keys in response
    response.update({'latency': latency})

    return response

def update_proxy(proxy, **kwargs) -> Manager:
    """Updates a proxy object based on connnection data.

    Arguments:
        proxy {dict} -- A shareable dictionary.
    """
    # Stores old connection for comparison
    old_connection = proxy.get('connection').copy()
    # Retrieves new connnection data
    new_connection = get_connection_info(proxy_server=proxy.get('server'))
    # Connection data is always updated
    proxy.update({'connection': new_connection})
    # Conditions
    is_success = new_connection.get('status') == 'success'
    is_USA = new_connection.get('countryCode') == 'US'
    new_IP = old_connection.get('query') != new_connection.get('query')

    # Notifies or not a change in IP
    if new_IP:
        proxy.get('change_ip').set()
        proxy.update({'last_change': dt.now(tz=tzlocal.get_localzone())})
    else:
        proxy.get('change_ip').clear()

    # If not being a successful connection it doesn't continue
    if not is_success:
        proxy.get('available').clear()
        proxy.update({'refresh_time': settings.HIGH_PROXY_REFRESH_TIME})
        return

    # If not being a USA connection it doesn't continue
    if not is_USA:
        proxy.get('available').clear()
        proxy.update({'refresh_time': settings.HIGH_PROXY_REFRESH_TIME})
        return

    # Turns proxy available
    proxy.get('available').set()
    proxy.update({'refresh_time': settings.PROXY_REFRESH_TIME})

    # New IP
    if new_IP:
        releases = proxy.get('releases')
        proxy.update({'releases': releases+1})

    # If delay is True, put thread to sleep
    if kwargs.get('delay'):
        time.sleep(proxy.get('refresh_time'))
