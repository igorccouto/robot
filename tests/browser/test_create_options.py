import os
import settings
from robot.browser import chrome
from selenium.webdriver.chrome.options import Options


BROWSER_SETTINGS = {'user-agent': 'SOME USER AGENT',
                    'window-size': 'SOME SIZE',
                    '--lang': 'SOME LANG',
                    'user-data-dir': 'SOME DIR',
                    '--proxy-server': 'SOME PROXY',
                    '--log-level': 3,
                    'disable-automation-extension': True,
                    'password-manager': True,
                    'extensions': []}

def test_returns_options():
    opt = chrome.create_options()
    assert opt, 'the function returns nothing.'
    assert isinstance(opt, Options), 'the functions didn\'t return an Option type.'

def test_accepts_user_agent():
    browser_settings = {'user-agent': 'SOME BROWSER'}
    opt = chrome.create_options(**browser_settings)
    assert 'user-agent=SOME BROWSER' in opt.arguments

def test_accepts_window_size():
    browser_settings = {'window-size': 'SOME SIZE'}
    opt = chrome.create_options(**browser_settings)
    assert 'window-size=SOME SIZE' in opt.arguments

def test_accepts_language():
    browser_settings = {'--lang': 'SOME LANG'}
    opt = chrome.create_options(**browser_settings)
    assert '--lang=SOME LANG' in opt.arguments

def test_accepts_user_data_dir():
    browser_settings = {'user-data-dir': 'SOME DIR'}
    opt = chrome.create_options(**browser_settings)
    assert 'user-data-dir=SOME DIR' in opt.arguments

def test_accepts_proxy_server():
    browser_settings = {'--proxy-server': 'SOME PROXY SERVER'}
    opt = chrome.create_options(**browser_settings)
    assert '--proxy-server=SOME PROXY SERVER' in opt.arguments

def test_accepts_log_level():
    browser_settings = {'--log-level': 2}
    opt = chrome.create_options(**browser_settings)
    assert '--log-level=2' in opt.arguments

def test_accepts_headless():
    browser_settings = {'headless': True}
    opt = chrome.create_options(**browser_settings)
    assert '--headless' in opt.arguments

def test_accepts_automation_extension():
    automation_extension = {'excludeSwitches': ['enable-automation'],
                            'useAutomationExtension': False}
    # Enabling automation extension
    opt = chrome.create_options()
    assert not automation_extension == opt.experimental_options
    # Disabling automation extension
    browser_settings = {'disable-automation-extension': True}
    opt = chrome.create_options(**browser_settings)
    assert automation_extension == opt.experimental_options

def test_accepts_password_manager():
    password_manager = {'prefs': {'credentials_enable_service': False,
                                  'profile': {'password_manager_enabled': False}}}
    # Enabling password manager
    opt = chrome.create_options()
    assert not password_manager == opt.experimental_options
    # Disabling password manager
    browser_settings = {'password-manager': True}
    opt = chrome.create_options(**browser_settings)
    assert password_manager == opt.experimental_options

def test_adds_extensions():
    # No extension added
    opt = chrome.create_options()
    assert len(opt.extensions) == 0
    # Adding a extension
    block_img = os.path.join(settings.DRIVER_DIR, 'block_img.crx')
    browser_settings = {'extensions': [block_img]}
    opt = chrome.create_options(**browser_settings)
    assert len(opt.extensions) == 1
    # Adding 2 extensions
    webrtc_control = os.path.join(settings.DRIVER_DIR, 'webrtc-control.crx')
    browser_settings = {'extensions': [block_img, webrtc_control]}
    opt = chrome.create_options(**browser_settings)
    assert len(opt.extensions) == 2