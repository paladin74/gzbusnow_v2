#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author: jiehua233@gmail.com
# @date: 2015-09-27
#

""" 手机号码相关 """

import db
from utils import db_cache

@db_cache("phone")
def get_region(phone):
    return db.mysql.get(
        "SELECT * FROM `phoneregion` WHERE `phone` = %s", phone)

