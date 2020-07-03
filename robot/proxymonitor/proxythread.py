import time
from typing import Dict
from threading import Thread, Event
from robot.proxymonitor import proxytools


class ProxyThread(Thread):
    def __init__(self, proxy: Dict):
        self.proxy = proxy
        self.terminated = Event()
        Thread.__init__(self)

    def run(self):
        # Runs until terminated event be set
        while not self.terminated.is_set():
            proxytools.update_proxy(self.proxy)
            # Waits a little
            time.sleep(self.proxy.get('refresh_time'))

    def terminate(self):
        # By default, thread doesn't have terminate methods
        self.terminated.set()
