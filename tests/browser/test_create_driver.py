import os
import mock
import pytest
import settings
from robot.browser import chrome
from selenium.common.exceptions import WebDriverException


@mock.patch('selenium.webdriver.Chrome', side_effect=WebDriverException)
def test_avoids_WebDriverException(mock_Chrome):
    try:
        chrome.create_driver()
    except WebDriverException:
        pytest.fail('WebDriverException not avoided by function.')

@mock.patch('selenium.webdriver.Chrome')
def test_accepts_executable_path_arg(mock_Chrome):
    executable_path = os.path.join(settings.DRIVER_DIR, 'chromedriver.exe')
    chrome.create_driver()
    mock_Chrome.assert_called_with(executable_path=executable_path)
    chrome.create_driver(executable_path='ANY PATH')
    mock_Chrome.assert_called_with(executable_path='ANY PATH')

@mock.patch('selenium.webdriver.Chrome')
def test_accepts_options_arg(mock_Chrome):
    executable_path = os.path.join(settings.DRIVER_DIR, 'chromedriver.exe')
    options = chrome.create_Options()
    chrome.create_driver(options=options)
    mock_Chrome.assert_called_with(executable_path=executable_path, options=options)