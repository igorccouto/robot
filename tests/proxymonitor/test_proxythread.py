import mock
from threading import Thread
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
    t = ProxyThread(proxy=proxy)
    t.start()
    t.join()
    mock_update_proxy.assert_called()

@mock.patch('robot.proxymonitor.proxytools.update_proxy')
def test_updates_proxy_arg(mock_update_proxy):
    proxy = mock_data.create_sample_proxy()
    t = ProxyThread(proxy=proxy)
    t.start()
    t.join()
    mock_update_proxy.assert_called_with(proxy)

@mock.patch('robot.proxymonitor.proxytools.update_proxy')
def test_(mock_update_proxy):
    proxy = mock_data.create_sample_proxy()
    t = ProxyThread(proxy=proxy)
    t.start()
    t.is_alive()
    t.join()
