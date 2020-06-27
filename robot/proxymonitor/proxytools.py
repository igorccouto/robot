import time
import requests
from json import JSONDecodeError
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