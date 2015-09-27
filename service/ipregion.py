#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author: jiehua233@gmail.com
# @date: 2015-09-27
#

import constants
import utils

from protocols import JSONBaseHandler
from models import ipregion

ip_list = []

def IPInit():
    ipdat = ipregion.getall()
    for ip in ipdat:
        ip_list.append((ip['start_int'], ip['id']))


class IPRegionHandler(JSONBaseHandler):
    """ IP数据查询 """

    def get(self):
        ip = self.get_argument('ip', '')
        if ip == '':
            return self.return_error(constants.ERR_IP_NULL)

        try:
            int_ip = utils.ip2int(ip)
        except:
            return self.return_error(constants.ERR_IP_TYPE)

        ip_info = ipregion.get_info(self._get_id(int_ip))
        result = {
            "ipstart": ip_info['start'],
            "ipend": ip_info['end'],
            "country": ip_info['country'],
            "province": ip_info['region'],
            "area": ip_info['area'],
            "city": ip_info['city'],
            "county": ip_info['county'],
            "isp": ip_info['isp'],
            "total": ip_info['total'],
        }
        self.return_result(result)

    def _get_id(self, int_ip):
        # 二分查找
        i, j = 0, len(ip_list)-1
        while True:
            m = (i+j) / 2
            # 找到了
            if int_ip >= ip_list[m][0] and int_ip < ip_list[m+1][0]:
                break
            # 位于左半部分
            if int_ip < ip_list[m][0]:
                j = m
            else:
                # 位于右半部分
                i = m

        return ip_list[m][1]
