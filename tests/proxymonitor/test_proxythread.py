import mock
import time
from threading import Thread, Event
from tests.proxymonitor import mock_data
from robot.proxymonitor.proxythread import ProxyThread


def test_is_thread():
    proxy = mock_data.create_sample_proxy()
    t = ProxyThread(proxy=proxy)
    assert isinstance(t, Thread), 'ProxyThread is\'nt a thread'

@mock.patch('threading.Thread.__init__', return_value=None)
def test_calls_init(Thread_init_mock):
    t = ProxyThread(proxy='ANY PROXY')
    Thread_init_mock.assert_called()

@mock.patch('robot.proxymonitor.proxytools.update_proxy')
def test_calls_update_proxy(mock_update_proxy):
    proxy = mock_data.create_sample_proxy()
    proxy.update({'refresh_time': 0.01})
    t = ProxyThread(proxy=proxy)
    t.start()
    t.terminate()
    mock_update_proxy.assert_called()

@mock.patch('robot.proxymonitor.proxytools.update_proxy')
def test_updates_proxy_arg(mock_update_proxy):
    proxy = mock_data.create_sample_proxy()
    t = ProxyThread(proxy=proxy)
    proxy.update({'refresh_time': 0.01})
    t.start()
    t.terminate()
    mock_update_proxy.assert_called_with(proxy)

@mock.patch('robot.proxymonitor.proxytools.update_proxy')
def test_has_terminate(mock_update_proxy):
    proxy = mock_data.create_sample_proxy()
    t = ProxyThread(proxy=proxy)
    getattr(t, 'terminate'), 'ProxyThread doesn\'t have interrupt method.'

@mock.patch('robot.proxymonitor.proxytools.update_proxy')
def test_not_set_terminated_as_default(mock_update_proxy):
    proxy = mock_data.create_sample_proxy()
    t = ProxyThread(proxy=proxy)
    assert isinstance(t.terminated, Event), 'terminated attr isn\'t an event.'
    assert not t.terminated.is_set(), 'terminated event not clear by default.'

@mock.patch('robot.proxymonitor.proxytools.update_proxy')
def test_not_set_terminated_at_start(mock_update_proxy):
    proxy = mock_data.create_sample_proxy()
    proxy.update({'refresh_time': 0.01})
    t = ProxyThread(proxy=proxy)
    t.start()
    assert isinstance(t.terminated, Event), 'terminated attr isn\'t an event.'
    assert not t.terminated.is_set(), 'terminated event not clear by default.'
    t.terminate()

@mock.patch('robot.proxymonitor.proxytools.update_proxy')
def test_sets_terminated_at_terminate(mock_update_proxy):
    proxy = mock_data.create_sample_proxy()
    proxy.update({'refresh_time': 0.01})
    t = ProxyThread(proxy=proxy)
    t.start()
    t.terminate()
    assert t.terminated.is_set(), 'terminated not set after terminate be called.'

@mock.patch('robot.proxymonitor.proxytools.update_proxy')
def test_kills_thread_at_terminate(mock_update_proxy):
    proxy = mock_data.create_sample_proxy()
    proxy.update({'refresh_time': 0.01})
    t = ProxyThread(proxy=proxy)
    t.start()
    t.terminate()
    time.sleep(0.1)
    assert not t.is_alive(), 'thread is alive.'

@mock.patch('time.sleep')
@mock.patch('robot.proxymonitor.proxytools.update_proxy')
def test_ProxyThread_calls_sleep(mock_update_proxy, mock_sleep):
    proxy = mock_data.create_sample_proxy()
    proxy.update({'refresh_time': 0.01})
    t = ProxyThread(proxy=proxy)
    t.start()
    t.terminate()
    mock_sleep.assert_called()

@mock.patch('time.sleep')
@mock.patch('robot.proxymonitor.proxytools.update_proxy')
def test_ProxyThread_calls_sleep_with_proxy_refresh_time(mock_update_proxy, mock_sleep):
    proxy = mock_data.create_sample_proxy()
    proxy.update({'refresh_time': 0.01})
    t = ProxyThread(proxy=proxy)
    t.start()
    t.terminate()
    mock_sleep.assert_called_with(proxy.get('refresh_time'))