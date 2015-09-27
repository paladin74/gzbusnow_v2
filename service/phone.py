#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author: jiehua233@gmail.com
# @date: 2015-09-27
#

import constants

from protocols import JSONBaseHandler
from models import phone

class PhoneRegionHandler(JSONBaseHandler):
    """ 手机归属地 """

    def get(self):
        num = self.get_argument('num', '')
        # 参数为空
        if num == '':
            return self.return_error(constants.ERR_PHONE_NULL)

        # 是否为纯数字
        if not num.isdigit():
            return self.return_error(constants.ERR_PHONE_TYPE)

        # 长度
        if len(num) < 7:
            return self.return_error(constants.ERR_PHONE_LENGTH)

        num = num[:7]
        region_info = phone.get_region(num)
        if region_info == None:
            return self.return_error(constants.ERR_REGION_NULL)

        result = {
            'region': region_info['region'],
            'type': region_info['cardtype'],
            'regioncode': region_info['regioncode'],
            'postcode': region_info['postcode'],
        }
        return self.return_result(result)
