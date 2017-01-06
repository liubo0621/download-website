# -*- coding: utf-8 -*-
'''
Created on 2017-01-03 16:06
---------
@summary: paser 控制类
---------
@author: Boris
'''
import utils.tools as tools
from utils.log import log
from base.collector import Collector
import threading
import time

class  PaserControl(threading.Thread):
    def __init__(self, collector):
        super(PaserControl, self).__init__()
        self._parser = []
        self._collector = collector
        self._urlCount = int(tools.get_conf_value('config.conf', "parser", "url_count"))
        self._interval = int(tools.get_conf_value('config.conf', "parser", "sleep_time"))

    def run(self):
        while True:
            try:
                urls = self._collector.get_urls(self._urlCount)
                print("取到的url大小 %d"%len(urls))

                # 判断是否结束
                if self._collector.is_finished():
                    log.debug("-------------- 结束 --------------")
                    break

                for url in urls:
                    self._parser.parser(url)

                time.sleep(self._interval)
            except Exception as e:
                print(urls)
                log.debug(e)

    def add_parser(self, parser):
        self._parser = parser