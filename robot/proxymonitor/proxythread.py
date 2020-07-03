from typing import Dict
from threading import Thread
from robot.proxymonitor import proxytools


class ProxyThread(Thread):
    def __init__(self, proxy: Dict):
        self.proxy = proxy
        Thread.__init__(self)

    def run(self):
        proxytools.update_proxy(self.proxy)
