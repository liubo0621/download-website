# -*- coding: utf-8 -*-
'''
Created on 2017-01-03 11:05
---------
@summary: 提供一些操作数据库公用的方法
---------
@author: Boris
'''

from db.mongodb import MongoDB
import base.constance as Constance

db = MongoDB()

def get_site_id(table, site_name):
    result = db.find(table, {'name':site_name})
    if result:
        return result[0]['site_id']
    else:
        raise AttributeError('%s表中无%s信息'%(table, site_name))

def add_url(table, site_id, url, depth = 0, remark = '', status = Constance.TODO):
    url_dict = {'site_id':site_id, 'url':url, 'depth':depth, 'remark':remark, 'status':status}
    db.add(table, url_dict)

def update_url(table, url, status):
    db.update(table, {'url':url}, {'status':status})