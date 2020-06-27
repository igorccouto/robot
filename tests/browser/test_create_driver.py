import os
import mock
import pytest
import settings
from robot.browser import chrome
from robot.browser.webdrivererror import WebDriverError
from selenium.common.exceptions import WebDriverException


@mock.patch('robot.browser.chrome.create_options')
@mock.patch('selenium.webdriver.Chrome')
def test_accepts_executable_path_arg(mock_Chrome, mock_create_options):
    executable_path = 'ANY PATH'
    options = chrome.create_options()
    mock_create_options.return_value = options
    chrome.create_driver(executable_path=executable_path)
    mock_Chrome.assert_called_with(executable_path=executable_path, options=options)

@mock.patch('selenium.webdriver.Chrome')
def test_accepts_options_arg(mock_Chrome):
    executable_path = os.path.join(settings.DRIVER_DIR, 'chromedriver.exe')
    options = chrome.create_options()
    chrome.create_driver(options=options)
    mock_Chrome.assert_called_with(executable_path=executable_path, options=options)

@mock.patch('robot.browser.chrome.create_options')
@mock.patch('selenium.webdriver.Chrome')
def test_create_options_called_by_default(mock_Chrome, mock_create_options):
    chrome.create_driver()
    mock_create_options.assert_called()

@mock.patch('selenium.webdriver.Chrome', side_effect=WebDriverException('ANY MESSAGE'))
def test_avoids_None_in_WebDriverException(mock_Chrome):
    try:
        driver = chrome.create_driver()
        assert driver, 'returns None if a WebDriverException occurs.'
    except WebDriverException:
        pass
    except WebDriverError:
        pass

@mock.patch('selenium.webdriver.Chrome', side_effect=WebDriverException('ANY MESSAGE'))
def test_WebDriverException_launches_WebDriverError(mock_Chrome):
    try:
        chrome.create_driver()
        pytest.fail('WebDriverError not launched.')
    except WebDriverError as e:
        assert e.message == 'ANY MESSAGE'
