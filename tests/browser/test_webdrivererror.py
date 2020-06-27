from robot.browser.webdrivererror import WebDriverError
from selenium.common.exceptions import WebDriverException


def test_error_message():
    exception = WebDriverException('ANY MESSAGE')
    try:
        raise WebDriverError(error=exception, message='ANY MESSAGE')
    except WebDriverError as e:
        assert e.message == 'ANY MESSAGE'
        assert 'WebDriverException' in e.__str__()
