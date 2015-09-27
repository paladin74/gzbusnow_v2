#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author: jiehua233@gmail.com
# @date: 2014-12-16
#

import sys
import constants
import urlparse
import tornado.web
import ujson as json

from tornado import httpclient
from crypt import cipher
from protocols import JSONBaseHandler, ak_required
from models import gzbus

reload(sys)
sys.setdefaultencoding('utf-8')

class GZBusnowHandler(JSONBaseHandler):
    """ 实时公交 """

    params = {
        "username": "android",
        "password": "123456",
        "IMSI": "460000290762763",
        "devNumber": "0000000029F6B0C400000000454D8D02VIXPZQKPIK",
        "version": "2.5.8",
        "devType": 0,
        "queryType": 1,
        "type": "line",
    }

    @ak_required
    @tornado.web.asynchronous
    def get(self):
        self._oper = self.arguments.get('oper')
        self._route = self.arguments.get('route')
        self._dir = int(self.arguments.get('dir', 0))
        if self._oper not in ['fuzzy', 'detail']:
            return self.return_error(constants.ERR_OPER_ERROR)
        if self._dir not in [0, 1]:
            return self.return_error(constants.ERR_DIRECTION_ERROR)

        self.params['oper'] = self._oper
        try:
            self.params['routeName'] = self._route.encode('gbk')
        except UnicodeEncodeError:
            return self.return_error(constants.ERR_ENCODE_ERROR)
        # 缓存查询
        if self.params['oper'] == 'fuzzy':
            result = gzbus.get_buskey(self._route)
            if result:
                if u'查询无结果' in result['line']:
                    return self.return_error(constants.ERR_NOT_FOUND)
                else:
                    return self.return_result({"result": result['line']})

        elif self.params['oper'] == 'detail':
            data = self.redis.get("gzbus:busnow:%s" % self._route)
            if data:
                d = json.loads(data)
                result = self.__pacK_busnow(d)
                return self.return_result(result)

            # 缓存不存在，先判断该线路是否存在，再发起网络请求
            if not gzbus.get_busline(self._route):
                return self.return_error(constants.ERR_NOT_FOUND)

        # 缓存不存在，网络请求查询
        self.do_query()

    def do_query(self):
        """ 发起请求 """
        enc_data = cipher.encrypt(self.params)
        url = urlparse.urljoin(constants.SITE_MOBILE[0], 'Bus')
        request = {
            "method": "POST",
            "body": enc_data,
        }
        http_client = httpclient.AsyncHTTPClient()
        http_client.fetch(url, self.handle_callback, **request)

    def handle_callback(self, response):
        if response.code != 200:
            return self.return_error(constants.ERR_SERVER_BUSY)
        bus_data = cipher.decrypt(response.body)

        # 实时请求结果处理
        if self._oper == 'fuzzy':
            gzbus.new_buskey(self._route, bus_data['content'])
            if u'查询无结果' in bus_data['content']:
                return self.return_error(constants.ERR_NOT_FOUND)
            return self.return_result({"result": bus_data['content']})

        elif self.params['oper'] == 'detail':
            if u'查询无结果' in bus_data['content']:
                return self.return_error(constants.ERR_NOT_FOUND)
            self.redis.setex(
                "gzbus:busnow:%s" % self._route, json.dumps(bus_data['content']), 30)
            result = self.__pacK_busnow(bus_data['content'])
            return self.return_result(result)

    def __pacK_busnow(self, d):
        """ 数据打包 """
        # 方向选择
        d = d[self._dir]
        result = {}
        result['busLine'] = {
            "lineName": d['busLine']['lineName'],
            "firstTime": d['busLine']['firstTime'],
            "lastTime": d['busLine']['lastTime'],
            "strPlatName": d['busLine']['strPlatName'],
            "endPlatName": d['busLine']['endPlatName'],
            "totalPlat": d['busLine']['totalPlat'],
            "stationNames": d['busLine']['stationNames'],
            "flagSubway": d['busLine']['flagSubway'],
        }
        result['busTerminal'] = []
        for bus in d['busTerminal']:
            b = {
                "stationSeq": bus['stationSeq'],
                "adflag": bus['adflag'],
            }
            result['busTerminal'].append(b)

        return result
