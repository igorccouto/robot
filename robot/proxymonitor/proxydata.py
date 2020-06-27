import tzlocal
import settings
from typing import List
from robot.data import loader
from datetime import datetime as dt
from multiprocessing import Manager


def load_proxies(proxies: List[dict]) -> Manager:
    "Loads proxies to a multiprocessing.Manager"
    m = Manager()
    m_proxies = m.list()

    for p in proxies:
        p.update({'connection': m.dict(),
                  'available': m.Event(),
                  'change_ip': m.Event(),
                  'busy': m.Event(),
                  'releases': 0,
                  'last_change': dt.now(tz=tzlocal.get_localzone()),
                  'refresh_time': settings.PROXY_REFRESH_TIME})
        if 'proxy' in p:
            p.update({'server': p['proxy']})
            del p['proxy']

        m_proxies.append(p)

    return m_proxies
