import mock
from robot.data import loader
from robot.proxymonitor import proxydata


PROXIES = [{'proxy': '163.172.111.11:1231'},
           {'proxy': '163.172.111.11:1232'},
           {'proxy': '163.172.111.11:1233'},
           {'proxy': '163.172.111.11:1234'}]

WILLIS_TEXAS_CONN = {'status': 'success',
                     'country': 'United States',
                     'countryCode': 'US',
                     'region': 'TX',
                     'regionName': 'Texas',
                     'city': 'Willis',
                     'zip': '77318',
                     'lat': 30.4416,
                     'lon': -95.5394,
                     'timezone': 'America/Chicago',
                     'isp': 'Suddenlink Communications',
                     'org': 'Suddenlink Communications',
                     'as': 'AS19108 Suddenlink Communications',
                     'query': '74.193.3.21',
                     'latency': 0.9512729644775391}

WINTER_SPRINGS_FL_CONN = {'status': 'success',
                          'country': 'United States',
                          'countryCode': 'US',
                          'region': 'FL',
                          'regionName': 'Florida',
                          'city': 'Winter Springs',
                          'zip': '32708',
                          'lat': 28.6841,
                          'lon': -81.2812,
                          'timezone': 'America/New_York',
                          'isp': 'Charter Communications',
                          'org': 'Spectrum',
                          'as': 'AS33363 Charter Communications, Inc',
                          'query': '68.204.29.145',
                          'latency': 1.1133949756622314}

NON_USA_CONN = {'status': 'success',
                'country': 'Brazil',
                'countryCode': 'BR',
                'region': 'PA',
                'regionName': 'Para',
                'city': 'Ananindeua',
                'zip': '67000',
                'lat':-1.3461,
                'lon':-48.3829,
                'timezone': 'America/Belem',
                'isp': 'Interconect Teleinformatica Ltda',
                'org': 'Interconect Teleinformatica Ltda',
                'as': 'AS262492 INTERCONECT TELEINFORMATICA LTDA',
                'query': '168.121.108.34',
                'latency': 2.513394992828963}

FAILED_CONN = {'status': 'not success',
               'latency': None}

def create_sample_proxy():
    with mock.patch('robot.data.loader.read_csv') as mock_read_csv:
        mock_read_csv.return_value = PROXIES
        data = loader.read_csv('ANY CSV')
    proxy = proxydata.load_proxies(proxies=data)[0]

    return proxy
