#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author: jiehua233@gmail.com
# @date: 2015-09-27
#

""" 手机号码相关 """

import db
from utils import db_cache

@db_cache("ip")
def get_info(id):
    return db.mysql.get("SELECT * FROM `ipregion` WHERE `id` = %s", id)

def getall():
    return db.mysql.query(
        "SELECT `id`, `start_int` FROM `ipregion` ORDER BY `start_int`")
