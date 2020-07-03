from typing import Dict
from threading import Thread, Event
from robot.proxymonitor import proxytools


class ProxyThread(Thread):
    def __init__(self, proxy: Dict):
        self.proxy = proxy
        self.terminated = Event()
        Thread.__init__(self)

    def run(self):
        while not self.terminated.is_set():
            proxytools.update_proxy(self.proxy)

    def terminate(self):
        self.terminated.set()
