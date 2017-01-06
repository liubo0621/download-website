import sys
sys.path.append('..')
import init

import base.base_parser as base_parser
import utils.tools as tools
from utils.log import log
from base.collector import Collector
import base.constance as Constance

ROOT_URL = 'http://www.seantheme.com'

def get_save_path(url):
    path = Constance.LOCAL_SAVE_PATH + url[len(ROOT_URL) + 1:]
    if path.endswith('/'):
        path += 'index.html'

    return path

@tools.run_safe_model
def add_root_url():
    pass

@tools.run_safe_model
def parser(url_info):
    url_info['_id'] = str(url_info['_id'])
    log.debug(tools.dumps_json(url_info))

    download(url_info)

def download(url_info):
    url = url_info['url']
    if not url.startswith('http'):
        return

    path = get_save_path(url)
    tools.download_file(url, path)

    base_parser.update_url('download_urls', url, Constance.DONE)
