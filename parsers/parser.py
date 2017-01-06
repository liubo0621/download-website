import sys
sys.path.append('..')
import init
from utils.log import log
import base.base_parser as base_parser
import utils.tools as tools
import base.constance as Constance

ROOT_URL = 'http://www.seantheme.com'

@tools.run_safe_model
def add_root_url():
    url = 'http://www.seantheme.com/color-admin-v2.1/'
    base_parser.add_url('urls', 1, url)

def get_save_path(url):
    path = Constance.LOCAL_SAVE_PATH + url[len(ROOT_URL) + 1:]
    if path.endswith('/'):
        path += 'index.html'

    return path

@tools.run_safe_model
def parser(url_info):
    url_info['_id'] = str(url_info['_id'])
    log.debug(tools.dumps_json(url_info))

    root_url = url_info['url']
    depth = url_info['depth']
    site_id = url_info['site_id']
    remark = url_info['remark']

    # 解析
    html, request = tools.get_html_by_requests(root_url)
    if not html:
        base_parser.update_url('urls', root_url, Constance.EXCEPTION)

    # # 添加该界面的子url 到数据库
    urls = tools.get_urls(html)
    # javascript:;
    for url in urls:
        if url == 'javascript:;' or url.startswith('#') or url.find('@') != -1 or url.startswith('http'):
            continue
        url = tools.get_full_url(root_url, url)
        if url.startswith('http'):
            if url.endswith('/') or url.endswith('.html') or url.find('?') != -1:
                base_parser.add_url('urls', site_id, url, depth + 1, remark)

    # 添加下载链接
    # 本html界面
    base_parser.add_url('download_urls', site_id, request.url, depth, remark)

    # css
    regex = '<link href="(.*?)"'
    urls = tools.get_info(html, regex)
    for url in urls:
        if url.startswith('http'):
            continue

        url = tools.get_full_url(root_url, url)

        if url.startswith('http'):
            base_parser.add_url('download_urls', site_id, url, depth, remark)

    # jss jpg等
    regex = 'src="(.*?)"'
    urls = tools.get_info(html, regex)
    for url in urls:
        if url.startswith('http'):
            continue

        url = tools.get_full_url(root_url, url)

        if url.startswith('http'):
            base_parser.add_url('download_urls', site_id, url, depth, remark)

    base_parser.update_url('urls', root_url, Constance.DONE)

# url_info = {'_id':0, 'url':'http://www.seantheme.com/', 'site_id':1, 'remark':'', 'depth':0}
# parser(url_info)
