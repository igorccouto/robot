import os
import settings
from selenium import webdriver


def create_Options(**kwargs):
    """Creates an Options object to customize the browser. All settings are
    passed by kwargs (dictionary). Accepted arguments.
        + user-agent : str
        + window-size : str
        + --lang : str
        + user-data-dir : str
        + --proxy-server : str
        + --log-level : int
        + --headless : bool
        + disable-automation-extension : bool
        + password-manager : bool
        + extensions : list

    Returns:
        Options -- An object to customize a browser.
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

def create_driver(**kwargs):
    """Creates a Chrome Web

    Returns:
        webdriver.Chrome: The Chrome webdriver.
    """
    # Executable path
    if kwargs.get('executable_path'):
        executable_path = kwargs.get('executable_path')
    else:
        executable_path = os.path.join(settings.DRIVER_DIR, 'chromedriver.exe')

    try:
        driver = webdriver.Chrome(executable_path=executable_path)
    except:
        return None

    return driver