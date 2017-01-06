from db.mongodb import MongoDB
from utils.log import log
import utils.tools as tools
from base.parser_control import PaserControl
from parsers import *
from base.collector import Collector
import threading

class Main():
    def __init__(self, tab_urls, parser_control_count):
        self._db = MongoDB()
        self._db.set_unique_key(tab_urls, 'url')

        self._collector = Collector(tab_urls)
        self._parser_control_count = parser_control_count
        self._parsers = []

    def add_parser(self, parser):
        self._parsers.append(parser)

    def start(self):
        self._collector.start()

        while self._parser_control_count:
            parser_control = PaserControl(self._collector)

            for parser in self._parsers:
                parser_control.add_parser(parser)
                threading.Thread(target = parser.add_root_url).start()

            parser_control.start()
            self._parser_control_count -= 1

def main():
    parser_count = int(tools.get_conf_value('config.conf', 'parser', 'parser_count'))
    main = Main('urls', parser_count)

    # 添加parser
    main.add_parser(parser)

    main.start()

def download():
    parser_count = int(tools.get_conf_value('config.conf', 'parser', 'parser_count'))
    main = Main('download_urls', parser_count)

    # 添加parser
    main.add_parser(download_file)

    main.start()

if __name__ == '__main__':
    log.info("--------begin--------")
    main()
    download()
