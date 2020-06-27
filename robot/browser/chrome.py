import os
import settings
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


def create_options(**kwargs) -> webdriver.ChromeOptions:
    """Creates an Options object to customize the browser. All settings are
    passed by kwargs (dictionary). Accepted arguments:\n
    + user-agent : str\n
    + window-size : str\n
    + --lang : str\n
    + user-data-dir : str\n
    + --proxy-server : str\n
    + --log-level : int\n
    + --headless : bool\n
    + disable-automation-extension : bool\n
    + password-manager : bool\n
    + extensions : list\n
    """
    opt = webdriver.ChromeOptions()
    # Adding arguments
    if kwargs.get('user-agent'):
        opt.add_argument('user-agent=%s' % kwargs.get('user-agent'))
    if kwargs.get('window-size'):
        opt.add_argument('window-size=%s' % kwargs.get('window-size'))
    if kwargs.get('--lang'):
        opt.add_argument('--lang=%s' % kwargs.get('--lang'))
    if kwargs.get('user-data-dir'):
        opt.add_argument('user-data-dir=%s' % kwargs.get('user-data-dir'))
    if kwargs.get('--proxy-server'):
        opt.add_argument('--proxy-server=%s' % kwargs.get('--proxy-server'))
    if kwargs.get('--log-level'):
        opt.add_argument('--log-level=%s' % kwargs.get('--log-level'))
    if kwargs.get('headless'):
        opt.add_argument('--headless')
    # Adding experimental options
    if kwargs.get('disable-automation-extension'):
        opt.add_experimental_option("excludeSwitches", ['enable-automation'])
        opt.add_experimental_option('useAutomationExtension', False)
    if kwargs.get('password-manager'):
        opt.add_experimental_option('prefs', {'credentials_enable_service': False,
                                              'profile': {'password_manager_enabled': False}})
    # Adding extentions
    if kwargs.get('extensions'):
        extensions = kwargs.get('extensions')
        for ext in extensions:
            opt.add_extension(ext)

    return opt

def create_driver(**kwargs) -> webdriver.Chrome:
    """Creates a webdriver to Chrome. Accepted arguments:\n
    + executable_path : str\n
    + options : Options\n
    """
    # Executable path
    if kwargs.get('executable_path'):
        executable_path = kwargs.get('executable_path')
    else:
        executable_path = os.path.join(settings.DRIVER_DIR, 'chromedriver.exe')

    if kwargs.get('options'):
        options = kwargs.get('options')
    else:
        options = create_options()

    try:
        driver = webdriver.Chrome(executable_path=executable_path, options=options)
    except WebDriverException as e:
        print('WebDriverException: %s' % e.msg)
        return None

    return driver