import os
import random
import settings
from robot.data import loader
from robot.browser import chrome
from robot.proxymonitor import proxydata


def main():
    # Load customer
    customers_file = os.path.join(settings.DATA_DIR, 'customers.csv')
    customers_data = loader.read_csv(file=customers_file)
    customers = loader.load_customers(customers=customers_data)
    customer = random.choice(customers)

    # Load proxy
    proxies_file = os.path.join(settings.DATA_DIR, 'proxies.csv')
    proxies_data = loader.read_csv(file=proxies_file)
    proxies = proxydata.load_proxies(proxies=proxies_data)
    proxy = random.choice(proxies)

    # Open browser
    browser_settings = {'user-agent': customer.get('user_agent'),
                        'window-size': customer.get('resolution'),
                        '--lang': customer.get('languages'),
                        #'user-data-dir': 'SOME DIR',
                        '--proxy-server': proxy.get('server'),
                        '--log-level': 3,
                        'disable-automation-extension': True,
                        'password-manager': True,
                        'extensions': []}
    options = chrome.create_options(**browser_settings)
    driver = chrome.create_driver(options=options)

    driver.get('https://amazon.com')

if __name__ == "__main__":
    main()
